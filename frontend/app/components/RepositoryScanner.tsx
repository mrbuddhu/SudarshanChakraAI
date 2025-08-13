'use client'

import { useState } from 'react'
import { Github, Gitlab, GitBranch, Search, AlertTriangle, CheckCircle, Clock, FileCode, Shield } from 'lucide-react'

interface RepositoryScannerProps {
  onScanComplete: (results: any) => void
  isScanning: boolean
  setIsScanning: (scanning: boolean) => void
}

export default function RepositoryScanner({ onScanComplete, isScanning, setIsScanning }: RepositoryScannerProps) {
  const [repoUrl, setRepoUrl] = useState('')
  const [scanType, setScanType] = useState('quick')
  const [error, setError] = useState('')

  const handleScan = async () => {
    if (!repoUrl.trim()) {
      setError('Please enter a repository URL')
      return
    }

    // Validate URL format
    const urlPattern = /^https?:\/\/(github\.com|gitlab\.com|bitbucket\.org)\/[^\/]+\/[^\/]+/
    if (!urlPattern.test(repoUrl)) {
      setError('Please enter a valid GitHub, GitLab, or Bitbucket repository URL')
      return
    }

    setError('')
    setIsScanning(true)

    try {
      const response = await fetch('http://127.0.0.1:8000/scan-repository', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          repo_url: repoUrl,
          scan_type: scanType
        })
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const results = await response.json()
      onScanComplete(results)
    } catch (err) {
      setError(`Scan failed: ${err instanceof Error ? err.message : 'Unknown error'}`)
    } finally {
      setIsScanning(false)
    }
  }

  const getPlatformIcon = (url: string) => {
    if (url.includes('github.com')) return <Github className="w-5 h-5" />
    if (url.includes('gitlab.com')) return <Gitlab className="w-5 h-5" />
    return <GitBranch className="w-5 h-5" />
  }

  const getScanTypeDescription = () => {
    return scanType === 'quick' 
      ? 'Fast scan of main files (recommended for initial assessment)'
      : 'Comprehensive scan of entire repository (may take longer)'
  }

  return (
    <div className="card-modern p-8 rounded-2xl">
      <div className="text-center mb-8">
        <div className="w-20 h-20 gradient-bg rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-glow">
          <Shield className="w-10 h-10 text-white" />
        </div>
        <h2 className="text-3xl font-bold gradient-text mb-3">
          Open Source Repository Scanner
        </h2>
        <p className="text-gray-600 text-lg leading-relaxed">
          Analyze entire open source projects for vulnerabilities, dependencies, and security issues
        </p>
      </div>

      {/* Repository URL Input */}
      <div className="mb-8">
        <label className="block text-sm font-medium text-gray-700 mb-3">
          Repository URL
        </label>
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
            {repoUrl && getPlatformIcon(repoUrl)}
          </div>
          <input
            type="url"
            value={repoUrl}
            onChange={(e) => setRepoUrl(e.target.value)}
            placeholder="https://github.com/username/repository"
            className="w-full pl-12 pr-4 py-4 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-300"
            disabled={isScanning}
          />
        </div>
        <p className="text-sm text-gray-500 mt-2 flex items-center">
          <div className="w-2 h-2 bg-green-400 rounded-full mr-2"></div>
          Supports GitHub, GitLab, and Bitbucket repositories
        </p>
      </div>

      {/* Scan Type Selection */}
      <div className="mb-8">
        <label className="block text-sm font-medium text-gray-700 mb-3">
          Scan Type
        </label>
        <div className="grid grid-cols-2 gap-4">
          <button
            onClick={() => setScanType('quick')}
            disabled={isScanning}
            className={`btn-modern p-6 rounded-xl border-2 transition-all duration-300 ${
              scanType === 'quick'
                ? 'gradient-bg text-white shadow-glow scale-105'
                : 'card-modern hover:shadow-glow'
            }`}
          >
            <div className="flex items-center space-x-3 mb-3">
              <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${
                scanType === 'quick' ? 'bg-white/20' : 'gradient-bg'
              }`}>
                <Clock className={`w-4 h-4 ${scanType === 'quick' ? 'text-white' : 'text-white'}`} />
              </div>
              <span className="font-bold">Quick Scan</span>
            </div>
            <p className="text-sm opacity-80">Fast analysis of main files</p>
          </button>
          
          <button
            onClick={() => setScanType('full')}
            disabled={isScanning}
            className={`btn-modern p-6 rounded-xl border-2 transition-all duration-300 ${
              scanType === 'full'
                ? 'gradient-bg text-white shadow-glow scale-105'
                : 'card-modern hover:shadow-glow'
            }`}
          >
            <div className="flex items-center space-x-3 mb-3">
              <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${
                scanType === 'full' ? 'bg-white/20' : 'gradient-bg'
              }`}>
                <FileCode className={`w-4 h-4 ${scanType === 'full' ? 'text-white' : 'text-white'}`} />
              </div>
              <span className="font-bold">Full Scan</span>
            </div>
            <p className="text-sm opacity-80">Complete repository analysis</p>
          </button>
        </div>
        <p className="text-sm text-gray-500 mt-3 flex items-center">
          <div className="w-2 h-2 bg-blue-400 rounded-full mr-2"></div>
          {getScanTypeDescription()}
        </p>
      </div>

      {/* Error Display */}
      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl">
          <div className="flex items-center space-x-2">
            <AlertTriangle className="w-5 h-5 text-red-500" />
            <span className="text-red-700 font-medium">{error}</span>
          </div>
        </div>
      )}

      {/* Scan Button */}
      <button
        onClick={handleScan}
        disabled={isScanning || !repoUrl.trim()}
        className={`btn-modern w-full py-4 px-6 rounded-xl font-bold text-lg transition-all duration-300 flex items-center justify-center space-x-3 ${
          isScanning || !repoUrl.trim()
            ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
            : 'gradient-bg text-white shadow-modern hover:shadow-glow hover:scale-[1.02]'
        }`}
      >
        {isScanning ? (
          <>
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white"></div>
            <span>Scanning Repository...</span>
          </>
        ) : (
          <>
            <Search className="w-6 h-6" />
            <span>Scan Repository</span>
          </>
        )}
      </button>

      {/* Features */}
      <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="text-center p-6 card-modern rounded-xl hover:scale-105 transition-all duration-300">
          <div className="w-12 h-12 gradient-bg rounded-xl flex items-center justify-center mx-auto mb-4 shadow-glow">
            <FileCode className="w-6 h-6 text-white" />
          </div>
          <h3 className="font-bold text-gray-800 mb-2">Multi-Language</h3>
          <p className="text-sm text-gray-600">Supports Python, JavaScript, Java, C++, Go, Rust, and more</p>
        </div>
        
        <div className="text-center p-6 card-modern rounded-xl hover:scale-105 transition-all duration-300">
          <div className="w-12 h-12 gradient-bg-alt rounded-xl flex items-center justify-center mx-auto mb-4 shadow-glow">
            <Shield className="w-6 h-6 text-white" />
          </div>
          <h3 className="font-bold text-gray-800 mb-2">Dependency Analysis</h3>
          <p className="text-sm text-gray-600">Checks for vulnerable and outdated dependencies</p>
        </div>
        
        <div className="text-center p-6 card-modern rounded-xl hover:scale-105 transition-all duration-300">
          <div className="w-12 h-12 gradient-bg rounded-xl flex items-center justify-center mx-auto mb-4 shadow-glow">
            <CheckCircle className="w-6 h-6 text-white" />
          </div>
          <h3 className="font-bold text-gray-800 mb-2">CVE Mapping</h3>
          <p className="text-sm text-gray-600">Real-time CVE/CWE database integration</p>
        </div>
      </div>

      {/* Example Repositories */}
      <div className="mt-8 p-6 card-modern rounded-xl">
        <h4 className="font-bold text-gray-800 mb-4 flex items-center">
          <div className="w-2 h-2 bg-blue-400 rounded-full mr-3"></div>
          Example Repositories to Test:
        </h4>
        <div className="space-y-3">
          <button
            onClick={() => setRepoUrl('https://github.com/facebook/react')}
            className="block w-full text-left p-3 rounded-lg hover:bg-gray-50 transition-colors text-sm text-gray-700 hover:text-gray-900"
          >
            <span className="font-medium">• Facebook React</span>
            <span className="text-gray-500 ml-2">(JavaScript)</span>
          </button>
          <button
            onClick={() => setRepoUrl('https://github.com/django/django')}
            className="block w-full text-left p-3 rounded-lg hover:bg-gray-50 transition-colors text-sm text-gray-700 hover:text-gray-900"
          >
            <span className="font-medium">• Django Framework</span>
            <span className="text-gray-500 ml-2">(Python)</span>
          </button>
          <button
            onClick={() => setRepoUrl('https://github.com/spring-projects/spring-boot')}
            className="block w-full text-left p-3 rounded-lg hover:bg-gray-50 transition-colors text-sm text-gray-700 hover:text-gray-900"
          >
            <span className="font-medium">• Spring Boot</span>
            <span className="text-gray-500 ml-2">(Java)</span>
          </button>
        </div>
      </div>
    </div>
  )
}

