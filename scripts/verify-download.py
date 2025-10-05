#!/usr/bin/env python3
"""
DWMBlurGlass Download Verification Tool
Helps users verify they have a legitimate copy by checking for malicious patterns in binaries
"""

import os
import sys
import hashlib
from pathlib import Path

def print_banner():
    print("=" * 80)
    print("DWMBlurGlass Download Verification Tool")
    print("=" * 80)
    print()

def check_file_exists(filepath):
    """Check if file exists"""
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return False
    return True

def get_file_hash(filepath, algorithm='sha256'):
    """Calculate file hash"""
    hash_obj = hashlib.new(algorithm)
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return None

def check_digital_signature(filepath):
    """Check if file has a digital signature (Windows only)"""
    if sys.platform != 'win32':
        print("ℹ️  Digital signature check is only available on Windows")
        return None
    
    try:
        import subprocess
        result = subprocess.run(
            ['powershell', '-Command', 
             f'(Get-AuthenticodeSignature "{filepath}").Status'],
            capture_output=True,
            text=True,
            timeout=10
        )
        status = result.stdout.strip()
        
        if status == "Valid":
            print("✅ Digital signature: Valid")
            return True
        elif status == "NotSigned":
            print("⚠️  Digital signature: Not signed")
            print("   Note: Not all releases may be digitally signed")
            return None
        else:
            print(f"❌ Digital signature: {status}")
            return False
    except Exception as e:
        print(f"⚠️  Could not check digital signature: {e}")
        return None

def check_file_size(filepath):
    """Check file size for reasonableness"""
    size = os.path.getsize(filepath)
    size_mb = size / (1024 * 1024)
    
    print(f"ℹ️  File size: {size_mb:.2f} MB")
    
    # DWMBlurGlass should be relatively small (under 50MB)
    if size_mb > 50:
        print("⚠️  Warning: File is larger than expected")
        print("   Legitimate DWMBlurGlass is typically under 10MB")
        return False
    elif size_mb < 0.1:
        print("⚠️  Warning: File is suspiciously small")
        return False
    
    return True

def verify_exe(filepath):
    """Verify an executable file"""
    print(f"\n📁 Verifying: {filepath}")
    print("-" * 80)
    
    if not check_file_exists(filepath):
        return False
    
    # Check file size
    size_ok = check_file_size(filepath)
    
    # Calculate hash
    print("\n🔐 Calculating SHA-256 hash...")
    file_hash = get_file_hash(filepath)
    if file_hash:
        print(f"   Hash: {file_hash}")
        print("\n   Compare this hash with:")
        print("   1. Official GitHub release notes")
        print("   2. Hash posted by official maintainers")
        print("   3. Hash from a trusted source")
    
    # Check digital signature (Windows only)
    print("\n🔏 Checking digital signature...")
    check_digital_signature(filepath)
    
    # Warnings
    print("\n⚠️  IMPORTANT REMINDERS:")
    print("   • Only download from official sources:")
    print("     - GitHub: https://github.com/Maplespe/DWMBlurGlass/releases")
    print("     - Bilibili: https://space.bilibili.com/87195798")
    print("     - winmoes: https://winmoes.com")
    print("   • Never download from file sharing sites or unofficial mirrors")
    print("   • If in doubt, build from source code")
    
    print()
    return size_ok

def main():
    print_banner()
    
    if len(sys.argv) < 2:
        print("Usage: python verify-download.py <path-to-DWMBlurGlass.exe>")
        print()
        print("Example:")
        print("  python verify-download.py DWMBlurGlass.exe")
        print("  python verify-download.py C:\\Downloads\\DWMBlurGlass.exe")
        print()
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    # Verify the file
    result = verify_exe(filepath)
    
    print("=" * 80)
    if result:
        print("✅ Basic checks passed")
        print()
        print("Next steps:")
        print("1. Verify the hash matches official releases")
        print("2. Scan with your antivirus software")
        print("3. If you have the source code, run: python scripts/security-scan.py")
        print("4. Monitor the application for unexpected behavior")
    else:
        print("⚠️  Some checks failed - review warnings above")
        print()
        print("Recommendations:")
        print("1. Re-download from official source")
        print("2. Verify you're on the correct website")
        print("3. Build from source if possible")
    
    print("=" * 80)

if __name__ == '__main__':
    main()
