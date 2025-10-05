# Security Scripts

This directory contains security tools for DWMBlurGlass to help detect malicious code and verify the integrity of the codebase.

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

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash
python3 scripts/security-scan.py
if [ $? -ne 0 ]; then
    echo "Security scan failed. Commit aborted."
    exit 1
fi
```

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

## Support

For questions or issues with the security tools:
- Open an issue on [GitHub](https://github.com/Maplespe/DWMBlurGlass/issues)
- Include the scanner output
- Describe what you were trying to do
