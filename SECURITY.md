# Security Policy

## ⚠️ WARNING: Malicious Copies Detected

We have discovered that **malicious versions of DWMBlurGlass are being distributed** with code implants. To protect yourself:

### Official Distribution Channels

✅ **ONLY download DWMBlurGlass from these official sources:**
- [GitHub Releases](https://github.com/Maplespe/DWMBlurGlass/releases)
- [Bilibili](https://space.bilibili.com/87195798)
- [winmoes](https://winmoes.com)

❌ **DO NOT download from:**
- Third-party download sites
- File sharing services
- Unofficial mirrors
- Discord servers (we do not have an official Discord)
- Any other source claiming to be official

## Verifying Authenticity

### 1. Check the Source
Before downloading, verify you are on one of the official sites listed above.

### 2. Verify File Integrity
After downloading, you can verify the integrity of the release:

```bash
# Quick verification using our tool (recommended)
python3 scripts/verify-download.py DWMBlurGlass.exe

# Manual hash check - Windows PowerShell
Get-FileHash DWMBlurGlass.exe -Algorithm SHA256

# Manual hash check - Linux/macOS
sha256sum DWMBlurGlass.exe
```

Compare the hash with the official release notes on GitHub.

### 3. Run Security Scan
If you have cloned the source code repository, you can run our security scanner:

```bash
python3 scripts/security-scan.py
```

This scanner checks for:
- Unexpected network connections
- Data exfiltration attempts
- Suspicious persistence mechanisms
- Code obfuscation patterns
- Malicious file operations

### 4. Check Digital Signatures
Official releases from GitHub may be signed. Verify the digital signature:

```powershell
Get-AuthenticodeSignature DWMBlurGlass.exe
```

## What Makes DWMBlurGlass Legitimate

DWMBlurGlass is a **DWM (Desktop Window Manager) customization tool** that:

1. **Uses DLL injection** - This is expected and required to modify DWM behavior
2. **Requires administrator privileges** - Needed to inject into system processes
3. **Uses function hooking** - Via the MinHook library to intercept Windows APIs
4. **Does NOT:**
   - Make network connections
   - Access your personal files
   - Log keystrokes
   - Send data anywhere
   - Install hidden services
   - Modify system files outside of DWM

## Technical Security Details

### Expected Behavior
The legitimate DWMBlurGlass performs these operations:

- **Process injection into `dwm.exe`**: Required to apply blur effects
- **Windows API hooking**: Uses MinHook library to modify DWM rendering
- **Registry access**: Only for storing user preferences
- **Scheduled tasks**: Optional, for auto-start functionality
- **File operations**: Limited to its own installation directory

### What to Watch For
**WARNING SIGNS of a malicious copy:**

❌ Network activity or internet connections  
❌ Access to Documents, Downloads, or personal folders  
❌ Keyboard or mouse monitoring  
❌ Hidden file creation outside installation directory  
❌ Modifications to Windows system files  
❌ Installation of services not related to DWM  
❌ Requests for credentials or personal information  

## Reporting Security Issues

### Found a Malicious Copy?
If you encounter a malicious version being distributed:

1. **DO NOT run it**
2. Report the source to us via [GitHub Issues](https://github.com/Maplespe/DWMBlurGlass/issues)
3. Include:
   - Where you found it
   - File hash (SHA256)
   - Any suspicious behavior observed

### Found a Vulnerability?
If you discover a security vulnerability in the legitimate DWMBlurGlass:

1. **DO NOT** publicly disclose it
2. Report privately via GitHub Security Advisories or Issues
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will respond to security reports as quickly as possible.

## Build from Source

The most secure way to use DWMBlurGlass is to build it from source:

```bash
# Clone the official repository
git clone https://github.com/Maplespe/DWMBlurGlass.git
cd DWMBlurGlass

# Run security scan
python3 scripts/security-scan.py

# Build using Visual Studio 2022
# Open DWMBlurGlass.sln and build
```

Building from source ensures you have the exact code from the official repository.

## Security Scanning

We provide a Python-based security scanner that checks for malicious patterns:

### Running the Scanner

```bash
python3 scripts/security-scan.py
```

### What It Checks

The scanner looks for suspicious patterns including:
- **Network operations**: HTTP, sockets, downloads
- **Data exfiltration**: Clipboard, keyboard monitoring
- **Persistence**: Startup registry keys, services
- **Code obfuscation**: Encrypted strings, shellcode
- **File operations**: Hidden files, system modifications
- **Unexpected binaries**: Files in wrong locations

### Interpreting Results

- ✅ **No issues found**: Code appears clean
- ⚠️ **Warnings**: Review carefully, may be false positives
- ❌ **Issues found**: Investigate immediately

## Code Review Guidelines

If you're reviewing the code yourself, pay attention to:

1. **No network calls**: Search for `WinHttp`, `Internet`, `socket`, `WSA`
2. **Limited process access**: Only `dwm.exe` should be targeted
3. **No keylogging**: No hooks for `WH_KEYBOARD_LL` or `GetAsyncKeyState`
4. **Transparent file ops**: All file operations should be in installation directory
5. **Open source dependencies**: Check that libraries match official repos

## Dependencies

DWMBlurGlass uses these trusted open-source libraries:
- [MiaoUI Lite](https://github.com/Maplespe/MiaoUILite) - UI library
- [minhook](https://github.com/m417z/minhook) - Function hooking
- [pugixml](https://github.com/zeux/pugixml) - XML parsing
- [Windows Implementation Libraries](https://github.com/Microsoft/wil) - Windows helpers

Always verify these match the official repositories.

## Additional Resources

- [Official Repository](https://github.com/Maplespe/DWMBlurGlass)
- [Issue Tracker](https://github.com/Maplespe/DWMBlurGlass/issues)
- [License (LGPL v3)](https://www.gnu.org/licenses/lgpl-3.0.html)

---

**Last Updated**: October 2024

**Remember**: When in doubt, build from source or ask on the official GitHub repository.
