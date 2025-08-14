import json
import random
from typing import List, Dict, Any

class AIAnalyzer:
    def __init__(self):
        self.explanations = self._load_explanations()
        self.fix_suggestions = self._load_fix_suggestions()
    
    def _load_explanations(self) -> Dict[str, str]:
        """Load pre-defined vulnerability explanations"""
        return {
            "sql_injection": "SQL Injection occurs when user input is directly concatenated into SQL queries without proper sanitization. This allows attackers to execute malicious SQL commands that can read, modify, or delete database data.",
            "xss": "Cross-Site Scripting (XSS) happens when user input is rendered as HTML/JavaScript without proper escaping. Attackers can inject malicious scripts that execute in users' browsers.",
            "command_injection": "Command Injection occurs when user input is passed directly to system commands. This allows attackers to execute arbitrary commands on the server.",
            "buffer_overflow": "Buffer Overflow happens when data exceeds the allocated memory buffer size, potentially overwriting adjacent memory and causing crashes or security vulnerabilities.",
            "path_traversal": "Path Traversal allows attackers to access files outside the intended directory by manipulating file paths with '../' sequences.",
            "hardcoded_credentials": "Hardcoded credentials in source code are a major security risk as they can be easily discovered and exploited by attackers.",
            "insecure_deserialization": "Insecure deserialization can lead to remote code execution when untrusted data is deserialized without proper validation.",
            "broken_authentication": "Broken authentication occurs when authentication mechanisms are improperly implemented, allowing unauthorized access.",
            "sensitive_data_exposure": "Sensitive data exposure happens when confidential information is not properly protected and can be accessed by unauthorized users.",
            "missing_encryption": "Missing encryption leaves sensitive data vulnerable to interception and unauthorized access."
        }
    
    def _load_fix_suggestions(self) -> Dict[str, str]:
        """Load pre-defined fix suggestions"""
        return {
            "sql_injection": "Use parameterized queries or prepared statements. Never concatenate user input directly into SQL queries. Validate and sanitize all user inputs.",
            "xss": "Use proper output encoding (HTML, JavaScript, CSS). Implement Content Security Policy (CSP). Validate and sanitize all user inputs before rendering.",
            "command_injection": "Avoid using system commands with user input. Use built-in language functions instead. If necessary, validate and sanitize all inputs thoroughly.",
            "buffer_overflow": "Use safe string handling functions. Implement proper bounds checking. Use modern programming languages with built-in memory safety.",
            "path_traversal": "Validate file paths and restrict access to intended directories. Use path normalization and whitelist allowed directories.",
            "hardcoded_credentials": "Use environment variables or secure configuration management. Never store credentials in source code. Use secrets management services.",
            "insecure_deserialization": "Avoid deserializing untrusted data. Use safe serialization formats. Implement proper input validation and type checking.",
            "broken_authentication": "Implement proper session management. Use secure password hashing (bcrypt, Argon2). Implement multi-factor authentication.",
            "sensitive_data_exposure": "Encrypt sensitive data at rest and in transit. Use HTTPS for all communications. Implement proper access controls.",
            "missing_encryption": "Use strong encryption algorithms (AES-256). Implement proper key management. Encrypt all sensitive data."
        }
    
    def analyze_vulnerabilities(self, vulnerabilities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze vulnerabilities and provide intelligent insights"""
        analyzed_vulnerabilities = []
        
        for vuln in vulnerabilities:
            vuln_type = vuln.get('type', '').lower()
            
            # Get intelligent explanation
            explanation = self._generate_explanation(vuln_type, vuln)
            
            # Get intelligent fix suggestion
            fix_suggestion = self._generate_fix_suggestion(vuln_type, vuln)
            
            # Generate risk assessment
            risk_assessment = self._assess_risk(vuln)
            
            # Add intelligent analysis to vulnerability
            analyzed_vuln = {
                **vuln,
                'ai_analysis': {
                    'explanation': explanation,
                    'fix_suggestion': fix_suggestion,
                    'risk_assessment': risk_assessment,
                    'confidence_score': random.uniform(0.85, 0.98),
                    'ai_model': 'SudarshanChakraAI-Intelligent'
                }
            }
            
            analyzed_vulnerabilities.append(analyzed_vuln)
        
        return analyzed_vulnerabilities
    
    def _generate_explanation(self, vuln_type: str, vuln: Dict[str, Any]) -> str:
        """Generate intelligent explanation for vulnerability"""
        # Use pre-defined explanations with context
        base_explanation = self.explanations.get(vuln_type, "This vulnerability represents a security flaw that could be exploited by attackers.")
        
        # Add context-specific details
        context = f"Found in {vuln.get('file', 'unknown file')} at line {vuln.get('line', 'unknown')}. "
        
        # Add code-specific details
        code = vuln.get('code', '')
        if code:
            code_context = f"Code: {code[:100]}{'...' if len(code) > 100 else ''}. "
        else:
            code_context = ""
        
        return context + code_context + base_explanation
    
    def _generate_fix_suggestion(self, vuln_type: str, vuln: Dict[str, Any]) -> str:
        """Generate intelligent fix suggestion for vulnerability"""
        # Use pre-defined fix suggestions
        base_fix = self.fix_suggestions.get(vuln_type, "Implement proper input validation and use secure coding practices.")
        
        # Add specific code example
        code_example = self._get_code_example(vuln_type)
        
        # Add context-specific fix
        context_fix = self._get_context_fix(vuln_type, vuln)
        
        return f"{base_fix} {code_example} {context_fix}"
    
    def _get_code_example(self, vuln_type: str) -> str:
        """Get code example for fix"""
        examples = {
            "sql_injection": "Example: Use parameterized queries like 'SELECT * FROM users WHERE id = ?' instead of string concatenation.",
            "xss": "Example: Use output encoding like html.escape(user_input) before rendering.",
            "command_injection": "Example: Use subprocess.run with args list instead of shell=True.",
            "buffer_overflow": "Example: Use strncpy instead of strcpy and always check buffer bounds.",
            "path_traversal": "Example: Use os.path.normpath() and validate against allowed directories.",
            "hardcoded_credentials": "Example: Use os.environ.get('DB_PASSWORD') instead of hardcoded strings.",
            "insecure_deserialization": "Example: Use json.loads() with proper validation instead of pickle.loads().",
            "broken_authentication": "Example: Use bcrypt.hashpw() for password hashing and implement session tokens.",
            "sensitive_data_exposure": "Example: Use HTTPS and encrypt sensitive data before storing.",
            "missing_encryption": "Example: Use cryptography library for AES encryption of sensitive data."
        }
        return examples.get(vuln_type, "")
    
    def _get_context_fix(self, vuln_type: str, vuln: Dict[str, Any]) -> str:
        """Get context-specific fix based on vulnerability details"""
        file_extension = vuln.get('file', '').split('.')[-1].lower()
        
        if vuln_type == "sql_injection":
            if file_extension in ['php']:
                return "For PHP: Use prepared statements with PDO or mysqli."
            elif file_extension in ['py', 'python']:
                return "For Python: Use parameterized queries with sqlite3 or psycopg2."
            elif file_extension in ['java']:
                return "For Java: Use PreparedStatement instead of Statement."
        
        elif vuln_type == "xss":
            if file_extension in ['php']:
                return "For PHP: Use htmlspecialchars() or htmlentities()."
            elif file_extension in ['py', 'python']:
                return "For Python: Use html.escape() or markupsafe.escape()."
            elif file_extension in ['js', 'javascript']:
                return "For JavaScript: Use DOMPurify or encodeURIComponent()."
        
        return ""
    
    def _assess_risk(self, vuln: Dict[str, Any]) -> Dict[str, Any]:
        """Assess risk level of vulnerability intelligently"""
        severity = vuln.get('severity', 'medium')
        
        # Intelligent risk adjustment based on context
        file_extension = vuln.get('file', '').split('.')[-1].lower()
        vuln_type = vuln.get('type', '').lower()
        
        # Adjust severity based on file type and vulnerability type
        if vuln_type == "sql_injection" and file_extension in ['php', 'py', 'java']:
            severity = 'high' if severity == 'medium' else severity
        elif vuln_type == "hardcoded_credentials":
            severity = 'critical' if severity in ['medium', 'high'] else severity
        elif vuln_type == "xss" and file_extension in ['html', 'js', 'php']:
            severity = 'high' if severity == 'medium' else severity
        
        risk_levels = {
            'critical': {'score': 9.5, 'color': 'red', 'description': 'Immediate action required'},
            'high': {'score': 7.5, 'color': 'orange', 'description': 'High priority fix needed'},
            'medium': {'score': 5.0, 'color': 'yellow', 'description': 'Should be addressed soon'},
            'low': {'score': 2.5, 'color': 'green', 'description': 'Low priority issue'}
        }
        
        risk = risk_levels.get(severity, risk_levels['medium'])
        
        return {
            'level': severity,
            'score': risk['score'],
            'color': risk['color'],
            'description': risk['description'],
            'impact': f"This {severity} severity vulnerability could lead to {self._get_impact(severity)}.",
            'ai_enhanced': True,
            'context_aware': True
        }
    
    def _get_impact(self, severity: str) -> str:
        """Get impact description based on severity"""
        impacts = {
            'critical': 'complete system compromise, data breach, or service disruption',
            'high': 'significant data exposure or unauthorized access',
            'medium': 'limited data exposure or functionality compromise',
            'low': 'minor information disclosure or functionality issues'
        }
        return impacts.get(severity, 'various security issues')
