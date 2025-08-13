#!/usr/bin/env python3
"""
Test script for SudarshanChakraAI vulnerability scanner
"""

from vulnerability_scanner import VulnerabilityScanner
from cve_database import CVEDatabase
from ai_analyzer import AIAnalyzer

def test_vulnerability_detection():
    """Test vulnerability detection with sample vulnerable code"""
    
    # Initialize components
    scanner = VulnerabilityScanner()
    cve_db = CVEDatabase()
    ai_analyzer = AIAnalyzer()
    
    # Sample vulnerable Python code
    vulnerable_python_code = '''
import os
import sqlite3

def vulnerable_function(user_input):
    # SQL Injection vulnerability
    query = "SELECT * FROM users WHERE id = " + user_input
    cursor.execute(query)
    
    # Command Injection vulnerability
    os.system(user_input)
    
    # Hardcoded credentials
    password = "secret123"
    api_key = "sk-1234567890abcdef"
    
    return "Vulnerable code executed"

# Path traversal vulnerability
file_path = "../etc/passwd"
with open(file_path, 'r') as f:
    data = f.read()
'''
    
    print("🔍 Testing Vulnerability Detection...")
    print("=" * 50)
    
    # Scan the code
    vulnerabilities = scanner.scan_code(vulnerable_python_code, 'python')
    
    print(f"📊 Found {len(vulnerabilities)} vulnerabilities:")
    print()
    
    for i, vuln in enumerate(vulnerabilities, 1):
        print(f"{i}. {vuln['type']} (Line {vuln['line_number']})")
        print(f"   Severity: {vuln['severity']}")
        print(f"   CWE: {vuln['cwe']}")
        print(f"   Description: {vuln['description']}")
        print()
    
    # Get CVE information
    print("🔗 CVE Information:")
    print("=" * 30)
    for vuln in vulnerabilities:
        cve_info = cve_db.get_cve_info(vuln['type'])
        if cve_info:
            print(f"📋 {vuln['type']}:")
            print(f"   CVE ID: {cve_info['cve_id']}")
            print(f"   CVSS Score: {cve_info['cvss_score']}")
            print(f"   Remediation: {cve_info['remediation'][:100]}...")
            print()
    
    # AI Analysis
    print("🤖 AI Analysis:")
    print("=" * 20)
    analysis = ai_analyzer.analyze_vulnerabilities(vulnerabilities, vulnerable_python_code)
    
    print("📈 Risk Assessment:")
    risk = analysis['risk_assessment']
    print(f"   Level: {risk['level']}")
    print(f"   Score: {risk['score']}")
    print(f"   Description: {risk['description']}")
    print()
    
    print("💡 Recommendations:")
    for i, rec in enumerate(analysis['recommendations'][:5], 1):
        print(f"   {i}. {rec}")
    
    print()
    print("✅ Vulnerability detection test completed successfully!")
    
    return vulnerabilities

if __name__ == "__main__":
    test_vulnerability_detection()
