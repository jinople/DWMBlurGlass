#!/usr/bin/env python3
"""
Security Scanner for DWMBlurGlass
Detects potentially malicious code patterns in the codebase
"""

import os
import re
import sys
import hashlib
from pathlib import Path
from typing import List, Dict, Tuple

class SecurityScanner:
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.issues = []
        self.warnings = []
        
        # Known safe DLL injection patterns (expected for DWM customization)
        self.expected_patterns = [
            'LoadLibraryW',
            'FreeLibrary',
            'CreateRemoteThread',
            'WriteProcessMemory',
            'VirtualAllocEx',
            'GetProcAddress'
        ]
        
        # Suspicious patterns that should NOT be present
        self.malicious_patterns = {
            'network': [
                (r'WinHttpOpen', 'Unexpected HTTP network call'),
                (r'InternetOpenA?', 'Unexpected Internet API usage'),
                (r'URLDownloadToFile', 'Unexpected file download'),
                (r'HttpSendRequest', 'Unexpected HTTP request'),
                (r'\bsocket\s*\(', 'Raw socket creation'),
                (r'WSAStartup', 'Windows socket initialization'),
            ],
            'data_exfiltration': [
                (r'GetClipboardData', 'Clipboard data access'),
                (r'GetKeyboardState', 'Keyboard state access'),
                (r'GetAsyncKeyState', 'Keyboard monitoring (keylogger)'),
                (r'SetWindowsHookEx.*WH_KEYBOARD', 'Keyboard hook (keylogger)'),
                (r'SHGetFolderPath.*CSIDL_PERSONAL', 'Access to user documents'),
            ],
            'persistence': [
                (r'RegSetValueEx.*\\Software\\Microsoft\\Windows\\CurrentVersion\\Run', 'Startup registry key'),
                (r'CreateService', 'Service creation'),
                (r'StartService', 'Service starting'),
                (r'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run', 'Startup registry'),
            ],
            'obfuscation': [
                (r'CallWindowProc\s*\(.*\bShellExecute', 'Indirect function call'),
                (r'\\x[0-9a-fA-F]{2}\\x[0-9a-fA-F]{2}\\x[0-9a-fA-F]{2}\\x[0-9a-fA-F]{2}\\x[0-9a-fA-F]{2}', 'Embedded shellcode pattern (5+ consecutive hex bytes)'),
                (r'DecryptStringW?', 'String decryption (potential obfuscation)'),
                (r'VirtualAlloc.*PAGE_EXECUTE_READWRITE', 'Executable memory allocation'),
            ],
            'process_manipulation': [
                (r'CreateProcess.*DETACHED_PROCESS', 'Detached process creation'),
                (r'NtSetContextThread', 'Thread context manipulation'),
                (r'ZwSetContextThread', 'Thread context manipulation'),
            ],
            'file_operations': [
                (r'DeleteFile.*\\Windows\\System32', 'System file deletion'),
                (r'MoveFile.*\\Windows\\System32', 'System file move'),
                (r'CopyFile.*\\Windows\\System32', 'System file copy to system dir'),
                (r'SetFileAttributes.*FILE_ATTRIBUTE_HIDDEN', 'File hiding'),
            ]
        }
        
        # Expected legitimate operations for DWM customization
        self.legitimate_operations = [
            'OpenProcess',  # Needed to inject into dwm.exe
            'LoadLibraryW',  # Needed to load the extension DLL
            'GetModuleHandle',  # Standard Windows API
            'GetProcAddress',  # Standard Windows API
            'CreateRemoteThread',  # Needed for DLL injection
            'VirtualAllocEx',  # Needed for DLL injection
            'WriteProcessMemory',  # Needed for DLL injection
        ]
    
    def scan_file(self, filepath: Path) -> List[Dict]:
        """Scan a single file for malicious patterns"""
        file_issues = []
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                line_number = 0
                
                for line in content.split('\n'):
                    line_number += 1
                    
                    # Check for malicious patterns
                    for category, patterns in self.malicious_patterns.items():
                        for pattern, description in patterns:
                            if re.search(pattern, line, re.IGNORECASE):
                                file_issues.append({
                                    'file': str(filepath.relative_to(self.root_dir)),
                                    'line': line_number,
                                    'category': category,
                                    'pattern': pattern,
                                    'description': description,
                                    'content': line.strip()[:100]
                                })
        except Exception as e:
            self.warnings.append(f"Error scanning {filepath}: {e}")
        
        return file_issues
    
    def scan_directory(self) -> None:
        """Scan all source files in the directory"""
        extensions = ['.cpp', '.c', '.h', '.hpp', '.cc']
        
        # Skip certain directories
        skip_dirs = {'.git', 'bin', 'obj', 'Debug', 'Release', 'x64', 'x86', 
                    'packages', 'node_modules', '.vs', '.vscode'}
        
        for ext in extensions:
            for filepath in self.root_dir.rglob(f'*{ext}'):
                # Skip if in excluded directory
                if any(skip_dir in filepath.parts for skip_dir in skip_dirs):
                    continue
                
                issues = self.scan_file(filepath)
                self.issues.extend(issues)
    
    def check_binary_artifacts(self) -> List[Dict]:
        """Check for unexpected binary files"""
        suspicious_binaries = []
        binary_extensions = ['.exe', '.dll', '.sys', '.bat', '.cmd', '.vbs', '.ps1']
        
        # Expected binary locations
        expected_locations = ['bin', 'Release', 'Debug', 'x64', 'x86']
        
        for ext in binary_extensions:
            for filepath in self.root_dir.rglob(f'*{ext}'):
                # Check if in expected location
                if not any(loc in filepath.parts for loc in expected_locations):
                    suspicious_binaries.append({
                        'file': str(filepath.relative_to(self.root_dir)),
                        'reason': 'Binary file in unexpected location'
                    })
        
        return suspicious_binaries
    
    def generate_report(self) -> str:
        """Generate a security scan report"""
        report = []
        report.append("=" * 80)
        report.append("DWMBlurGlass Security Scan Report")
        report.append("=" * 80)
        report.append("")
        
        # Group issues by category
        if self.issues:
            report.append(f"⚠️  Found {len(self.issues)} potential security issue(s):")
            report.append("")
            
            by_category = {}
            for issue in self.issues:
                category = issue['category']
                if category not in by_category:
                    by_category[category] = []
                by_category[category].append(issue)
            
            for category, issues in by_category.items():
                report.append(f"Category: {category.upper()}")
                report.append("-" * 80)
                for issue in issues:
                    report.append(f"  File: {issue['file']}:{issue['line']}")
                    report.append(f"  Issue: {issue['description']}")
                    report.append(f"  Pattern: {issue['pattern']}")
                    report.append(f"  Code: {issue['content']}")
                    report.append("")
        else:
            report.append("✓ No suspicious patterns detected")
            report.append("")
        
        # Check for unexpected binaries
        suspicious_bins = self.check_binary_artifacts()
        if suspicious_bins:
            report.append(f"⚠️  Found {len(suspicious_bins)} suspicious binary file(s):")
            for binary in suspicious_bins:
                report.append(f"  {binary['file']}: {binary['reason']}")
            report.append("")
        
        # Warnings
        if self.warnings:
            report.append("Warnings:")
            for warning in self.warnings:
                report.append(f"  ⚠ {warning}")
            report.append("")
        
        report.append("=" * 80)
        report.append("Scan completed")
        report.append("=" * 80)
        
        return "\n".join(report)

def main():
    if len(sys.argv) > 1:
        root_dir = sys.argv[1]
    else:
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    scanner = SecurityScanner(root_dir)
    print(f"Scanning directory: {root_dir}")
    print("This may take a moment...\n")
    
    scanner.scan_directory()
    report = scanner.generate_report()
    print(report)
    
    # Exit with error code if issues found
    if scanner.issues:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == '__main__':
    main()
