'use client'

import { useState } from 'react'
import { Upload, Shield, Zap, Target, AlertTriangle, CheckCircle } from 'lucide-react'
import FileUpload from './components/FileUpload'
import VulnerabilityResults from './components/VulnerabilityResults'
import ChakraVisualization from './components/ChakraVisualization'

export default function Home() {
  const [scanResults, setScanResults] = useState(null)
  const [isScanning, setIsScanning] = useState(false)

  const handleScanComplete = (results: any) => {
    setScanResults(results)
    setIsScanning(false)
  }

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="bg-gradient-to-r from-chakra-600 to-chakra-800 text-white py-6">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-12 h-12 bg-chakra-500 rounded-full flex items-center justify-center chakra-spin">
                <Shield className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold">SudarshanChakraAI</h1>
                <p className="text-chakra-200">The Divine Weapon of Cybersecurity</p>
              </div>
            </div>
            <div className="text-right">
              <p className="text-sm text-chakra-200">AI Grand Challenge 2024</p>
              <p className="text-xs text-chakra-300">Built in 24 hours</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-chakra-800 mb-4">
            Detect Vulnerabilities with Divine Precision
          </h2>
          <p className="text-xl text-chakra-600 mb-8 max-w-3xl mx-auto">
            Upload your code and let our AI-powered Sudarshan Chakra scan for vulnerabilities 
            across multiple programming languages with real-time CVE/CWE mapping.
          </p>
          
          {/* Features Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
            <div className="bg-white p-6 rounded-lg shadow-lg border border-chakra-200">
              <Target className="w-12 h-12 text-chakra-500 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-chakra-800 mb-2">Multi-Language Support</h3>
              <p className="text-chakra-600">Java, Python, C/C++, PHP, JavaScript and more</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-lg border border-chakra-200">
              <Zap className="w-12 h-12 text-chakra-500 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-chakra-800 mb-2">AI-Powered Analysis</h3>
              <p className="text-chakra-600">Intelligent vulnerability detection with explanations</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-lg border border-chakra-200">
              <Shield className="w-12 h-12 text-chakra-500 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-chakra-800 mb-2">CVE/CWE Mapping</h3>
              <p className="text-chakra-600">Real-time vulnerability database integration</p>
            </div>
          </div>
        </div>

        {/* Upload Section */}
        <div className="max-w-4xl mx-auto">
          <FileUpload 
            onScanComplete={handleScanComplete}
            isScanning={isScanning}
            setIsScanning={setIsScanning}
          />
        </div>

        {/* Results Section */}
        {scanResults && (
          <div className="mt-12">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Chakra Visualization */}
              <div className="bg-white p-6 rounded-lg shadow-lg border border-chakra-200">
                <h3 className="text-xl font-semibold text-chakra-800 mb-4 flex items-center">
                  <div className="w-8 h-8 bg-chakra-500 rounded-full flex items-center justify-center mr-3 chakra-spin">
                    <Target className="w-4 h-4 text-white" />
                  </div>
                  Sudarshan Chakra Radar
                </h3>
                <ChakraVisualization vulnerabilities={scanResults.vulnerabilities} />
              </div>

              {/* Vulnerability Results */}
              <div className="bg-white p-6 rounded-lg shadow-lg border border-chakra-200">
                <h3 className="text-xl font-semibold text-chakra-800 mb-4 flex items-center">
                  <AlertTriangle className="w-6 h-6 text-red-500 mr-3" />
                  Vulnerability Analysis
                </h3>
                <VulnerabilityResults results={scanResults} />
              </div>
            </div>
          </div>
        )}

        {/* Footer */}
        <footer className="mt-16 text-center text-chakra-600">
          <p>Built with ❤️ for the AI Grand Challenge - Making cybersecurity accessible to everyone</p>
          <p className="text-sm mt-2">Domain: sudarshanchakraai.xyz | 100% Free Technology Stack</p>
        </footer>
      </main>
    </div>
  )
}
