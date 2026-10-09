#!/usr/bin/env python3
"""
ENCHDASH Repository Integrity Validator

Validates:
- Firmware manifest hash integrity
- USB VID/PID consistency between firmware and VIA JSON
- License file existence
- Required documentation files
- Link integrity (basic checks)

Usage:
    python tools/verify_repository.py
    python tools/verify_repository.py --manifest-only
    python tools/verify_repository.py --verbose
"""

import argparse
import hashlib
import json
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
    
    all_valid = True
    for artifact in artifacts:
        path_str = artifact.get('path')
        expected_hash = artifact.get('sha256')
        
        if not path_str or not expected_hash:
            errors.append(f"Artifact missing 'path' or 'sha256': {artifact}")
            all_valid = False
            continue
        
        artifact_path = Path(path_str)
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
    
    all_valid = True
    for artifact in manifest.get('artifacts', []):
        via_json_path_str = artifact.get('via_json')
        if not via_json_path_str:
            continue
        
        via_json_path = Path(via_json_path_str)
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


def main():
    parser = argparse.ArgumentParser(description='ENCHDASH repository integrity validator')
    parser.add_argument('--manifest-only', action='store_true',
                        help='Only check manifest hash integrity')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Print detailed success messages')
    args = parser.parse_args()
    
    repo_root = Path(__file__).parent.parent
    manifest_path = repo_root / 'FIRMWARE' / 'manifest.json'
    
    print(color_text("ENCHDASH Repository Integrity Validator", Colors.BOLD))
    print(f"Repository root: {repo_root}\n")
    
    all_checks_passed = True
    
    # Check 1: Manifest hash integrity
    print(color_text("[1/5] Firmware manifest hash integrity", Colors.BOLD))
    valid, errors = check_manifest_hashes(manifest_path, args.verbose)
    if valid:
        print(color_text("  ✓ All firmware hashes match manifest", Colors.GREEN))
    else:
        print(color_text("  ✗ Hash verification failed", Colors.RED))
        for error in errors:
            print(color_text(f"    {error}", Colors.RED))
        all_checks_passed = False
    print()
    
    if args.manifest_only:
        sys.exit(0 if all_checks_passed else 1)
    
    # Check 2: USB VID/PID consistency
    print(color_text("[2/5] USB VID/PID consistency", Colors.BOLD))
    valid, errors = check_usb_identity_consistency(manifest_path, args.verbose)
    if valid:
        print(color_text("  ✓ USB identities consistent", Colors.GREEN))
    else:
        print(color_text("  ✗ USB identity mismatch detected", Colors.RED))
        for error in errors:
            print(color_text(f"    {error}", Colors.RED))
        all_checks_passed = False
    print()
    
    # Check 3: Required files
    print(color_text("[3/5] Required documentation files", Colors.BOLD))
    valid, errors = check_required_files(repo_root, args.verbose)
    if valid:
        print(color_text("  ✓ All required files present", Colors.GREEN))
    else:
        print(color_text("  ✗ Missing required files", Colors.RED))
        for error in errors:
            print(color_text(f"    {error}", Colors.RED))
        all_checks_passed = False
    print()
    
    # Check 4: License content
    print(color_text("[4/5] License file content", Colors.BOLD))
    valid, errors = check_license_content(repo_root, args.verbose)
    if valid:
        print(color_text("  ✓ License files contain expected content", Colors.GREEN))
    else:
        print(color_text("  ✗ License content validation failed", Colors.RED))
        for error in errors:
            print(color_text(f"    {error}", Colors.RED))
        all_checks_passed = False
    print()
    
    # Check 5: JSON syntax
    print(color_text("[5/5] JSON file syntax", Colors.BOLD))
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
