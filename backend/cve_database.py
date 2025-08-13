import sqlite3
import json
from typing import Dict, Any, Optional

class CVEDatabase:
    def __init__(self):
        """Initialize CVE database with common vulnerabilities"""
        self.db_path = "cve_database.db"
        self.init_database()
    
    def init_database(self):
        """Initialize the SQLite database with CVE data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create CVE table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cve_data (
                id INTEGER PRIMARY KEY,
                cve_id TEXT UNIQUE,
                cwe_id TEXT,
                vulnerability_type TEXT,
                description TEXT,
                severity TEXT,
                cvss_score REAL,
                remediation TEXT,
                ref_links TEXT
            )
        ''')
        
        # Insert sample CVE data
        cve_data = [
            ('CVE-2021-44228', 'CWE-502', 'SQL Injection', 
             'SQL injection vulnerability in database queries', 'critical', 9.8,
             'Use parameterized queries and input validation',
             'https://nvd.nist.gov/vuln/detail/CVE-2021-44228'),
            
            ('CWE-89', 'CWE-89', 'SQL Injection',
             'Improper Neutralization of Special Elements used in an SQL Command',
             'critical', 9.8,
             'Use prepared statements and parameterized queries',
             'https://cwe.mitre.org/data/definitions/89.html'),
            
            ('CWE-78', 'CWE-78', 'Command Injection',
             'Improper Neutralization of Special Elements used in an OS Command',
             'critical', 9.8,
             'Avoid command execution with user input, use safe APIs',
             'https://cwe.mitre.org/data/definitions/78.html'),
            
            ('CWE-79', 'CWE-79', 'Cross-site Scripting (XSS)',
             'Improper Neutralization of Input During Web Page Generation',
             'high', 6.1,
             'Validate and sanitize all user inputs, use CSP headers',
             'https://cwe.mitre.org/data/definitions/79.html'),
            
            ('CWE-120', 'CWE-120', 'Buffer Overflow',
             'Buffer Copy without Checking Size of Input',
             'critical', 9.8,
             'Use safe string functions and bounds checking',
             'https://cwe.mitre.org/data/definitions/120.html'),
            
            ('CWE-22', 'CWE-22', 'Path Traversal',
             'Improper Limitation of a Pathname to a Restricted Directory',
             'high', 7.5,
             'Validate file paths and use safe file operations',
             'https://cwe.mitre.org/data/definitions/22.html'),
            
            ('CWE-259', 'CWE-259', 'Hardcoded Credentials',
             'Use of Hard-coded Password',
             'high', 7.5,
             'Use environment variables or secure credential management',
             'https://cwe.mitre.org/data/definitions/259.html'),
            
            ('CWE-190', 'CWE-190', 'Integer Overflow',
             'Integer Overflow or Wraparound',
             'high', 7.5,
             'Use safe arithmetic operations and bounds checking',
             'https://cwe.mitre.org/data/definitions/190.html'),
            
            ('CWE-416', 'CWE-416', 'Use After Free',
             'Use After Free',
             'critical', 9.8,
             'Properly manage memory allocation and deallocation',
             'https://cwe.mitre.org/data/definitions/416.html'),
            
            ('CWE-434', 'CWE-434', 'Unrestricted Upload',
             'Unrestricted Upload of File with Dangerous Type',
             'high', 7.5,
             'Validate file types and implement upload restrictions',
             'https://cwe.mitre.org/data/definitions/434.html'),
            
            ('CWE-352', 'CWE-352', 'Cross-Site Request Forgery',
             'Cross-Site Request Forgery (CSRF)',
             'medium', 6.5,
             'Implement CSRF tokens and validate request origin',
             'https://cwe.mitre.org/data/definitions/352.html'),
            
            ('CWE-200', 'CWE-200', 'Information Exposure',
             'Exposure of Sensitive Information to an Unauthorized Actor',
             'medium', 5.3,
             'Implement proper access controls and data protection',
             'https://cwe.mitre.org/data/definitions/200.html'),
            
            ('CWE-125', 'CWE-125', 'Out-of-bounds Read',
             'Out-of-bounds Read',
             'high', 7.5,
             'Implement proper bounds checking for array access',
             'https://cwe.mitre.org/data/definitions/125.html'),
            
            ('CWE-787', 'CWE-787', 'Out-of-bounds Write',
             'Out-of-bounds Write',
             'critical', 9.8,
             'Implement proper bounds checking for array writes',
             'https://cwe.mitre.org/data/definitions/787.html')
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO cve_data 
            (cve_id, cwe_id, vulnerability_type, description, severity, cvss_score, remediation, ref_links)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', cve_data)
        
        conn.commit()
        conn.close()
    
    def get_cve_info(self, vulnerability_type: str) -> Optional[Dict[str, Any]]:
        """Get CVE information for a vulnerability type"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT cve_id, cwe_id, vulnerability_type, description, severity, 
                   cvss_score, remediation, ref_links
            FROM cve_data 
            WHERE vulnerability_type = ?
        ''', (vulnerability_type,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'cve_id': result[0],
                'cwe_id': result[1],
                'vulnerability_type': result[2],
                'description': result[3],
                'severity': result[4],
                'cvss_score': result[5],
                'remediation': result[6],
                'ref_links': result[7]
            }
        
        return None
    
    def get_all_cves(self) -> list:
        """Get all CVE entries"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM cve_data')
        results = cursor.fetchall()
        conn.close()
        
        cves = []
        for result in results:
            cves.append({
                'id': result[0],
                'cve_id': result[1],
                'cwe_id': result[2],
                'vulnerability_type': result[3],
                'description': result[4],
                'severity': result[5],
                'cvss_score': result[6],
                'remediation': result[7],
                'references': result[8]
            })
        
        return cves
    
    def search_cve_by_cwe(self, cwe_id: str) -> list:
        """Search CVE by CWE ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM cve_data WHERE cwe_id = ?', (cwe_id,))
        results = cursor.fetchall()
        conn.close()
        
        cves = []
        for result in results:
            cves.append({
                'id': result[0],
                'cve_id': result[1],
                'cwe_id': result[2],
                'vulnerability_type': result[3],
                'description': result[4],
                'severity': result[5],
                'cvss_score': result[6],
                'remediation': result[7],
                'references': result[8]
            })
        
        return cves
    
    def get_severity_stats(self) -> Dict[str, int]:
        """Get vulnerability statistics by severity"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT severity, COUNT(*) FROM cve_data GROUP BY severity')
        results = cursor.fetchall()
        conn.close()
        
        stats = {}
        for result in results:
            stats[result[0]] = result[1]
        
        return stats
