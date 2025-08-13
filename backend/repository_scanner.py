import os
import json
import requests
import zipfile
import tempfile
import subprocess
from typing import Dict, List, Any, Optional
from pathlib import Path
import re
from datetime import datetime

class RepositoryScanner:
    def __init__(self):
        """Initialize repository scanner for open source software analysis"""
        self.supported_platforms = ['github', 'gitlab', 'bitbucket']
        self.ignored_dirs = [
            '.git', '.svn', '.hg', '__pycache__', 'node_modules', 
            '.venv', 'venv', 'env', 'build', 'dist', 'target',
            '.idea', '.vscode', '.DS_Store', '*.log', '*.tmp'
        ]
        self.ignored_files = [
            'package-lock.json', 'yarn.lock', 'requirements.txt',
            'Pipfile.lock', 'poetry.lock', '.gitignore', 'README.md',
            'LICENSE', 'CHANGELOG.md', '*.md', '*.txt'
        ]

    def scan_repository(self, repo_url: str, scan_type: str = 'full') -> Dict[str, Any]:
        """
        Scan an entire open source repository for vulnerabilities
        
        Args:
            repo_url: URL of the repository (GitHub, GitLab, etc.)
            scan_type: 'full' for complete scan, 'quick' for basic scan
        
        Returns:
            Dictionary containing scan results
        """
        try:
            print(f"🔍 Starting repository scan: {repo_url}")
            
            # Parse repository URL
            repo_info = self._parse_repo_url(repo_url)
            if not repo_info:
                return {"error": "Invalid repository URL"}
            
            # Download repository
            repo_path = self._download_repository(repo_info)
            if not repo_path:
                return {"error": "Failed to download repository"}
            
            # Analyze repository structure
            structure = self._analyze_structure(repo_path)
            
            # Scan for vulnerabilities based on type
            if scan_type == 'full':
                vulnerabilities = self._full_scan(repo_path, structure)
            else:
                vulnerabilities = self._quick_scan(repo_path, structure)
            
            # Analyze dependencies
            dependencies = self._analyze_dependencies(repo_path, structure)
            
            # Generate comprehensive report
            report = self._generate_report(repo_info, structure, vulnerabilities, dependencies)
            
            # Cleanup
            self._cleanup(repo_path)
            
            return report
            
        except Exception as e:
            print(f"❌ Repository scan failed: {e}")
            return {"error": f"Scan failed: {str(e)}"}

    def _parse_repo_url(self, url: str) -> Optional[Dict[str, str]]:
        """Parse repository URL to extract platform, owner, and repo name"""
        patterns = {
            'github': r'https?://github\.com/([^/]+)/([^/]+)',
            'gitlab': r'https?://gitlab\.com/([^/]+)/([^/]+)',
            'bitbucket': r'https?://bitbucket\.org/([^/]+)/([^/]+)'
        }
        
        for platform, pattern in patterns.items():
            match = re.match(pattern, url)
            if match:
                return {
                    'platform': platform,
                    'owner': match.group(1),
                    'repo': match.group(2).replace('.git', ''),
                    'url': url
                }
        
        return None

    def _download_repository(self, repo_info: Dict[str, str]) -> Optional[str]:
        """Download repository to temporary directory"""
        try:
            temp_dir = tempfile.mkdtemp()
            
            if repo_info['platform'] == 'github':
                return self._download_github_repo(repo_info, temp_dir)
            elif repo_info['platform'] == 'gitlab':
                return self._download_gitlab_repo(repo_info, temp_dir)
            else:
                return self._download_git_repo(repo_info, temp_dir)
                
        except Exception as e:
            print(f"❌ Download failed: {e}")
            return None

    def _download_github_repo(self, repo_info: Dict[str, str], temp_dir: str) -> Optional[str]:
        """Download GitHub repository"""
        try:
            # Try to download as ZIP first (faster)
            zip_url = f"https://github.com/{repo_info['owner']}/{repo_info['repo']}/archive/refs/heads/main.zip"
            response = requests.get(zip_url, timeout=30)
            
            if response.status_code == 200:
                zip_path = os.path.join(temp_dir, "repo.zip")
                with open(zip_path, 'wb') as f:
                    f.write(response.content)
                
                # Extract ZIP
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                
                # Find extracted directory
                extracted_dir = None
                for item in os.listdir(temp_dir):
                    if item.endswith('.zip'):
                        continue
                    if os.path.isdir(os.path.join(temp_dir, item)):
                        extracted_dir = os.path.join(temp_dir, item)
                        break
                
                return extracted_dir
            else:
                # Fallback to git clone
                return self._download_git_repo(repo_info, temp_dir)
                
        except Exception as e:
            print(f"GitHub download failed: {e}")
            return self._download_git_repo(repo_info, temp_dir)

    def _download_gitlab_repo(self, repo_info: Dict[str, str], temp_dir: str) -> Optional[str]:
        """Download GitLab repository"""
        try:
            # Try ZIP download
            zip_url = f"https://gitlab.com/{repo_info['owner']}/{repo_info['repo']}/-/archive/main/{repo_info['repo']}-main.zip"
            response = requests.get(zip_url, timeout=30)
            
            if response.status_code == 200:
                zip_path = os.path.join(temp_dir, "repo.zip")
                with open(zip_path, 'wb') as f:
                    f.write(response.content)
                
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                
                # Find extracted directory
                for item in os.listdir(temp_dir):
                    if item.endswith('.zip'):
                        continue
                    if os.path.isdir(os.path.join(temp_dir, item)):
                        return os.path.join(temp_dir, item)
            
            return self._download_git_repo(repo_info, temp_dir)
            
        except Exception as e:
            print(f"GitLab download failed: {e}")
            return self._download_git_repo(repo_info, temp_dir)

    def _download_git_repo(self, repo_info: Dict[str, str], temp_dir: str) -> Optional[str]:
        """Download repository using git clone"""
        try:
            repo_path = os.path.join(temp_dir, repo_info['repo'])
            subprocess.run([
                'git', 'clone', '--depth', '1', 
                repo_info['url'], repo_path
            ], check=True, capture_output=True)
            
            return repo_path
            
        except Exception as e:
            print(f"Git clone failed: {e}")
            return None

    def _analyze_structure(self, repo_path: str) -> Dict[str, Any]:
        """Analyze repository structure and identify project type"""
        structure = {
            'total_files': 0,
            'code_files': 0,
            'languages': {},
            'project_type': 'unknown',
            'files': [],
            'directories': []
        }
        
        try:
            for root, dirs, files in os.walk(repo_path):
                # Skip ignored directories
                dirs[:] = [d for d in dirs if d not in self.ignored_dirs]
                
                for file in files:
                    if self._should_ignore_file(file):
                        continue
                    
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, repo_path)
                    
                    structure['total_files'] += 1
                    
                    # Analyze file type
                    file_info = self._analyze_file(file_path, rel_path)
                    if file_info['is_code']:
                        structure['code_files'] += 1
                        lang = file_info['language']
                        structure['languages'][lang] = structure['languages'].get(lang, 0) + 1
                    
                    structure['files'].append(file_info)
            
            # Determine project type
            structure['project_type'] = self._determine_project_type(structure)
            
            return structure
            
        except Exception as e:
            print(f"Structure analysis failed: {e}")
            return structure

    def _should_ignore_file(self, filename: str) -> bool:
        """Check if file should be ignored"""
        for pattern in self.ignored_files:
            if pattern.startswith('*'):
                if filename.endswith(pattern[1:]):
                    return True
            elif filename == pattern:
                return True
        return False

    def _analyze_file(self, file_path: str, rel_path: str) -> Dict[str, Any]:
        """Analyze individual file"""
        file_info = {
            'path': rel_path,
            'size': os.path.getsize(file_path),
            'is_code': False,
            'language': 'unknown',
            'lines': 0
        }
        
        # Get file extension
        ext = os.path.splitext(file_path)[1].lower()
        
        # Language mapping
        lang_map = {
            '.py': 'python', '.js': 'javascript', '.ts': 'typescript',
            '.java': 'java', '.cpp': 'cpp', '.c': 'c', '.cs': 'csharp',
            '.php': 'php', '.rb': 'ruby', '.go': 'go', '.rs': 'rust',
            '.swift': 'swift', '.kt': 'kotlin', '.scala': 'scala',
            '.html': 'html', '.css': 'css', '.sql': 'sql',
            '.sh': 'bash', '.ps1': 'powershell', '.bat': 'batch'
        }
        
        if ext in lang_map:
            file_info['language'] = lang_map[ext]
            file_info['is_code'] = True
            
            # Count lines
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    file_info['lines'] = len(f.readlines())
            except:
                file_info['lines'] = 0
        
        return file_info

    def _determine_project_type(self, structure: Dict[str, Any]) -> str:
        """Determine the type of project based on structure"""
        languages = structure['languages']
        
        if 'python' in languages and languages['python'] > 5:
            return 'python'
        elif 'javascript' in languages and languages['javascript'] > 5:
            return 'javascript'
        elif 'java' in languages and languages['java'] > 5:
            return 'java'
        elif 'cpp' in languages or 'c' in languages:
            return 'cpp'
        elif 'php' in languages and languages['php'] > 5:
            return 'php'
        elif 'go' in languages and languages['go'] > 5:
            return 'go'
        elif 'rust' in languages and languages['rust'] > 5:
            return 'rust'
        else:
            return 'multi-language'

    def _analyze_dependencies(self, repo_path: str, structure: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze project dependencies for vulnerabilities"""
        dependencies = {
            'package_managers': [],
            'dependencies': [],
            'vulnerable_deps': [],
            'outdated_deps': []
        }
        
        project_type = structure['project_type']
        
        try:
            if project_type == 'python':
                dependencies.update(self._analyze_python_deps(repo_path))
            elif project_type == 'javascript':
                dependencies.update(self._analyze_node_deps(repo_path))
            elif project_type == 'java':
                dependencies.update(self._analyze_java_deps(repo_path))
            elif project_type == 'cpp':
                dependencies.update(self._analyze_cpp_deps(repo_path))
            elif project_type == 'go':
                dependencies.update(self._analyze_go_deps(repo_path))
            elif project_type == 'rust':
                dependencies.update(self._analyze_rust_deps(repo_path))
            
        except Exception as e:
            print(f"Dependency analysis failed: {e}")
        
        return dependencies

    def _analyze_python_deps(self, repo_path: str) -> Dict[str, Any]:
        """Analyze Python dependencies"""
        deps = {'package_managers': [], 'dependencies': []}
        
        # Check for requirements.txt
        req_file = os.path.join(repo_path, 'requirements.txt')
        if os.path.exists(req_file):
            deps['package_managers'].append('pip')
            try:
                with open(req_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            deps['dependencies'].append({
                                'name': line.split('==')[0].split('>=')[0].split('<=')[0],
                                'manager': 'pip',
                                'file': 'requirements.txt'
                            })
            except:
                pass
        
        # Check for setup.py
        setup_file = os.path.join(repo_path, 'setup.py')
        if os.path.exists(setup_file):
            deps['package_managers'].append('setuptools')
        
        # Check for pyproject.toml
        pyproject_file = os.path.join(repo_path, 'pyproject.toml')
        if os.path.exists(pyproject_file):
            deps['package_managers'].append('poetry')
        
        return deps

    def _analyze_node_deps(self, repo_path: str) -> Dict[str, Any]:
        """Analyze Node.js dependencies"""
        deps = {'package_managers': [], 'dependencies': []}
        
        # Check for package.json
        pkg_file = os.path.join(repo_path, 'package.json')
        if os.path.exists(pkg_file):
            deps['package_managers'].append('npm')
            try:
                with open(pkg_file, 'r') as f:
                    pkg_data = json.load(f)
                    for dep_type in ['dependencies', 'devDependencies']:
                        if dep_type in pkg_data:
                            for name, version in pkg_data[dep_type].items():
                                deps['dependencies'].append({
                                    'name': name,
                                    'version': version,
                                    'manager': 'npm',
                                    'type': dep_type,
                                    'file': 'package.json'
                                })
            except:
                pass
        
        # Check for yarn.lock
        yarn_file = os.path.join(repo_path, 'yarn.lock')
        if os.path.exists(yarn_file):
            deps['package_managers'].append('yarn')
        
        return deps

    def _analyze_java_deps(self, repo_path: str) -> Dict[str, Any]:
        """Analyze Java dependencies"""
        deps = {'package_managers': [], 'dependencies': []}
        
        # Check for pom.xml (Maven)
        pom_file = os.path.join(repo_path, 'pom.xml')
        if os.path.exists(pom_file):
            deps['package_managers'].append('maven')
        
        # Check for build.gradle
        gradle_file = os.path.join(repo_path, 'build.gradle')
        if os.path.exists(gradle_file):
            deps['package_managers'].append('gradle')
        
        return deps

    def _analyze_cpp_deps(self, repo_path: str) -> Dict[str, Any]:
        """Analyze C++ dependencies"""
        deps = {'package_managers': [], 'dependencies': []}
        
        # Check for CMakeLists.txt
        cmake_file = os.path.join(repo_path, 'CMakeLists.txt')
        if os.path.exists(cmake_file):
            deps['package_managers'].append('cmake')
        
        # Check for Makefile
        makefile = os.path.join(repo_path, 'Makefile')
        if os.path.exists(makefile):
            deps['package_managers'].append('make')
        
        return deps

    def _analyze_go_deps(self, repo_path: str) -> Dict[str, Any]:
        """Analyze Go dependencies"""
        deps = {'package_managers': [], 'dependencies': []}
        
        # Check for go.mod
        go_mod = os.path.join(repo_path, 'go.mod')
        if os.path.exists(go_mod):
            deps['package_managers'].append('go modules')
        
        return deps

    def _analyze_rust_deps(self, repo_path: str) -> Dict[str, Any]:
        """Analyze Rust dependencies"""
        deps = {'package_managers': [], 'dependencies': []}
        
        # Check for Cargo.toml
        cargo_file = os.path.join(repo_path, 'Cargo.toml')
        if os.path.exists(cargo_file):
            deps['package_managers'].append('cargo')
        
        return deps

    def _full_scan(self, repo_path: str, structure: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Perform full vulnerability scan of repository"""
        vulnerabilities = []
        
        # Scan each code file
        for file_info in structure['files']:
            if file_info['is_code']:
                file_path = os.path.join(repo_path, file_info['path'])
                file_vulns = self._scan_file(file_path, file_info)
                vulnerabilities.extend(file_vulns)
        
        # Add repository-level vulnerabilities
        repo_vulns = self._scan_repository_level(repo_path, structure)
        vulnerabilities.extend(repo_vulns)
        
        return vulnerabilities

    def _quick_scan(self, repo_path: str, structure: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Perform quick vulnerability scan"""
        vulnerabilities = []
        
        # Scan only main files (first 10 code files)
        code_files = [f for f in structure['files'] if f['is_code']][:10]
        
        for file_info in code_files:
            file_path = os.path.join(repo_path, file_info['path'])
            file_vulns = self._scan_file(file_path, file_info)
            vulnerabilities.extend(file_vulns)
        
        return vulnerabilities

    def _scan_file(self, file_path: str, file_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Scan individual file for vulnerabilities"""
        vulnerabilities = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Basic vulnerability patterns (this would be enhanced with proper scanner)
            vuln_patterns = [
                (r'password\s*=\s*["\'][^"\']*["\']', 'Hardcoded Password'),
                (r'api_key\s*=\s*["\'][^"\']*["\']', 'Hardcoded API Key'),
                (r'exec\s*\(', 'Code Execution'),
                (r'eval\s*\(', 'Code Evaluation'),
                (r'SELECT.*FROM.*WHERE.*\$\{', 'SQL Injection'),
                (r'innerHTML\s*=', 'XSS Vulnerability'),
            ]
            
            for line_num, line in enumerate(lines, 1):
                for pattern, vuln_type in vuln_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        vulnerabilities.append({
                            'type': vuln_type,
                            'severity': 'medium',
                            'file': file_info['path'],
                            'line': line_num,
                            'line_content': line.strip(),
                            'language': file_info['language'],
                            'description': f'{vuln_type} detected in {file_info["path"]}:{line_num}'
                        })
        
        except Exception as e:
            print(f"File scan failed for {file_path}: {e}")
        
        return vulnerabilities

    def _scan_repository_level(self, repo_path: str, structure: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Scan repository-level security issues"""
        vulnerabilities = []
        
        # Check for sensitive files
        sensitive_files = [
            '.env', '.env.local', '.env.production', 'config.json',
            'secrets.json', 'credentials.json', 'private.key'
        ]
        
        for sensitive_file in sensitive_files:
            if os.path.exists(os.path.join(repo_path, sensitive_file)):
                vulnerabilities.append({
                    'type': 'Sensitive File Exposure',
                    'severity': 'high',
                    'file': sensitive_file,
                    'line': 0,
                    'line_content': '',
                    'language': 'unknown',
                    'description': f'Sensitive file {sensitive_file} found in repository'
                })
        
        # Check for large files (potential secrets)
        for file_info in structure['files']:
            if file_info['size'] > 10 * 1024 * 1024:  # 10MB
                vulnerabilities.append({
                    'type': 'Large File',
                    'severity': 'low',
                    'file': file_info['path'],
                    'line': 0,
                    'line_content': '',
                    'language': file_info['language'],
                    'description': f'Large file detected: {file_info["path"]} ({file_info["size"]} bytes)'
                })
        
        return vulnerabilities

    def _generate_report(self, repo_info: Dict[str, str], structure: Dict[str, Any], 
                        vulnerabilities: List[Dict[str, Any]], dependencies: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive scan report"""
        return {
            'repository': {
                'url': repo_info['url'],
                'platform': repo_info['platform'],
                'owner': repo_info['owner'],
                'name': repo_info['repo']
            },
            'scan_summary': {
                'total_files': structure['total_files'],
                'code_files': structure['code_files'],
                'languages': structure['languages'],
                'project_type': structure['project_type'],
                'total_vulnerabilities': len(vulnerabilities),
                'severity_breakdown': self._get_severity_breakdown(vulnerabilities)
            },
            'vulnerabilities': vulnerabilities,
            'dependencies': dependencies,
            'recommendations': self._generate_recommendations(vulnerabilities, dependencies),
            'scan_timestamp': str(datetime.now())
        }

    def _get_severity_breakdown(self, vulnerabilities: List[Dict[str, Any]]) -> Dict[str, int]:
        """Get breakdown of vulnerabilities by severity"""
        breakdown = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        for vuln in vulnerabilities:
            severity = vuln.get('severity', 'medium')
            breakdown[severity] = breakdown.get(severity, 0) + 1
        return breakdown

    def _generate_recommendations(self, vulnerabilities: List[Dict[str, Any]], 
                                dependencies: Dict[str, Any]) -> List[str]:
        """Generate security recommendations"""
        recommendations = []
        
        if vulnerabilities:
            recommendations.append("Review and fix all detected vulnerabilities")
        
        if dependencies.get('vulnerable_deps'):
            recommendations.append("Update vulnerable dependencies")
        
        if dependencies.get('outdated_deps'):
            recommendations.append("Update outdated dependencies")
        
        if not recommendations:
            recommendations.append("No immediate security issues detected")
        
        return recommendations

    def _cleanup(self, repo_path: str):
        """Clean up temporary files"""
        try:
            import shutil
            shutil.rmtree(os.path.dirname(repo_path))
        except:
            pass

