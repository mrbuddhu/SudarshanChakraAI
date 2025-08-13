'use client'

import { useState, useEffect } from 'react'
import { 
  Trophy, Shield, Users, Brain, TrendingUp, Target, 
  Zap, CheckCircle, AlertTriangle, Star, Award, Rocket
} from 'lucide-react'

interface AdvancedFeaturesProps {
  scanResults?: any
}

export default function AdvancedFeatures({ scanResults }: AdvancedFeaturesProps) {
  const [winningData, setWinningData] = useState<any>(null)
  const [activeTab, setActiveTab] = useState('security-score')

  useEffect(() => {
    // Fetch winning demo data
         fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'}/demo/winning-data`)
      .then(res => res.json())
      .then(data => setWinningData(data))
      .catch(err => console.error('Error fetching demo data:', err))
  }, [])

  const getSecurityScoreColor = (score: number) => {
    if (score >= 90) return 'text-green-600'
    if (score >= 80) return 'text-blue-600'
    if (score >= 70) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getSecurityScoreBg = (score: number) => {
    if (score >= 90) return 'bg-green-100'
    if (score >= 80) return 'bg-blue-100'
    if (score >= 70) return 'bg-yellow-100'
    return 'bg-red-100'
  }

  if (!scanResults && !winningData) {
    return (
      <div className="card-modern p-8 rounded-2xl text-center">
        <div className="w-16 h-16 gradient-bg rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-glow">
          <Trophy className="w-8 h-8 text-white" />
        </div>
        <h3 className="text-2xl font-bold gradient-text mb-2">Advanced Features</h3>
        <p className="text-gray-600">Loading advanced security features...</p>
      </div>
    )
  }

  return (
    <div className="card-modern p-8 rounded-2xl">
      {/* Header */}
      <div className="text-center mb-8">
        <div className="w-16 h-16 gradient-bg rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-glow">
          <Trophy className="w-8 h-8 text-white" />
        </div>
        <h2 className="text-3xl font-bold gradient-text mb-3">
          Advanced Security Features
        </h2>
        <p className="text-gray-600 text-lg">
          Cutting-edge AI-powered security analysis for maximum protection
        </p>
      </div>

      {/* Tabs */}
      <div className="flex space-x-1 mb-8 bg-gray-100 p-1 rounded-xl">
        {[
          { id: 'security-score', label: 'Security Score', icon: Shield },
          { id: 'compliance', label: 'Compliance', icon: CheckCircle },
          { id: 'automated-fixes', label: 'Auto Fixes', icon: Zap },
          { id: 'threat-intel', label: 'Threat Intel', icon: Target },
          { id: 'analytics', label: 'Analytics', icon: TrendingUp },
          { id: 'innovation', label: 'Innovation', icon: Rocket }
        ].map((tab) => {
          const Icon = tab.icon
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300 ${
                activeTab === tab.id
                  ? 'gradient-bg text-white shadow-glow'
                  : 'text-gray-600 hover:text-gray-800 hover:bg-white'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{tab.label}</span>
            </button>
          )
        })}
      </div>

      {/* Content */}
      <div className="space-y-6">
        {/* Security Score */}
        {activeTab === 'security-score' && scanResults?.security_score && (
          <div className="space-y-6">
            <div className="text-center">
              <div className={`inline-flex items-center justify-center w-24 h-24 rounded-full ${getSecurityScoreBg(scanResults.security_score.score)} mb-4`}>
                <span className={`text-3xl font-bold ${getSecurityScoreColor(scanResults.security_score.score)}`}>
                  {scanResults.security_score.score}
                </span>
              </div>
              <h3 className="text-2xl font-bold text-gray-800 mb-2">
                Security Score: {scanResults.security_score.grade}
              </h3>
              <p className="text-gray-600">
                Status: <span className="font-semibold">{scanResults.security_score.status}</span>
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="card-modern p-4 rounded-xl">
                <h4 className="font-semibold text-gray-800 mb-2">Score Breakdown</h4>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span>Vulnerabilities Deduction:</span>
                    <span className="font-semibold text-red-600">
                      -{scanResults.security_score.breakdown.vulnerabilities_deduction}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span>Dependencies Deduction:</span>
                    <span className="font-semibold text-red-600">
                      -{scanResults.security_score.breakdown.dependencies_deduction}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Compliance */}
        {activeTab === 'compliance' && scanResults?.compliance_report && (
          <div className="space-y-4">
            <h3 className="text-2xl font-bold text-gray-800 mb-4">Compliance Report</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {Object.entries(scanResults.compliance_report).map(([standard, data]: [string, any]) => (
                <div key={standard} className="card-modern p-4 rounded-xl">
                  <div className="flex items-center justify-between mb-3">
                    <h4 className="font-semibold text-gray-800">{standard}</h4>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      data.status === 'Compliant' ? 'bg-green-100 text-green-800' :
                      data.status === 'Partially Compliant' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {data.status}
                    </span>
                  </div>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span>Score:</span>
                      <span className="font-semibold">{data.score}/100</span>
                    </div>
                    {data.issues.length > 0 && (
                      <div>
                        <span className="text-sm text-gray-600">Issues:</span>
                        <ul className="text-sm text-red-600 mt-1">
                          {data.issues.map((issue: string, idx: number) => (
                            <li key={idx}>• {issue}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Automated Fixes */}
        {activeTab === 'automated-fixes' && scanResults?.automated_fixes && (
          <div className="space-y-4">
            <h3 className="text-2xl font-bold text-gray-800 mb-4">Automated Fix Suggestions</h3>
            <div className="space-y-4">
              {scanResults.automated_fixes.map((fix: any, idx: number) => (
                <div key={idx} className="card-modern p-6 rounded-xl">
                  <div className="flex items-center space-x-3 mb-4">
                    <div className="w-10 h-10 gradient-bg rounded-xl flex items-center justify-center">
                      <Zap className="w-5 h-5 text-white" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-800">{fix.fix_type}</h4>
                      <p className="text-sm text-gray-600">{fix.vulnerability.type}</p>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                    <div>
                      <h5 className="font-medium text-red-600 mb-2">Before (Vulnerable)</h5>
                      <pre className="bg-red-50 p-3 rounded-lg text-sm overflow-x-auto">
                        <code>{fix.before_code}</code>
                      </pre>
                    </div>
                    <div>
                      <h5 className="font-medium text-green-600 mb-2">After (Secure)</h5>
                      <pre className="bg-green-50 p-3 rounded-lg text-sm overflow-x-auto">
                        <code>{fix.after_code}</code>
                      </pre>
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-600">{fix.explanation}</span>
                    <div className="flex items-center space-x-4">
                      <span className="text-gray-500">Difficulty: {fix.implementation_difficulty}</span>
                      <span className="text-gray-500">Time: {fix.estimated_time}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Threat Intelligence */}
        {activeTab === 'threat-intel' && scanResults?.threat_intelligence && (
          <div className="space-y-4">
            <h3 className="text-2xl font-bold text-gray-800 mb-4">Threat Intelligence Report</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {Object.entries(scanResults.threat_intelligence.threat_actors).map(([actor, data]: [string, any]) => (
                <div key={actor} className="card-modern p-4 rounded-xl">
                  <div className="flex items-center space-x-2 mb-3">
                    <Target className="w-5 h-5 text-purple-600" />
                    <h4 className="font-semibold text-gray-800 capitalize">{actor.replace('_', ' ')}</h4>
                  </div>
                  
                  <div className="space-y-2 text-sm">
                    <div>
                      <span className="text-gray-600">Capability:</span>
                      <span className="font-medium ml-2">{data.profile.capability}</span>
                    </div>
                    <div>
                      <span className="text-gray-600">Motivation:</span>
                      <span className="font-medium ml-2">{data.profile.motivation}</span>
                    </div>
                    <div>
                      <span className="text-gray-600">Risk Level:</span>
                      <span className={`font-medium ml-2 px-2 py-1 rounded-full text-xs ${
                        data.risk_level === 'High' ? 'bg-red-100 text-red-800' :
                        data.risk_level === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-green-100 text-green-800'
                      }`}>
                        {data.risk_level}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Analytics */}
        {activeTab === 'analytics' && scanResults?.advanced_analytics && (
          <div className="space-y-4">
            <h3 className="text-2xl font-bold text-gray-800 mb-4">Advanced Analytics</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="card-modern p-4 rounded-xl">
                <h4 className="font-semibold text-gray-800 mb-3">Scan Metrics</h4>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span>Files Scanned:</span>
                    <span className="font-semibold">{scanResults.advanced_analytics.scan_metrics.total_files_scanned}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Vulnerabilities Found:</span>
                    <span className="font-semibold">{scanResults.advanced_analytics.scan_metrics.vulnerabilities_found}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Files/Second:</span>
                    <span className="font-semibold">{scanResults.advanced_analytics.scan_metrics.files_per_second:.1f}</span>
                  </div>
                </div>
              </div>
              
              <div className="card-modern p-4 rounded-xl">
                <h4 className="font-semibold text-gray-800 mb-3">Key Insights</h4>
                <ul className="space-y-2 text-sm">
                  {scanResults.advanced_analytics.insights.map((insight: string, idx: number) => (
                    <li key={idx} className="flex items-start space-x-2">
                      <Star className="w-4 h-4 text-yellow-500 mt-0.5 flex-shrink-0" />
                      <span>{insight}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}

        {/* Innovation */}
        {activeTab === 'innovation' && winningData && (
          <div className="space-y-6">
            <h3 className="text-2xl font-bold text-gray-800 mb-4">Innovation Highlights</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="card-modern p-6 rounded-xl">
                <div className="flex items-center space-x-3 mb-4">
                  <div className="w-12 h-12 gradient-bg rounded-xl flex items-center justify-center">
                    <Award className="w-6 h-6 text-white" />
                  </div>
                  <h4 className="text-xl font-bold text-gray-800">Technical Achievements</h4>
                </div>
                <ul className="space-y-3">
                  {winningData.technical_achievements.map((achievement: string, idx: number) => (
                    <li key={idx} className="flex items-start space-x-2">
                      <CheckCircle className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                      <span className="text-sm">{achievement}</span>
                    </li>
                  ))}
                </ul>
              </div>
              
              <div className="card-modern p-6 rounded-xl">
                <div className="flex items-center space-x-3 mb-4">
                  <div className="w-12 h-12 gradient-bg-alt rounded-xl flex items-center justify-center">
                    <Rocket className="w-6 h-6 text-white" />
                  </div>
                  <h4 className="text-xl font-bold text-gray-800">Innovation Features</h4>
                </div>
                <ul className="space-y-3">
                  {winningData.innovation_highlights.map((highlight: string, idx: number) => (
                    <li key={idx} className="flex items-start space-x-2">
                      <Star className="w-5 h-5 text-yellow-500 mt-0.5 flex-shrink-0" />
                      <span className="text-sm">{highlight}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
