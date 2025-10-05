# Security Scripts

This directory contains security tools for DWMBlurGlass to help detect malicious code and verify the integrity of the codebase.

## Tools

### 1. Security Scanner (`security-scan.py`)
Scans source code for malicious patterns.

### 2. Download Verifier (`verify-download.py`)
Verifies downloaded executables for authenticity.

### 3. Pre-commit Hook (`pre-commit-hook.sh`)
Git hook that runs security scan before each commit.

---

## Security Scanner (`security-scan.py`)

A Python script that scans the DWMBlurGlass source code for potentially malicious patterns.

### Usage

```bash
# Scan the entire repository
python3 security-scan.py

# Scan a specific directory
python3 security-scan.py /path/to/directory
```

### What It Detects

The scanner checks for suspicious patterns that could indicate malicious code:

#### Network Operations
- HTTP/Internet API calls
- Socket operations
- File downloads
- Network connections

#### Data Exfiltration
- Clipboard data access
- Keyboard state monitoring
- Keylogger hooks
- Access to user documents

#### Persistence Mechanisms
- Startup registry keys
- Service creation
- Auto-start modifications

#### Code Obfuscation
- Memory protection changes
- Encrypted strings
- Shellcode patterns
- Hidden execution

#### Process Manipulation
- Thread context manipulation
- Detached process creation
- Unexpected process access

#### File Operations
- System file modifications
- Hidden file creation
- Suspicious file operations

### Expected Behavior

DWMBlurGlass legitimately uses:
- **DLL injection** - Required for DWM customization
- **Function hooking** - Via MinHook library
- **Process access** - Only to `dwm.exe`
- **Registry access** - For user preferences
- **Scheduled tasks** - Optional auto-start

These patterns are **excluded** from the scanner as they are expected and safe.

### Output

The scanner generates a report with:
- Number of issues found
- Issues grouped by category
- File location and line numbers
- Code snippets showing the issue

Example output:
```
================================================================================
DWMBlurGlass Security Scan Report
================================================================================

✓ No suspicious patterns detected

================================================================================
Scan completed
================================================================================
```

### Exit Codes

- `0` - No issues found
- `1` - Suspicious patterns detected

### Continuous Integration

This scanner runs automatically via GitHub Actions on:
- Every push to master/dev branches
- Every pull request
- Weekly schedule (Mondays at 00:00 UTC)
- Manual workflow dispatch

### False Positives

If legitimate code triggers a warning:

1. Review the flagged code carefully
2. Verify it's necessary for the feature
3. Add appropriate context in comments
4. Consider refining the scanner pattern

### Customization

To modify detection patterns, edit the `malicious_patterns` dictionary in `security-scan.py`:

```python
self.malicious_patterns = {
    'category_name': [
        (r'pattern_regex', 'Description of what it detects'),
    ],
}
```

## Integrating with Your Workflow

### Pre-commit Hook

To automatically run security scans before each commit:

```bash
# Install the pre-commit hook
cp scripts/pre-commit-hook.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

The hook will run `security-scan.py` and prevent commits if issues are detected.

### Pre-release Check

Before creating a release:

```bash
# Run full security scan
python3 scripts/security-scan.py

# Check for unexpected files
find . -name "*.exe" -o -name "*.dll" | grep -v -E "(bin|Debug|Release|x64|x86)"

# Verify no credentials in code
git grep -i -E "(password|api_key|secret|token)" -- "*.cpp" "*.h"
```

## Contributing

To improve the security scanner:

1. Test against known malicious patterns
2. Reduce false positives
3. Add new detection categories
4. Improve performance for large codebases

## License

This security scanner is part of DWMBlurGlass and follows the same LGPL v3 license.

## Download Verifier (`verify-download.py`)

A tool to help users verify downloaded DWMBlurGlass executables.

### Usage

```bash
# Verify a downloaded executable
python3 verify-download.py DWMBlurGlass.exe

# Or with full path
python3 verify-download.py C:\Downloads\DWMBlurGlass.exe
```

### What It Checks

1. **File Size** - Verifies reasonable file size (under 50MB)
2. **SHA-256 Hash** - Calculates hash for comparison with official releases
3. **Digital Signature** - Checks code signing (Windows only)

### Output

The tool provides:
- File hash to compare with official releases
- Digital signature status
- File size validation
- Warnings and recommendations

### Example Usage

```bash
$ python3 verify-download.py DWMBlurGlass.exe

================================================================================
DWMBlurGlass Download Verification Tool
================================================================================

📁 Verifying: DWMBlurGlass.exe
--------------------------------------------------------------------------------
ℹ️  File size: 2.45 MB

🔐 Calculating SHA-256 hash...
   Hash: abc123...

   Compare this hash with:
   1. Official GitHub release notes
   2. Hash posted by official maintainers
   3. Hash from a trusted source

🔏 Checking digital signature...
✅ Digital signature: Valid

⚠️  IMPORTANT REMINDERS:
   • Only download from official sources
   • Never download from file sharing sites
   • If in doubt, build from source code
```

## Support

For questions or issues with the security tools:
- Open an issue on [GitHub](https://github.com/Maplespe/DWMBlurGlass/issues)
- Include the scanner output
- Describe what you were trying to do
