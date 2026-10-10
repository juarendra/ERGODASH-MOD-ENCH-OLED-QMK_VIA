#!/usr/bin/env python3
"""
Unit tests for ENCHDASH repository validator

Tests behavioral correctness:
- Hash mismatch detection
- USB VID/PID mismatch detection
- Missing file detection
- JSON syntax validation

Usage:
    python tests/test_verify_repository.py
"""

import os
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

# Add tools directory to path to import validator
sys.path.insert(0, str(Path(__file__).parent.parent / 'tools'))
from verify_repository import (
    compute_sha256,
    check_manifest_hashes,
    check_usb_identity_consistency,
    check_required_files,
    check_license_content,
    validate_manifest,
    check_local_markdown_links,
)


class TestComputeSHA256(unittest.TestCase):
    """Test SHA-256 hash computation"""

    def test_known_hash(self):
        """Test hash of known content"""
        with tempfile.NamedTemporaryFile(delete=False, mode='wb') as f:
            f.write(b'test content')
            temp_path = Path(f.name)

        try:
            expected_hash = hashlib.sha256(b'test content').hexdigest()
            actual_hash = compute_sha256(temp_path)
            self.assertEqual(actual_hash, expected_hash)
        finally:
            temp_path.unlink()

    def test_empty_file(self):
        """Test hash of empty file"""
        with tempfile.NamedTemporaryFile(delete=False, mode='wb') as f:
            temp_path = Path(f.name)

        try:
            expected_hash = hashlib.sha256(b'').hexdigest()
            actual_hash = compute_sha256(temp_path)
            self.assertEqual(actual_hash, expected_hash)
        finally:
            temp_path.unlink()


class TestManifestHashValidation(unittest.TestCase):
    """Test firmware manifest hash validation"""

    def test_valid_manifest(self):
        """Test manifest with correct hashes"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            # Create firmware file
            firmware = tmpdir / 'test.hex'
            firmware.write_bytes(b'firmware content')
            firmware_hash = compute_sha256(firmware)

            # Create manifest
            manifest = tmpdir / 'manifest.json'
            manifest.write_text(json.dumps({
                'artifacts': [
                    {
                        'path': str(firmware),
                        'sha256': firmware_hash
                    }
                ]
            }))

            valid, errors = check_manifest_hashes(manifest)
            self.assertTrue(valid)
            self.assertEqual(len(errors), 0)

    def test_hash_mismatch(self):
        """Test manifest with incorrect hash"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            firmware = tmpdir / 'test.hex'
            firmware.write_bytes(b'firmware content')

            manifest = tmpdir / 'manifest.json'
            manifest.write_text(json.dumps({
                'artifacts': [
                    {
                        'path': str(firmware),
                        'sha256': 'incorrect_hash_value'
                    }
                ]
            }))

            valid, errors = check_manifest_hashes(manifest)
            self.assertFalse(valid)
            self.assertGreater(len(errors), 0)
            self.assertIn('mismatch', errors[0].lower())

    def test_missing_artifact_file(self):
        """Test manifest referencing non-existent file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            manifest = tmpdir / 'manifest.json'
            manifest.write_text(json.dumps({
                'artifacts': [
                    {
                        'path': str(tmpdir / 'nonexistent.hex'),
                        'sha256': 'some_hash'
                    }
                ]
            }))

            valid, errors = check_manifest_hashes(manifest)
            self.assertFalse(valid)
            self.assertGreater(len(errors), 0)
            self.assertIn('not found', errors[0].lower())

    def test_missing_manifest(self):
        """Test with missing manifest file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            manifest = tmpdir / 'nonexistent_manifest.json'

            valid, errors = check_manifest_hashes(manifest)
            self.assertFalse(valid)
            self.assertGreater(len(errors), 0)

    def test_invalid_json(self):
        """Test manifest with invalid JSON syntax"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            manifest = tmpdir / 'manifest.json'
            manifest.write_text('{ invalid json }')

            valid, errors = check_manifest_hashes(manifest)
            self.assertFalse(valid)
            self.assertIn('invalid', errors[0].lower())

    def test_relative_paths_from_different_cwd(self):
        """Test manifest with relative paths works from different CWD"""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / 'repo'
            repo.mkdir()

            # Create FIRMWARE/manifest.json
            firmware_dir = repo / 'FIRMWARE'
            firmware_dir.mkdir()
            firmware = firmware_dir / 'test.hex'
            firmware.write_bytes(b'firmware content')
            firmware_hash = compute_sha256(firmware)

            # Create VIA/test.json
            via_dir = repo / 'VIA'
            via_dir.mkdir()
            via_json = via_dir / 'test.json'
            via_json.write_text(json.dumps({
                'vendorId': '0x4D44',
                'productId': '0x6061'
            }))

            # Create manifest with relative paths
            manifest = firmware_dir / 'manifest.json'
            manifest.write_text(json.dumps({
                'usb_identity': {
                    'vid': '0x4D44',
                    'pid': '0x6061'
                },
                'artifacts': [
                    {
                        'path': 'FIRMWARE/test.hex',
                        'sha256': firmware_hash,
                        'via_json': 'VIA/test.json'
                    }
                ]
            }))

            # Change to different directory and verify
            with tempfile.TemporaryDirectory() as other_dir:
                original_cwd = os.getcwd()
                try:
                    os.chdir(other_dir)

                    valid_hash, errors_hash = check_manifest_hashes(manifest)
                    self.assertTrue(valid_hash, f"Hash check failed: {errors_hash}")
                    self.assertEqual(len(errors_hash), 0)

                    valid_usb, errors_usb = check_usb_identity_consistency(manifest)
                    self.assertTrue(valid_usb, f"USB check failed: {errors_usb}")
                    self.assertEqual(len(errors_usb), 0)
                finally:
                    os.chdir(original_cwd)


class TestUSBIdentityConsistency(unittest.TestCase):
    """Test USB VID/PID consistency validation"""

    def test_matching_usb_ids(self):
        """Test manifest and VIA JSON with matching USB IDs"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            via_json = tmpdir / 'test.json'
            via_json.write_text(json.dumps({
                'vendorId': '0x4D44',
                'productId': '0x6061'
            }))

            manifest = tmpdir / 'manifest.json'
            manifest.write_text(json.dumps({
                'usb_identity': {
                    'vid': '0x4D44',
                    'pid': '0x6061'
                },
                'artifacts': [
                    {
                        'path': 'test.hex',
                        'via_json': str(via_json)
                    }
                ]
            }))

            valid, errors = check_usb_identity_consistency(manifest)
            self.assertTrue(valid)
            self.assertEqual(len(errors), 0)

    def test_mismatched_usb_ids(self):
        """Test USB VID/PID mismatch detection"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            via_json = tmpdir / 'test.json'
            via_json.write_text(json.dumps({
                'vendorId': '0x1234',
                'productId': '0x5678'
            }))

            manifest = tmpdir / 'manifest.json'
            manifest.write_text(json.dumps({
                'usb_identity': {
                    'vid': '0x4D44',
                    'pid': '0x6061'
                },
                'artifacts': [
                    {
                        'path': 'test.hex',
                        'via_json': str(via_json)
                    }
                ]
            }))

            valid, errors = check_usb_identity_consistency(manifest)
            self.assertFalse(valid)
            self.assertGreater(len(errors), 0)
            self.assertIn('mismatch', errors[0].lower())


class TestManifestValidation(unittest.TestCase):
    """Test manifest schema validation"""

    def test_manifest_rejects_invalid_sha256_and_status(self):
        """SHA-256 must be 64 lowercase hex; status must be valid"""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)

            # Create minimal artifact file
            firmware_dir = repo_root / 'FIRMWARE'
            firmware_dir.mkdir()
            (firmware_dir / 'test.hex').write_bytes(b'test')

            manifest = {
                'schema_version': '1.0',
                'usb_identity': {'vid': '0x4D44', 'pid': '0x6061'},
                'artifacts': [
                    {
                        'path': 'FIRMWARE/test.hex',
                        'sha256': 'TOOSHORT',  # Invalid
                        'hardware_revision': 'v1',
                        'source_path': 'FIRMWARE',
                        'via_json': 'FIRMWARE/test.hex',
                        'qmk_base_commit': None,
                        'source_commit': None,
                        'build_command': None,
                        'provenance_status': 'invalid_status',  # Invalid
                    }
                ]
            }

            valid, errors = validate_manifest(repo_root, manifest)
            self.assertFalse(valid)
            self.assertTrue(any('sha256' in error.lower() for error in errors))
            self.assertTrue(any('provenance_status' in error for error in errors))

    def test_manifest_rejects_missing_fields(self):
        """All required artifact fields must be present"""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)

            manifest = {
                'schema_version': '1.0',
                'usb_identity': {'vid': '0x4D44', 'pid': '0x6061'},
                'artifacts': [
                    {
                        'path': 'test.hex',
                        # Missing most fields
                    }
                ]
            }

            valid, errors = validate_manifest(repo_root, manifest)
            self.assertFalse(valid)
            self.assertTrue(any('missing fields' in error.lower() for error in errors))

    def test_manifest_enforces_provenance_constraints(self):
        """Non-incomplete status requires commit and build strings"""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            firmware_dir = repo_root / 'FIRMWARE'
            firmware_dir.mkdir()
            (firmware_dir / 'test.hex').write_bytes(b'test')
            (firmware_dir / 'test.json').write_text(json.dumps({
                'vendorId': '0x4d44',
                'productId': '0x6061'
            }))

            # Verified status with null commits should fail
            manifest_bad = {
                'schema_version': '1.0',
                'usb_identity': {'vid': '0x4D44', 'pid': '0x6061'},
                'artifacts': [
                    {
                        'path': 'FIRMWARE/test.hex',
                        'sha256': 'a' * 64,
                        'hardware_revision': 'v1',
                        'source_path': 'FIRMWARE',
                        'via_json': 'FIRMWARE/test.json',
                        'qmk_base_commit': None,
                        'source_commit': None,
                        'build_command': None,
                        'provenance_status': 'verified',
                    }
                ]
            }

            valid, errors = validate_manifest(repo_root, manifest_bad)
            self.assertFalse(valid)
            self.assertTrue(any('qmk_base_commit' in error for error in errors))

            # Incomplete status with null commits should pass
            manifest_ok = {
                'schema_version': '1.0',
                'usb_identity': {'vid': '0x4D44', 'pid': '0x6061'},
                'artifacts': [
                    {
                        'path': 'FIRMWARE/test.hex',
                        'sha256': 'a' * 64,
                        'hardware_revision': 'v1',
                        'source_path': 'FIRMWARE',
                        'via_json': 'FIRMWARE/test.json',
                        'qmk_base_commit': None,
                        'source_commit': None,
                        'build_command': None,
                        'provenance_status': 'incomplete',
                    }
                ]
            }

            valid, errors = validate_manifest(repo_root, manifest_ok)
            self.assertTrue(valid, f"Incomplete with null commits should pass: {errors}")


class TestRequiredFilesExtended(unittest.TestCase):
    """Test extended required file checks"""

    def test_required_files_include_release_and_owner_evidence(self):
        """Missing evidence files must fail"""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)

            # Create some but not all required files
            (repo_root / 'LICENSE').write_text('license')
            (repo_root / 'LICENSES').mkdir()
            (repo_root / 'LICENSES' / 'MIT-ErgoDash.txt').write_text('MIT')
            (repo_root / 'LICENSES' / 'GPL-2.0-or-later.txt').write_text('GPL')
            (repo_root / 'THIRD_PARTY_NOTICES.md').write_text('notices')
            (repo_root / 'FIRMWARE').mkdir()
            (repo_root / 'FIRMWARE' / 'manifest.json').write_text('{}')
            (repo_root / 'FIRMWARE' / 'README.md').write_text('readme')
            (repo_root / 'docs').mkdir()
            (repo_root / 'docs' / 'LEGACY-SUPPORT.md').write_text('legacy')
            (repo_root / 'docs' / 'HARDWARE-ATTRIBUTION.md').write_text('hw')
            (repo_root / 'docs' / 'RELEASE-CHECKLIST.md').write_text('checklist')
            (repo_root / 'docs' / 'SILKSCREEN-GUIDE.md').write_text('silk')
            (repo_root / 'docs' / 'evidence').mkdir()
            (repo_root / 'docs' / 'evidence' / 'qmk-build.md').write_text('qmk')
            (repo_root / 'docs' / 'evidence' / 'review-remediation.md').write_text('review')
            # Missing: kicad-owner-verification.md

            valid, errors = check_required_files(repo_root)
            self.assertFalse(valid)
            self.assertTrue(any('kicad-owner-verification.md' in error for error in errors))


class TestMarkdownLinks(unittest.TestCase):
    """Test markdown link validation"""

    def test_markdown_links_reject_missing_local_targets(self):
        """Relative links must point to existing files"""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)

            # Create a markdown file with broken local link
            readme = repo_root / 'README.md'
            readme.write_text('''
# Test
[Valid external](https://example.com)
[Valid anchor](#section)
[Broken local](missing.md)
![Broken image](missing.png)
''')

            valid, errors = check_local_markdown_links(repo_root, [readme])
            self.assertFalse(valid)
            self.assertTrue(any('missing local link' in error.lower() for error in errors))
            self.assertTrue(any('missing.md' in error for error in errors))


class TestRequiredFiles(unittest.TestCase):
    """Test required file existence checks"""

    def test_all_files_present(self):
        """Test when all required files exist"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            # Create all required files
            (tmpdir / 'LICENSE').touch()
            (tmpdir / 'LICENSES').mkdir()
            (tmpdir / 'LICENSES' / 'MIT-ErgoDash.txt').touch()
            (tmpdir / 'LICENSES' / 'GPL-2.0-or-later.txt').touch()
            (tmpdir / 'THIRD_PARTY_NOTICES.md').touch()
            (tmpdir / 'FIRMWARE').mkdir()
            (tmpdir / 'FIRMWARE' / 'manifest.json').touch()
            (tmpdir / 'FIRMWARE' / 'README.md').touch()
            (tmpdir / 'docs').mkdir()
            (tmpdir / 'docs' / 'LEGACY-SUPPORT.md').touch()
            (tmpdir / 'docs' / 'HARDWARE-ATTRIBUTION.md').touch()
            (tmpdir / 'docs' / 'RELEASE-CHECKLIST.md').touch()
            (tmpdir / 'docs' / 'SILKSCREEN-GUIDE.md').touch()
            (tmpdir / 'docs' / 'evidence').mkdir()
            (tmpdir / 'docs' / 'evidence' / 'kicad-owner-verification.md').touch()
            (tmpdir / 'docs' / 'evidence' / 'qmk-build.md').touch()
            (tmpdir / 'docs' / 'evidence' / 'review-remediation.md').touch()

            valid, errors = check_required_files(tmpdir)
            self.assertTrue(valid)
            self.assertEqual(len(errors), 0)

    def test_missing_license(self):
        """Test detection of missing LICENSE file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            valid, errors = check_required_files(tmpdir)
            self.assertFalse(valid)
            self.assertGreater(len(errors), 0)
            self.assertTrue(any('LICENSE' in error for error in errors))


class TestLicenseContent(unittest.TestCase):
    """Test license file content validation"""

    def test_valid_mit_license(self):
        """Test MIT license with correct omkbd copyright"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            (tmpdir / 'LICENSES').mkdir()
            mit_license = tmpdir / 'LICENSES' / 'MIT-ErgoDash.txt'
            mit_license.write_text('Copyright (c) 2018 omkbd\n\nMIT License...')

            valid, errors = check_license_content(tmpdir)
            self.assertTrue(valid)
            self.assertEqual(len(errors), 0)

    def test_missing_omkbd_copyright(self):
        """Test MIT license missing omkbd copyright notice"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            (tmpdir / 'LICENSES').mkdir()
            mit_license = tmpdir / 'LICENSES' / 'MIT-ErgoDash.txt'
            mit_license.write_text('Some other copyright\n\nMIT License...')

            valid, errors = check_license_content(tmpdir)
            self.assertFalse(valid)
            self.assertGreater(len(errors), 0)
            self.assertIn('omkbd', errors[0].lower())

    def test_valid_gpl_license(self):
        """Test GPL license with correct header"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            (tmpdir / 'LICENSES').mkdir()
            gpl_license = tmpdir / 'LICENSES' / 'GPL-2.0-or-later.txt'
            gpl_license.write_text('GNU GENERAL PUBLIC LICENSE\nVersion 2, June 1991\n...')

            valid, errors = check_license_content(tmpdir)
            self.assertTrue(valid)
            self.assertEqual(len(errors), 0)


def run_tests():
    """Run all tests and report results"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
