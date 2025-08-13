'use client'

import { useState } from 'react'
import { Upload, Shield, Zap, Target, AlertTriangle, CheckCircle, Settings, GitBranch } from 'lucide-react'
import FileUpload from './components/FileUpload'
import RepositoryScanner from './components/RepositoryScanner'
import VulnerabilityResults from './components/VulnerabilityResults'
import ChakraVisualization from './components/ChakraVisualization'
import LLMDashboard from './components/LLMDashboard'

export default function Home() {
  const [scanResults, setScanResults] = useState(null)
  const [isScanning, setIsScanning] = useState(false)
  const [showLLMDashboard, setShowLLMDashboard] = useState(false)
  const [scanMode, setScanMode] = useState('file') // 'file' or 'repository'
  const [llmConfig, setLlmConfig] = useState({
    provider: 'huggingface',
    apiKey: '',
    model: 'microsoft/DialoGPT-medium',
    isEnabled: true
  })

  const handleScanComplete = (results: any) => {
    setScanResults(results)
    setIsScanning(false)
  }

  const handleLLMConfigChange = (config: any) => {
    setLlmConfig(config)
    // Send config to backend
    fetch('http://127.0.0.1:8000/llm/config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(config)
    })
  }

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Background Elements */}
      <div className="absolute inset-0 -z-10">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-purple-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-float"></div>
        <div className="absolute top-0 right-1/4 w-96 h-96 bg-blue-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-float" style={{animationDelay: '1s'}}></div>
        <div className="absolute bottom-0 left-1/3 w-96 h-96 bg-pink-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-float" style={{animationDelay: '2s'}}></div>
      </div>

      {/* Header */}
      <header className="relative glass-dark text-white py-8 border-b border-white/10">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="relative">
                <div className="w-14 h-14 gradient-bg rounded-2xl flex items-center justify-center shadow-glow pulse-glow">
                  <Shield className="w-7 h-7 text-white" />
                </div>
                <div className="absolute -top-1 -right-1 w-4 h-4 bg-green-400 rounded-full border-2 border-white"></div>
              </div>
              <div>
                <h1 className="text-3xl font-bold gradient-text">SudarshanChakraAI</h1>
                <p className="text-white/80 font-medium">The Divine Weapon of Cybersecurity</p>
              </div>
            </div>
            <div className="text-right">
              <div className="flex items-center space-x-2 mb-2">
                <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                <p className="text-sm text-white/80 font-medium">AI Grand Challenge 2024</p>
              </div>
              <p className="text-xs text-white/60 mb-3">Built in 24 hours</p>
              <button
                onClick={() => setShowLLMDashboard(!showLLMDashboard)}
                className="btn-modern px-4 py-2 gradient-bg rounded-xl text-sm text-white font-medium shadow-modern hover:shadow-glow"
              >
                <Settings className="w-4 h-4 inline mr-2" />
                <span>AI Config</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16 slide-up">
          <div className="inline-flex items-center space-x-2 mb-6">
            <div className="w-2 h-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full"></div>
            <span className="text-sm font-medium text-gray-600 uppercase tracking-wider">AI-Powered Security</span>
            <div className="w-2 h-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full"></div>
          </div>
          <h2 className="text-5xl md:text-6xl font-bold mb-6">
            <span className="gradient-text">Secure Open Source Software</span>
            <br />
            <span className="text-gray-800">with Divine Precision</span>
          </h2>
          <p className="text-xl text-gray-600 mb-12 max-w-4xl mx-auto leading-relaxed">
            Analyze entire open source repositories and individual code files with our AI-powered 
            Sudarshan Chakra vulnerability detection system. Supports multiple programming languages 
            with real-time CVE/CWE mapping and dependency analysis.
          </p>
          
                               {/* Features Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
            <div className="card-modern p-8 rounded-2xl text-center group hover:scale-105 transition-all duration-300">
              <div className="w-16 h-16 gradient-bg rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-glow group-hover:shadow-glow-purple">
                <GitBranch className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-3">Repository Analysis</h3>
              <p className="text-gray-600 leading-relaxed">Scan entire open source projects from GitHub, GitLab, Bitbucket</p>
            </div>
            <div className="card-modern p-8 rounded-2xl text-center group hover:scale-105 transition-all duration-300">
              <div className="w-16 h-16 gradient-bg-alt rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-glow group-hover:shadow-glow-purple">
                <Target className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-3">Multi-Language Support</h3>
              <p className="text-gray-600 leading-relaxed">Python, JavaScript, Java, C/C++, Go, Rust, PHP and more</p>
            </div>
            <div className="card-modern p-8 rounded-2xl text-center group hover:scale-105 transition-all duration-300">
              <div className="w-16 h-16 gradient-bg rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-glow group-hover:shadow-glow-purple">
                <Zap className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-3">AI-Powered Analysis</h3>
              <p className="text-gray-600 leading-relaxed">Intelligent vulnerability detection with LLM explanations</p>
            </div>
            <div className="card-modern p-8 rounded-2xl text-center group hover:scale-105 transition-all duration-300">
              <div className="w-16 h-16 gradient-bg-alt rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-glow group-hover:shadow-glow-purple">
                <Shield className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-3">Dependency Security</h3>
              <p className="text-gray-600 leading-relaxed">CVE/CWE mapping and dependency vulnerability analysis</p>
            </div>
          </div>
        </div>

        {/* LLM Dashboard */}
        {showLLMDashboard && (
          <div className="max-w-4xl mx-auto mb-8">
            <LLMDashboard
              onConfigChange={handleLLMConfigChange}
              currentConfig={llmConfig}
            />
          </div>
        )}

        {/* Scan Mode Selection */}
        <div className="max-w-5xl mx-auto mb-12">
          <div className="card-modern p-8 rounded-3xl">
            <div className="text-center mb-8">
              <h3 className="text-2xl font-bold gradient-text mb-2">
                Choose Scan Mode
              </h3>
              <p className="text-gray-600">Select how you want to analyze your code</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <button
                onClick={() => setScanMode('file')}
                className={`btn-modern p-8 rounded-2xl text-left transition-all duration-300 ${
                  scanMode === 'file'
                    ? 'gradient-bg text-white shadow-glow scale-105'
                    : 'card-modern hover:shadow-glow'
                }`}
              >
                <div className="flex items-center space-x-4 mb-4">
                  <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${
                    scanMode === 'file' ? 'bg-white/20' : 'gradient-bg'
                  }`}>
                    <Upload className={`w-6 h-6 ${scanMode === 'file' ? 'text-white' : 'text-white'}`} />
                  </div>
                  <span className="font-bold text-xl">Single File Scan</span>
                </div>
                <p className="text-sm opacity-80 leading-relaxed">
                  Upload and analyze individual code files for vulnerabilities
                </p>
              </button>
              
              <button
                onClick={() => setScanMode('repository')}
                className={`btn-modern p-8 rounded-2xl text-left transition-all duration-300 ${
                  scanMode === 'repository'
                    ? 'gradient-bg text-white shadow-glow scale-105'
                    : 'card-modern hover:shadow-glow'
                }`}
              >
                <div className="flex items-center space-x-4 mb-4">
                  <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${
                    scanMode === 'repository' ? 'bg-white/20' : 'gradient-bg'
                  }`}>
                    <GitBranch className={`w-6 h-6 ${scanMode === 'repository' ? 'text-white' : 'text-white'}`} />
                  </div>
                  <span className="font-bold text-xl">Repository Scan</span>
                </div>
                <p className="text-sm opacity-80 leading-relaxed">
                  Analyze entire open source projects and repositories
                </p>
              </button>
            </div>
          </div>
        </div>

        {/* Scanner Section */}
        <div className="max-w-5xl mx-auto">
          {scanMode === 'file' ? (
            <FileUpload 
              onScanComplete={handleScanComplete}
              isScanning={isScanning}
              setIsScanning={setIsScanning}
            />
          ) : (
            <RepositoryScanner
              onScanComplete={handleScanComplete}
              isScanning={isScanning}
              setIsScanning={setIsScanning}
            />
          )}
        </div>

        {/* Results Section */}
        {scanResults && (
          <div className="mt-16">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Chakra Visualization */}
              <div className="card-modern p-8 rounded-2xl">
                <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
                  <div className="w-10 h-10 gradient-bg rounded-xl flex items-center justify-center mr-4 shadow-glow">
                    <Target className="w-5 h-5 text-white" />
                  </div>
                  <span className="gradient-text">Sudarshan Chakra Radar</span>
                </h3>
                <ChakraVisualization vulnerabilities={scanResults.vulnerabilities} />
              </div>

              {/* Vulnerability Results */}
              <div className="card-modern p-8 rounded-2xl">
                <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
                  <div className="w-10 h-10 bg-red-500 rounded-xl flex items-center justify-center mr-4 shadow-glow">
                    <AlertTriangle className="w-5 h-5 text-white" />
                  </div>
                  <span className="gradient-text">Vulnerability Analysis</span>
                </h3>
                <VulnerabilityResults results={scanResults} />
              </div>
            </div>
          </div>
        )}

        {/* Footer */}
        <footer className="mt-20 text-center">
          <div className="card-modern p-8 rounded-2xl">
            <div className="flex items-center justify-center space-x-2 mb-4">
              <div className="w-2 h-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full"></div>
              <span className="text-sm font-medium text-gray-600 uppercase tracking-wider">Built with ❤️</span>
              <div className="w-2 h-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full"></div>
            </div>
            <p className="text-lg font-medium text-gray-800 mb-2">AI Grand Challenge 2024</p>
            <p className="text-gray-600 mb-4">Making cybersecurity accessible to everyone</p>
            <div className="flex items-center justify-center space-x-4 text-sm text-gray-500">
              <span>Domain: sudarshanchakraai.xyz</span>
              <span>•</span>
              <span>100% Free Technology Stack</span>
            </div>
          </div>
        </footer>
      </main>
    </div>
  )
}
