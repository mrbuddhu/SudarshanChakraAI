from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from typing import List, Dict, Any
import json
import os

# Import our modules
from vulnerability_scanner import VulnerabilityScanner
from cve_database import CVEDatabase
from ai_analyzer import AIAnalyzer

app = FastAPI(
    title="SudarshanChakraAI",
    description="AI-Powered Vulnerability Detection System",
    version="1.0.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
vulnerability_scanner = VulnerabilityScanner()
cve_database = CVEDatabase()
ai_analyzer = AIAnalyzer()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "SudarshanChakraAI - AI-Powered Vulnerability Detection",
        "version": "1.0.0",
        "status": "running"
    }

@app.post("/scan-code")
async def scan_code(file: UploadFile = File(...)):
    """Scan uploaded code file for vulnerabilities"""
    try:
        # Read file content
        content = await file.read()
        code = content.decode('utf-8')
        
        # Get file extension for language detection
        file_extension = file.filename.split('.')[-1].lower()
        
        # Scan for vulnerabilities
        vulnerabilities = vulnerability_scanner.scan_code(code, file_extension)
        
        # Get CVE information for detected vulnerabilities
        for vuln in vulnerabilities:
            cve_info = cve_database.get_cve_info(vuln['type'])
            vuln['cve_info'] = cve_info
        
        # AI analysis for explanations
        ai_analysis = ai_analyzer.analyze_vulnerabilities(vulnerabilities, code)
        
        return {
            "filename": file.filename,
            "language": file_extension,
            "vulnerabilities": vulnerabilities,
            "ai_analysis": ai_analysis,
            "total_vulnerabilities": len(vulnerabilities),
            "severity_summary": {
                "critical": len([v for v in vulnerabilities if v['severity'] == 'critical']),
                "high": len([v for v in vulnerabilities if v['severity'] == 'high']),
                "medium": len([v for v in vulnerabilities if v['severity'] == 'medium']),
                "low": len([v for v in vulnerabilities if v['severity'] == 'low'])
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scanning code: {str(e)}")

@app.get("/supported-languages")
async def get_supported_languages():
    """Get list of supported programming languages"""
    return {
        "languages": [
            {"name": "Python", "extension": "py", "supported": True},
            {"name": "Java", "extension": "java", "supported": True},
            {"name": "C++", "extension": "cpp", "supported": True},
            {"name": "C", "extension": "c", "supported": True},
            {"name": "C#", "extension": "cs", "supported": True},
            {"name": "PHP", "extension": "php", "supported": True},
            {"name": "JavaScript", "extension": "js", "supported": True}
        ]
    }

@app.get("/vulnerability-types")
async def get_vulnerability_types():
    """Get list of vulnerability types we can detect"""
    return {
        "owasp_top_10": [
            "SQL Injection",
            "Cross-Site Scripting (XSS)",
            "Broken Authentication",
            "Sensitive Data Exposure",
            "XML External Entity (XXE)",
            "Broken Access Control",
            "Security Misconfiguration",
            "Cross-Site Request Forgery (CSRF)",
            "Using Components with Known Vulnerabilities",
            "Insufficient Logging & Monitoring"
        ],
        "cwe_top_25": [
            "CWE-79: Cross-site Scripting",
            "CWE-89: SQL Injection",
            "CWE-120: Buffer Copy without Checking Size",
            "CWE-200: Information Exposure",
            "CWE-125: Out-of-bounds Read",
            "CWE-78: OS Command Injection",
            "CWE-787: Out-of-bounds Write",
            "CWE-22: Path Traversal",
            "CWE-352: Cross-Site Request Forgery",
            "CWE-434: Unrestricted Upload of File"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "components": {
        "vulnerability_scanner": "running",
        "cve_database": "running",
        "ai_analyzer": "running"
    }}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
