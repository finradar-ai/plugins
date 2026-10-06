#!/usr/bin/env python3
"""Build both client formats from one skill, connection and metadata source."""

import argparse
import hashlib
import io
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
CLAUDE_MANIFEST = ROOT / ".claude-plugin/plugin.json"
CLAUDE_MARKETPLACE = ROOT / ".claude-plugin/marketplace.json"
CUSTOMER_MCP_URL = "https://api.finradar.ai/api/mcp"
OPENAI_MCP_URL = "https://mcp.finradar.ai/api/mcp"
FILES = (
    ".codex-plugin/plugin.json", ".claude-plugin/plugin.json", ".mcp.json",
    "skills/finradar-api/SKILL.md", "README.md", "scripts/package_plugin.py",
    "assets/finradar-icon.png", ".claude-plugin/marketplace.json",
    "legal/privacy-policy/index.html",
)


def archive_bytes(files):
    """The single archive writer for private preparation and public releases."""
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in files.items():
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    return output.getvalue()


def json_bytes(value):
    return (json.dumps(value, indent=2) + "\n").encode()


def write_immutable(destination, data):
    """Write one content-addressed output without replacing another build."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        if destination.read_bytes() != data:
            raise FileExistsError(
                "Output differs from an existing release; choose a new output directory"
            )
        return
    with destination.open("xb") as stream:
        stream.write(data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check", action="store_true")
    action.add_argument("--output-dir", type=Path)
    action.add_argument("--build-output-dir", type=Path,
                        help="Prepare an immutable content-addressed archive for an automated build")
    args = parser.parse_args()

    source = json.loads((ROOT / FILES[0]).read_text())
    if source.get("name") != "finradar" or not source.get("version"):
        raise ValueError("Expected named, versioned FinRadar package metadata")
    expected = {key: source[key] for key in (
        "name", "version", "description", "author", "homepage", "keywords"
    )}
    expected["mcpServers"] = "./.mcp.json"
    category = source["interface"]["category"]
    if not isinstance(category, str) or not category.strip():
        raise ValueError("Expected a non-empty category in canonical package metadata")
    generated = {
        CLAUDE_MANIFEST: expected,
        CLAUDE_MARKETPLACE: {
            "name": source["name"],
            "description": source["description"],
            "owner": source["author"],
            "plugins": [{
                "name": source["name"],
                "source": "./",
                "displayName": source["interface"]["displayName"],
                "description": source["description"],
                "category": category,
            }],
        },
    }
    skill_files = {str(p.relative_to(ROOT)) for p in (ROOT / "skills").rglob("*") if p.is_file()}
    if skill_files != {"skills/finradar-api/SKILL.md"}:
        raise ValueError("Connected plugin must contain one skill and no frozen API references/helpers")
    connection = json.loads((ROOT / ".mcp.json").read_text())
    if connection != {"mcpServers": {"finradar": {
        "type": "http", "url": CUSTOMER_MCP_URL
    }}}:
        raise ValueError("Connection must preserve the existing credential-free FinRadar URL")
    icon_path = source["interface"].get("composerIcon")
    if icon_path != source["interface"].get("logo") or icon_path != "./assets/finradar-icon.png":
        raise ValueError("OpenAI presentation fields must share the canonical FinRadar icon")
    icon = (ROOT / icon_path.removeprefix("./")).read_bytes()
    if not icon.startswith(b"\x89PNG\r\n\x1a\n") or len(icon) > 10_000:
        raise ValueError("Canonical FinRadar icon must be a PNG no larger than 10 KB")
    if any(p.is_symlink() for p in ROOT.rglob("*")):
        raise ValueError("Release input must contain regular files, not symlinks")

    if args.check:
        for path, payload in generated.items():
            if json.loads(path.read_text()) != payload:
                raise ValueError(f"{path.relative_to(ROOT)} differs from its canonical source; rebuild the package")
        print("PASS: shared skill, credential-free connection and matching client metadata/catalog")
        return

    CLAUDE_MANIFEST.parent.mkdir(exist_ok=True)
    for path, payload in generated.items():
        path.write_text(json.dumps(payload, indent=2) + "\n")
    files = {name: (ROOT / name).read_bytes() for name in FILES}
    data = archive_bytes(files)
    digest = hashlib.sha256(data).hexdigest()
    destination = ((args.build_output_dir / digest) if args.build_output_dir is not None
                   else args.output_dir) / "finradar.plugin"
    write_immutable(destination, data)

    openai_files = dict(files)
    openai_connection = json.loads(json.dumps(connection))
    openai_connection["mcpServers"]["finradar"]["url"] = OPENAI_MCP_URL
    openai_files[".mcp.json"] = json_bytes(openai_connection)
    openai_data = archive_bytes(openai_files)
    openai_digest = hashlib.sha256(openai_data).hexdigest()
    openai_destination = ((args.build_output_dir / openai_digest)
                          if args.build_output_dir is not None else args.output_dir) / "finradar-openai.zip"
    write_immutable(openai_destination, openai_data)

    print(json.dumps({
        "package": str(destination),
        "files": len(FILES),
        "sha256": digest,
        "bytes": len(data),
        "openai_package": str(openai_destination),
        "openai_sha256": openai_digest,
        "openai_bytes": len(openai_data),
    }))


if __name__ == "__main__":
    main()
