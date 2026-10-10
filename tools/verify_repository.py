#!/usr/bin/env python3
"""
ENCHDASH Repository Integrity Validator

Validates:
- Firmware manifest hash integrity
- Manifest schema and local paths
- USB VID/PID consistency between firmware and VIA JSON
- Required documentation files
- License file content
- JSON file syntax
- Local markdown link targets

Usage:
    python tools/verify_repository.py
    python tools/verify_repository.py --manifest-only
    python tools/verify_repository.py --verbose
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import List, Tuple


class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def color_text(text: str, color: str) -> str:
    """Apply ANSI color to text if stdout is a TTY"""
    if sys.stdout.isatty():
        return f"{color}{text}{Colors.RESET}"
    return text


def compute_sha256(file_path: Path) -> str:
    """Compute SHA-256 hash of a file"""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()


def manifest_repo_root(manifest_path: Path) -> Path:
    """Get repository root from manifest path (manifest is in FIRMWARE/)"""
    return manifest_path.resolve().parents[1]


def repo_path(repo_root: Path, relative_path: str) -> Path:
    """Resolve path relative to repo root; pass through absolute paths"""
    path = Path(relative_path)
    return path if path.is_absolute() else repo_root / path

# Manifest validation constants
VALID_PROVENANCE = {"incomplete", "functionally rebuilt", "verified"}
REQUIRED_ARTIFACT_FIELDS = {
    "path", "sha256", "hardware_revision", "source_path",
    "via_json", "qmk_base_commit", "source_commit",
    "build_command", "provenance_status",
}


def validate_manifest(repo_root: Path, manifest: dict) -> Tuple[bool, List[str]]:
    """Validate manifest structure, schema, and referenced files"""
    errors = []

    # Check root structure
    if not isinstance(manifest, dict):
        errors.append("Manifest root must be an object")
        return False, errors

    if 'schema_version' not in manifest:
        errors.append("Manifest missing 'schema_version'")

    if 'usb_identity' not in manifest:
        errors.append("Manifest missing 'usb_identity'")
    else:
        usb_identity = manifest.get('usb_identity', {})
        vid = usb_identity.get('vid')
        pid = usb_identity.get('pid')

        if not isinstance(vid, str) or not isinstance(pid, str):
            errors.append("usb_identity.vid and usb_identity.pid must be strings")
        else:
            hex_pattern = re.compile(r'^0x[0-9a-fA-F]{4}$')
            if not hex_pattern.match(vid):
                errors.append(f"usb_identity.vid invalid format: {vid}")
            if not hex_pattern.match(pid):
                errors.append(f"usb_identity.pid invalid format: {pid}")

    artifacts = manifest.get('artifacts')
    if not artifacts:
        errors.append("Manifest must contain non-empty 'artifacts' list")
        return False, errors

    if not isinstance(artifacts, list):
        errors.append("Manifest 'artifacts' must be a list")
        return False, errors

    # Validate each artifact
    for idx, artifact in enumerate(artifacts):
        if not isinstance(artifact, dict):
            errors.append(f"Artifact {idx} must be an object")
            continue

        # Check required fields
        missing = REQUIRED_ARTIFACT_FIELDS - artifact.keys()
        if missing:
            errors.append(f"Artifact {idx} missing fields: {', '.join(sorted(missing))}")
            continue

        # Validate sha256 format
        sha256 = artifact.get('sha256', '')
        if not isinstance(sha256, str) or not re.match(r'^[0-9a-f]{64}$', sha256):
            errors.append(f"Artifact {idx} sha256 must be 64 lowercase hex chars")

        # Validate provenance_status
        status = artifact.get('provenance_status')
        if status not in VALID_PROVENANCE:
            errors.append(f"Artifact {idx} provenance_status must be one of: {', '.join(VALID_PROVENANCE)}")

        # Validate provenance fields for non-incomplete status
        qmk_base = artifact.get('qmk_base_commit')
        src_commit = artifact.get('source_commit')
        build_cmd = artifact.get('build_command')

        if status != 'incomplete':
            if not qmk_base or not isinstance(qmk_base, str):
                errors.append(f"Artifact {idx} with status '{status}' must have non-empty qmk_base_commit string")
            if not src_commit or not isinstance(src_commit, str):
                errors.append(f"Artifact {idx} with status '{status}' must have non-empty source_commit string")
            if not build_cmd or not isinstance(build_cmd, str):
                errors.append(f"Artifact {idx} with status '{status}' must have non-empty build_command string")

        # Validate file paths exist
        for field in ['path', 'source_path', 'via_json']:
            value = artifact.get(field)
            if not value:
                continue

            if not isinstance(value, str):
                errors.append(f"Artifact {idx} {field} must be a string")
                continue

            resolved = repo_path(repo_root, value)
            if not resolved.exists():
                errors.append(f"Artifact {idx} {field} not found: {value}")

        # Validate VIA JSON USB IDs match manifest
        via_json_path_str = artifact.get('via_json')
        if via_json_path_str and isinstance(via_json_path_str, str):
            via_json_path = repo_path(repo_root, via_json_path_str)
            if via_json_path.exists():
                try:
                    with open(via_json_path, 'r', encoding='utf-8') as f:
                        via_json = json.load(f)

                    via_vid = via_json.get('vendorId', '').lower()
                    via_pid = via_json.get('productId', '').lower()
                    manifest_vid = manifest.get('usb_identity', {}).get('vid', '').lower()
                    manifest_pid = manifest.get('usb_identity', {}).get('pid', '').lower()

                    if via_vid != manifest_vid or via_pid != manifest_pid:
                        errors.append(
                            f"Artifact {idx} VIA JSON USB ID mismatch:\n"
                            f"  Manifest: {manifest_vid}:{manifest_pid}\n"
                            f"  VIA JSON: {via_vid}:{via_pid}"
                        )
                except (json.JSONDecodeError, OSError) as e:
                    errors.append(f"Artifact {idx} VIA JSON read error: {e}")

    return len(errors) == 0, errors

def check_manifest_hashes(manifest_path: Path, verbose: bool = False) -> Tuple[bool, List[str]]:
    """Verify all firmware hashes in manifest match actual files"""
    errors = []

    if not manifest_path.exists():
        errors.append(f"Manifest not found: {manifest_path}")
        return False, errors

    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f"Manifest JSON invalid: {e}")
        return False, errors

    artifacts = manifest.get('artifacts', [])
    if not artifacts:
        errors.append("Manifest contains no artifacts")
        return False, errors

    repo_root = manifest_repo_root(manifest_path)
    all_valid = True
    for artifact in artifacts:
        path_str = artifact.get('path')
        expected_hash = artifact.get('sha256')

        if not path_str or not expected_hash:
            errors.append(f"Artifact missing 'path' or 'sha256': {artifact}")
            all_valid = False
            continue

        artifact_path = repo_path(repo_root, path_str)
        if not artifact_path.exists():
            errors.append(f"Artifact file not found: {artifact_path}")
            all_valid = False
            continue

        actual_hash = compute_sha256(artifact_path)
        if actual_hash != expected_hash:
            errors.append(
                f"Hash mismatch for {artifact_path}:\n"
                f"  Expected: {expected_hash}\n"
                f"  Actual:   {actual_hash}"
            )
            all_valid = False
        elif verbose:
            print(f"  ✓ {artifact_path.name}: {actual_hash[:16]}...")

    return all_valid, errors


def check_usb_identity_consistency(manifest_path: Path, verbose: bool = False) -> Tuple[bool, List[str]]:
    """Check USB VID/PID consistency between manifest and VIA JSON files"""
    errors = []

    if not manifest_path.exists():
        return True, []  # Skip if manifest doesn't exist (checked elsewhere)

    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    usb_identity = manifest.get('usb_identity', {})
    expected_vid = usb_identity.get('vid')
    expected_pid = usb_identity.get('pid')

    if not expected_vid or not expected_pid:
        errors.append("Manifest missing usb_identity.vid or usb_identity.pid")
        return False, errors

    repo_root = manifest_repo_root(manifest_path)
    all_valid = True
    for artifact in manifest.get('artifacts', []):
        via_json_path_str = artifact.get('via_json')
        if not via_json_path_str:
            continue

        via_json_path = repo_path(repo_root, via_json_path_str)
        if not via_json_path.exists():
            errors.append(f"VIA JSON not found: {via_json_path}")
            all_valid = False
            continue

        try:
            with open(via_json_path, 'r', encoding='utf-8') as f:
                via_json = json.load(f)
        except json.JSONDecodeError as e:
            errors.append(f"VIA JSON invalid ({via_json_path}): {e}")
            all_valid = False
            continue

        via_vid = via_json.get('vendorId')
        via_pid = via_json.get('productId')

        if via_vid != expected_vid or via_pid != expected_pid:
            errors.append(
                f"USB ID mismatch for {via_json_path.name}:\n"
                f"  Manifest: {expected_vid}:{expected_pid}\n"
                f"  VIA JSON: {via_vid}:{via_pid}"
            )
            all_valid = False
        elif verbose:
            print(f"  ✓ {via_json_path.name}: {via_vid}:{via_pid}")

    return all_valid, errors


def check_required_files(repo_root: Path, verbose: bool = False) -> Tuple[bool, List[str]]:
    """Check that required documentation and license files exist"""
    required_files = [
        'LICENSE',
        'LICENSES/MIT-ErgoDash.txt',
        'LICENSES/GPL-2.0-or-later.txt',
        'THIRD_PARTY_NOTICES.md',
        'FIRMWARE/manifest.json',
        'FIRMWARE/README.md',
        'docs/LEGACY-SUPPORT.md',
        'docs/HARDWARE-ATTRIBUTION.md',
        'docs/RELEASE-CHECKLIST.md',
        'docs/SILKSCREEN-GUIDE.md',
        'docs/evidence/kicad-owner-verification.md',
        'docs/evidence/qmk-build.md',
        'docs/evidence/review-remediation.md',
    ]

    errors = []
    all_valid = True

    for file_rel in required_files:
        file_path = repo_root / file_rel
        if not file_path.exists():
            errors.append(f"Required file missing: {file_rel}")
            all_valid = False
        elif verbose:
            print(f"  ✓ {file_rel}")

    return all_valid, errors


def check_license_content(repo_root: Path, verbose: bool = False) -> Tuple[bool, List[str]]:
    """Verify license files contain expected content"""
    errors = []
    all_valid = True

    # Check MIT license
    mit_license = repo_root / 'LICENSES' / 'MIT-ErgoDash.txt'
    if mit_license.exists():
        content = mit_license.read_text(encoding='utf-8')
        if 'Copyright (c) 2018 omkbd' not in content:
            errors.append("MIT-ErgoDash.txt missing omkbd copyright notice")
            all_valid = False
        elif verbose:
            print("  ✓ MIT-ErgoDash.txt contains omkbd copyright")

    # Check GPL license
    gpl_license = repo_root / 'LICENSES' / 'GPL-2.0-or-later.txt'
    if gpl_license.exists():
        content = gpl_license.read_text(encoding='utf-8')
        if 'GNU GENERAL PUBLIC LICENSE' not in content or 'Version 2, June 1991' not in content:
            errors.append("GPL-2.0-or-later.txt missing expected GPL header")
            all_valid = False
        elif verbose:
            print("  ✓ GPL-2.0-or-later.txt contains GPL v2 header")

    return all_valid, errors


def check_local_markdown_links(repo_root: Path, markdown_files: list) -> Tuple[bool, List[str]]:
    """Check local markdown link targets exist"""
    import urllib.parse

    errors = []
    link_pattern = re.compile(r'!?\[([^\]]*)\]\(([^)]+)\)')

    for md_file in markdown_files:
        if not md_file.exists():
            continue

        try:
            content = md_file.read_text(encoding='utf-8')
        except (OSError, UnicodeDecodeError):
            continue

        for match in link_pattern.finditer(content):
            dest = match.group(2)

            # Skip external links and anchors
            if dest.startswith(('http://', 'https://', 'mailto:', '#')):
                continue

            # Strip fragment
            if '#' in dest:
                dest = dest.split('#')[0]

            if not dest:
                continue

            # URL-decode
            dest = urllib.parse.unquote(dest)

            # Resolve relative to markdown file's parent
            target = (md_file.parent / dest).resolve()

            if not target.exists():
                errors.append(f"Missing local link: {md_file.relative_to(repo_root)} -> {dest}")

    return len(errors) == 0, errors


def main():
    parser = argparse.ArgumentParser(description='ENCHDASH repository integrity validator')
    parser.add_argument('--manifest-only', action='store_true',
                        help='Only check manifest hash integrity and schema')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Print detailed success messages')
    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent
    manifest_path = repo_root / 'FIRMWARE' / 'manifest.json'

    print(color_text("ENCHDASH Repository Integrity Validator", Colors.BOLD))
    print(f"Repository root: {repo_root}\n")

    all_checks_passed = True

    # Check 1: Manifest hash integrity
    print(color_text("[1/7] Firmware manifest hash integrity", Colors.BOLD))
    valid, errors = check_manifest_hashes(manifest_path, args.verbose)
    if valid:
        print(color_text("  ✓ All firmware hashes match manifest", Colors.GREEN))
    else:
        print(color_text("  ✗ Hash verification failed", Colors.RED))
        for error in errors:
            print(color_text(f"    {error}", Colors.RED))
        all_checks_passed = False
    print()

    # Check 2: Manifest schema and local paths
    print(color_text("[2/7] Manifest schema and local paths", Colors.BOLD))
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        valid, errors = validate_manifest(repo_root, manifest)
        if valid:
            print(color_text("  ✓ Manifest schema and paths valid", Colors.GREEN))
        else:
            print(color_text("  ✗ Manifest validation failed", Colors.RED))
            for error in errors:
                print(color_text(f"    {error}", Colors.RED))
            all_checks_passed = False
    except (OSError, json.JSONDecodeError) as e:
        print(color_text(f"  ✗ Cannot read manifest: {e}", Colors.RED))
        all_checks_passed = False
    print()

    if args.manifest_only:
        sys.exit(0 if all_checks_passed else 1)

    # Check 3: USB VID/PID consistency
    print(color_text("[3/7] USB VID/PID consistency", Colors.BOLD))
    valid, errors = check_usb_identity_consistency(manifest_path, args.verbose)
    if valid:
        print(color_text("  ✓ USB identities consistent", Colors.GREEN))
    else:
        print(color_text("  ✗ USB identity mismatch detected", Colors.RED))
        for error in errors:
            print(color_text(f"    {error}", Colors.RED))
        all_checks_passed = False
    print()

    # Check 4: Required files
    print(color_text("[4/7] Required documentation files", Colors.BOLD))
    valid, errors = check_required_files(repo_root, args.verbose)
    if valid:
        print(color_text("  ✓ All required files present", Colors.GREEN))
    else:
        print(color_text("  ✗ Missing required files", Colors.RED))
        for error in errors:
            print(color_text(f"    {error}", Colors.RED))
        all_checks_passed = False
    print()

    # Check 5: License content
    print(color_text("[5/7] License file content", Colors.BOLD))
    valid, errors = check_license_content(repo_root, args.verbose)
    if valid:
        print(color_text("  ✓ License files contain expected content", Colors.GREEN))
    else:
        print(color_text("  ✗ License content validation failed", Colors.RED))
        for error in errors:
            print(color_text(f"    {error}", Colors.RED))
        all_checks_passed = False
    print()

    # Check 6: JSON syntax
    print(color_text("[6/7] JSON file syntax", Colors.BOLD))
    json_files = [
        manifest_path,
        repo_root / 'ErgoDash_4key_mod_positron_elektronik.json',
        repo_root / 'NEW_ErgoDash_4key_V3_mod_positron_elektronik.json',
    ]
    json_valid = True
    for json_file in json_files:
        if json_file.exists():
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    json.load(f)
                if args.verbose:
                    print(f"  ✓ {json_file.name}")
            except json.JSONDecodeError as e:
                print(color_text(f"  ✗ {json_file.name}: {e}", Colors.RED))
                json_valid = False
                all_checks_passed = False

    if json_valid:
        print(color_text("  ✓ All JSON files valid", Colors.GREEN))
    print()

    # Check 7: Local markdown link targets
    print(color_text("[7/7] Local markdown link targets", Colors.BOLD))
    maintained_docs = [
        repo_root / 'README.md',
        repo_root / 'QUICKSTART.md',
        repo_root / 'FIRMWARE' / 'README.md',
        repo_root / 'LICENSE.md',
        repo_root / 'THIRD_PARTY_NOTICES.md',
        repo_root / 'docs' / 'LEGACY-SUPPORT.md',
        repo_root / 'docs' / 'HARDWARE-ATTRIBUTION.md',
        repo_root / 'docs' / 'RELEASE-CHECKLIST.md',
        repo_root / 'docs' / 'SILKSCREEN-GUIDE.md',
        repo_root / 'docs' / 'DEPLOYMENT-REPORT.md',
        repo_root / 'docs' / 'IMPLEMENTATION-SUMMARY.md',
    ]
    valid, errors = check_local_markdown_links(repo_root, maintained_docs)
    if valid:
        print(color_text("  ✓ All local markdown links valid", Colors.GREEN))
    else:
        print(color_text("  ✗ Broken local markdown links detected", Colors.RED))
        for error in errors:
            print(color_text(f"    {error}", Colors.RED))
        all_checks_passed = False
    print()

    # Final summary
    print(color_text("=" * 60, Colors.BOLD))
    if all_checks_passed:
        print(color_text("✓ All integrity checks passed", Colors.GREEN + Colors.BOLD))
        sys.exit(0)
    else:
        print(color_text("✗ Some integrity checks failed", Colors.RED + Colors.BOLD))
        sys.exit(1)


if __name__ == '__main__':
    main()
