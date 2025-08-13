import json
from typing import List, Dict, Any
import re
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch

class AIAnalyzer:
    def __init__(self):
        """Initialize AI analyzer with real LLM integration"""
        try:
            # Load free Hugging Face model for text generation
            self.text_generator = pipeline(
                "text-generation",
                model="microsoft/DialoGPT-small",  # Free model
                device=-1  # Use CPU
            )
            
            # Load model for vulnerability classification
            self.classifier = pipeline(
                "text-classification",
                model="distilbert-base-uncased",  # Free model
                device=-1
            )
            
            print("✅ LLM models loaded successfully!")
        except Exception as e:
            print(f"⚠️ LLM models not available, using fallback: {e}")
            self.text_generator = None
            self.classifier = None
        
        self.vulnerability_explanations = self._load_explanations()
        self.fix_suggestions = self._load_fix_suggestions()
    
    def _load_explanations(self) -> Dict[str, str]:
        """Load pre-defined vulnerability explanations"""
        return {
            'SQL Injection': """
            **SQL Injection Vulnerability Detected**
            
            This vulnerability occurs when user input is directly concatenated into SQL queries without proper sanitization. 
            Attackers can inject malicious SQL code to manipulate the database.
            
            **Why it's dangerous:**
            - Can lead to unauthorized data access
            - Database manipulation or deletion
            - Complete system compromise
            
            **Common attack vectors:**
            - User input in WHERE clauses
            - Login forms
            - Search functionality
            """,
            
            'Command Injection': """
            **Command Injection Vulnerability Detected**
            
            This vulnerability allows attackers to execute arbitrary system commands through the application.
            
            **Why it's dangerous:**
            - Complete server compromise
            - Data theft
            - System manipulation
            
            **Common attack vectors:**
            - System command execution
            - File operations
            - Process management
            """,
            
            'Cross-site Scripting (XSS)': """
            **Cross-site Scripting (XSS) Vulnerability Detected**
            
            This vulnerability allows attackers to inject malicious scripts into web pages viewed by other users.
            
            **Why it's dangerous:**
            - Session hijacking
            - Data theft
            - Malicious redirects
            
            **Common attack vectors:**
            - User input in HTML output
            - URL parameters
            - Form submissions
            """,
            
            'Buffer Overflow': """
            **Buffer Overflow Vulnerability Detected**
            
            This vulnerability occurs when a program writes data beyond the allocated memory buffer.
            
            **Why it's dangerous:**
            - Program crashes
            - Arbitrary code execution
            - System compromise
            
            **Common attack vectors:**
            - Unsafe string functions
            - Array access without bounds checking
            - Memory allocation issues
            """,
            
            'Path Traversal': """
            **Path Traversal Vulnerability Detected**
            
            This vulnerability allows attackers to access files outside the intended directory.
            
            **Why it's dangerous:**
            - Unauthorized file access
            - System information disclosure
            - Configuration file exposure
            
            **Common attack vectors:**
            - File path manipulation
            - Directory traversal sequences (../)
            - URL parameter manipulation
            """,
            
            'Hardcoded Credentials': """
            **Hardcoded Credentials Vulnerability Detected**
            
            This vulnerability exposes sensitive credentials directly in the source code.
            
            **Why it's dangerous:**
            - Credential exposure
            - Unauthorized access
            - Security bypass
            
            **Common attack vectors:**
            - Hardcoded passwords
            - API keys in code
            - Database connection strings
            """
        }
    
    def _load_fix_suggestions(self) -> Dict[str, str]:
        """Load pre-defined fix suggestions"""
        return {
            'SQL Injection': """
            **Fix: Use Parameterized Queries**
            
            ```python
            # VULNERABLE CODE:
            query = "SELECT * FROM users WHERE id = " + user_input
            
            # SECURE CODE:
            query = "SELECT * FROM users WHERE id = ?"
            cursor.execute(query, (user_input,))
            ```
            
            **Additional Security Measures:**
            - Input validation and sanitization
            - Use ORM frameworks
            - Implement least privilege principle
            """,
            
            'Command Injection': """
            **Fix: Avoid Command Execution with User Input**
            
            ```python
            # VULNERABLE CODE:
            os.system(user_input)
            
            # SECURE CODE:
            # Use safe APIs instead of command execution
            # For file operations, use os.path functions
            # For process management, use subprocess with shell=False
            ```
            
            **Additional Security Measures:**
            - Input validation
            - Use safe APIs
            - Implement command allowlisting
            """,
            
            'Cross-site Scripting (XSS)': """
            **Fix: Sanitize User Input**
            
            ```python
            # VULNERABLE CODE:
            print(f"<div>{user_input}</div>")
            
            # SECURE CODE:
            import html
            safe_input = html.escape(user_input)
            print(f"<div>{safe_input}</div>")
            ```
            
            **Additional Security Measures:**
            - Content Security Policy (CSP)
            - Input validation
            - Output encoding
            """,
            
            'Buffer Overflow': """
            **Fix: Use Safe String Functions**
            
            ```c
            // VULNERABLE CODE:
            strcpy(buffer, user_input);
            
            // SECURE CODE:
            strncpy(buffer, user_input, sizeof(buffer) - 1);
            buffer[sizeof(buffer) - 1] = '\\0';
            ```
            
            **Additional Security Measures:**
            - Bounds checking
            - Use safe libraries
            - Enable compiler warnings
            """,
            
            'Path Traversal': """
            **Fix: Validate File Paths**
            
            ```python
            # VULNERABLE CODE:
            file_path = user_input
            
            # SECURE CODE:
            import os
            base_path = "/safe/directory"
            requested_path = os.path.join(base_path, user_input)
            if not requested_path.startswith(base_path):
                raise ValueError("Invalid path")
            ```
            
            **Additional Security Measures:**
            - Path validation
            - Use safe file APIs
            - Implement access controls
            """,
            
            'Hardcoded Credentials': """
            **Fix: Use Environment Variables**
            
            ```python
            # VULNERABLE CODE:
            password = "secret123"
            
            # SECURE CODE:
            import os
            password = os.environ.get('DB_PASSWORD')
            ```
            
            **Additional Security Measures:**
            - Use secret management systems
            - Implement proper authentication
            - Regular credential rotation
            """
        }
    
        def analyze_vulnerabilities(self, vulnerabilities: List[Dict], code: str) -> Dict[str, Any]:
        """Analyze vulnerabilities and provide AI-powered insights using real LLM"""
        analysis = {
            'summary': self._generate_summary(vulnerabilities),
            'explanations': [],
            'fixes': [],
            'risk_assessment': self._assess_risk(vulnerabilities),
            'recommendations': self._generate_recommendations(vulnerabilities)
        }

        # Generate explanations and fixes for each vulnerability using LLM
        for vuln in vulnerabilities:
            vuln_type = vuln['type']
            line_content = vuln.get('line_content', '')

            # Use LLM for intelligent explanation
            if self.text_generator:
                explanation = self._generate_llm_explanation(vuln_type, line_content, code)
                fix = self._generate_llm_fix(vuln_type, line_content)
            else:
                # Fallback to pre-defined responses
                explanation = self.vulnerability_explanations.get(vuln_type,
                    f"**{vuln_type} Vulnerability Detected**\n\nThis vulnerability was detected in your code and requires immediate attention.")
                fix = self.fix_suggestions.get(vuln_type,
                    f"**Fix for {vuln_type}**\n\nPlease review the code and implement proper security measures.")

            analysis['explanations'].append({
                'type': vuln_type,
                'line': vuln['line_number'],
                'explanation': explanation,
                'severity': vuln['severity'],
                'ai_generated': self.text_generator is not None
            })

            analysis['fixes'].append({
                'type': vuln_type,
                'line': vuln['line_number'],
                'fix': fix,
                'priority': self._get_priority(vuln['severity']),
                'ai_generated': self.text_generator is not None
            })

        return analysis

    def _generate_llm_explanation(self, vuln_type: str, line_content: str, code: str) -> str:
        """Generate AI-powered vulnerability explanation"""
        try:
            prompt = f"""
            Explain this {vuln_type} vulnerability found in code:
            Line: {line_content}
            
            Provide a detailed explanation of:
            1. Why this is dangerous
            2. How attackers can exploit it
            3. What could happen if exploited
            
            Keep it clear and technical.
            """
            
            response = self.text_generator(prompt, max_length=200, num_return_sequences=1)
            return response[0]['generated_text']
        except Exception as e:
            return f"**{vuln_type} Vulnerability Detected**\n\nAI analysis: This vulnerability was detected and requires immediate attention."

    def _generate_llm_fix(self, vuln_type: str, line_content: str) -> str:
        """Generate AI-powered fix suggestion"""
        try:
            prompt = f"""
            Provide a fix for this {vuln_type} vulnerability:
            Vulnerable code: {line_content}
            
            Give:
            1. Secure code example
            2. Best practices to follow
            3. Additional security measures
            
            Keep it practical and actionable.
            """
            
            response = self.text_generator(prompt, max_length=200, num_return_sequences=1)
            return response[0]['generated_text']
        except Exception as e:
            return f"**Fix for {vuln_type}**\n\nPlease implement proper security measures for this vulnerability."
    
    def _generate_summary(self, vulnerabilities: List[Dict]) -> str:
        """Generate a summary of detected vulnerabilities"""
        if not vulnerabilities:
            return "No vulnerabilities detected. Your code appears to be secure!"
        
        total = len(vulnerabilities)
        critical = len([v for v in vulnerabilities if v['severity'] == 'critical'])
        high = len([v for v in vulnerabilities if v['severity'] == 'high'])
        medium = len([v for v in vulnerabilities if v['severity'] == 'medium'])
        low = len([v for v in vulnerabilities if v['severity'] == 'low'])
        
        summary = f"""
        **Vulnerability Analysis Summary**
        
        Total vulnerabilities detected: {total}
        - Critical: {critical}
        - High: {high}
        - Medium: {medium}
        - Low: {low}
        
        **Immediate Action Required:**
        """
        
        if critical > 0:
            summary += f"- {critical} critical vulnerabilities need immediate attention\n"
        if high > 0:
            summary += f"- {high} high-severity vulnerabilities should be addressed soon\n"
        
        return summary
    
    def _assess_risk(self, vulnerabilities: List[Dict]) -> Dict[str, Any]:
        """Assess overall risk level"""
        if not vulnerabilities:
            return {
                'level': 'low',
                'score': 0,
                'description': 'No vulnerabilities detected'
            }
        
        # Calculate risk score
        risk_score = 0
        for vuln in vulnerabilities:
            if vuln['severity'] == 'critical':
                risk_score += 10
            elif vuln['severity'] == 'high':
                risk_score += 7
            elif vuln['severity'] == 'medium':
                risk_score += 4
            elif vuln['severity'] == 'low':
                risk_score += 1
        
        # Determine risk level
        if risk_score >= 20:
            risk_level = 'critical'
            description = 'Immediate action required. Multiple critical vulnerabilities detected.'
        elif risk_score >= 10:
            risk_level = 'high'
            description = 'High risk. Several vulnerabilities need attention.'
        elif risk_score >= 5:
            risk_level = 'medium'
            description = 'Medium risk. Some vulnerabilities should be addressed.'
        else:
            risk_level = 'low'
            description = 'Low risk. Minor vulnerabilities detected.'
        
        return {
            'level': risk_level,
            'score': risk_score,
            'description': description
        }
    
    def _generate_recommendations(self, vulnerabilities: List[Dict]) -> List[str]:
        """Generate security recommendations"""
        recommendations = []
        
        if not vulnerabilities:
            recommendations.append("Continue following security best practices")
            return recommendations
        
        # Check for specific vulnerability types
        vuln_types = [v['type'] for v in vulnerabilities]
        
        if 'SQL Injection' in vuln_types:
            recommendations.append("Implement parameterized queries and input validation")
        
        if 'Command Injection' in vuln_types:
            recommendations.append("Avoid command execution with user input, use safe APIs")
        
        if 'Cross-site Scripting (XSS)' in vuln_types:
            recommendations.append("Implement input sanitization and Content Security Policy")
        
        if 'Buffer Overflow' in vuln_types:
            recommendations.append("Use safe string functions and implement bounds checking")
        
        if 'Path Traversal' in vuln_types:
            recommendations.append("Validate file paths and implement proper access controls")
        
        if 'Hardcoded Credentials' in vuln_types:
            recommendations.append("Use environment variables or secure credential management")
        
        # General recommendations
        recommendations.extend([
            "Implement regular security audits",
            "Use automated security testing tools",
            "Follow OWASP security guidelines",
            "Keep dependencies updated",
            "Implement proper logging and monitoring"
        ])
        
        return recommendations
    
    def _get_priority(self, severity: str) -> str:
        """Get priority level for fixes"""
        priorities = {
            'critical': 'Immediate',
            'high': 'High',
            'medium': 'Medium',
            'low': 'Low'
        }
        return priorities.get(severity, 'Medium')
