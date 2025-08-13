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
from llm_service import LLMService
from repository_scanner import RepositoryScanner
from advanced_features import AdvancedFeatures

app = FastAPI(
    title="SudarshanChakraAI",
    description="AI-Powered Vulnerability Detection System",
    version="1.0.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Frontend domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
vulnerability_scanner = VulnerabilityScanner()
cve_database = CVEDatabase()
ai_analyzer = AIAnalyzer()
llm_service = LLMService()
repository_scanner = RepositoryScanner()
advanced_features = AdvancedFeatures()

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

@app.post("/scan-repository")
async def scan_repository(repo_url: str, scan_type: str = "full"):
    """Scan entire open source repository for vulnerabilities"""
    try:
        # Validate scan type
        if scan_type not in ["full", "quick"]:
            scan_type = "full"
        
        # Scan repository
        scan_results = repository_scanner.scan_repository(repo_url, scan_type)
        
        if "error" in scan_results:
            raise HTTPException(status_code=400, detail=scan_results["error"])
        
        # Get CVE information for detected vulnerabilities
        for vuln in scan_results.get('vulnerabilities', []):
            cve_info = cve_database.get_cve_info(vuln['type'])
            vuln['cve_info'] = cve_info
        
        # AI analysis for explanations
        ai_analysis = ai_analyzer.analyze_vulnerabilities(
            scan_results.get('vulnerabilities', []), 
            f"Repository: {scan_results.get('repository', {}).get('name', 'Unknown')}"
        )
        scan_results['ai_analysis'] = ai_analysis
        
        # Add advanced features for winning
        scan_results['security_score'] = advanced_features.calculate_security_score(
            scan_results.get('vulnerabilities', []), 
            scan_results.get('dependencies', {})
        )
        
        scan_results['compliance_report'] = advanced_features.generate_compliance_report(
            scan_results.get('vulnerabilities', []),
            scan_results.get('scan_summary', {}).get('project_type', 'unknown')
        )
        
        scan_results['automated_fixes'] = advanced_features.generate_automated_fixes(
            scan_results.get('vulnerabilities', [])
        )
        
        scan_results['threat_intelligence'] = advanced_features.generate_threat_intelligence_report(
            scan_results.get('vulnerabilities', [])
        )
        
        scan_results['advanced_analytics'] = advanced_features.generate_advanced_analytics(scan_results)
        
        return scan_results
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scanning repository: {str(e)}")

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
        "ai_analyzer": "running",
        "llm_service": "running"
    }}

@app.post("/llm/config")
async def update_llm_config(config: dict):
    """Update LLM configuration"""
    try:
        llm_service.update_config(config)
        return {"status": "success", "message": "LLM configuration updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating LLM config: {str(e)}")

@app.get("/llm/config")
async def get_llm_config():
    """Get current LLM configuration"""
    return llm_service.current_config

@app.post("/llm/test")
async def test_llm_connection():
    """Test LLM connection"""
    try:
        result = llm_service.test_connection()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error testing LLM: {str(e)}")

# Advanced Features Endpoints for Winning
@app.get("/advanced/features")
async def get_advanced_features():
    """Get list of advanced features"""
    return {
        "features": advanced_features.innovation_features,
        "total_features": len(advanced_features.innovation_features)
    }

@app.post("/collaboration/session")
async def create_collaboration_session(project_id: str, users: List[str]):
    """Create real-time collaboration session"""
    try:
        session = advanced_features.create_collaboration_session(project_id, users)
        return session
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating session: {str(e)}")

@app.post("/collaboration/message")
async def add_collaboration_message(session_id: str, user: str, message: str, message_type: str = "comment"):
    """Add message to collaboration session"""
    try:
        result = advanced_features.add_collaboration_message(session_id, user, message, message_type)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding message: {str(e)}")

@app.get("/collaboration/session/{session_id}")
async def get_collaboration_session(session_id: str):
    """Get collaboration session details"""
    try:
        if session_id not in advanced_features.collaboration_sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        return advanced_features.collaboration_sessions[session_id]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting session: {str(e)}")

@app.get("/demo/winning-data")
async def get_winning_demo_data():
    """Get impressive demo data for hackathon presentation"""
    try:
        return advanced_features.create_winning_demo_data()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting demo data: {str(e)}")

@app.post("/predict/vulnerabilities")
async def predict_future_vulnerabilities(code_analysis: dict, project_history: dict = {}):
    """Predict potential future vulnerabilities"""
    try:
        predictions = advanced_features.predict_future_vulnerabilities(code_analysis, project_history)
        return {"predictions": predictions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error predicting vulnerabilities: {str(e)}")

@app.post("/detect/zero-day")
async def detect_zero_day_patterns(code_analysis: dict):
    """Detect potential zero-day vulnerability patterns"""
    try:
        patterns = advanced_features.detect_zero_day_patterns(code_analysis)
        return {"zero_day_patterns": patterns}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error detecting zero-day patterns: {str(e)}")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
