'use client'

import { useState } from 'react'
import { Settings, Key, Brain, Zap, Server, Globe, CheckCircle, AlertCircle } from 'lucide-react'

interface LLMConfig {
  provider: string
  apiKey: string
  model: string
  isEnabled: boolean
}

interface LLMDashboardProps {
  onConfigChange: (config: LLMConfig) => void
  currentConfig: LLMConfig
}

export default function LLMDashboard({ onConfigChange, currentConfig }: LLMDashboardProps) {
  const [activeTab, setActiveTab] = useState('openai')
  const [apiKey, setApiKey] = useState(currentConfig.apiKey || '')
  const [selectedModel, setSelectedModel] = useState(currentConfig.model || '')
  const [isEnabled, setIsEnabled] = useState(currentConfig.isEnabled || false)

  const llmProviders = {
    openai: {
      name: 'OpenAI',
      icon: <Brain className="w-5 h-5" />,
      models: [
        { id: 'gpt-4', name: 'GPT-4 (Most Powerful)' },
        { id: 'gpt-3.5-turbo', name: 'GPT-3.5 Turbo (Fast & Cheap)' },
        { id: 'gpt-4-turbo', name: 'GPT-4 Turbo (Latest)' }
      ],
      description: 'Industry-leading AI models with excellent code analysis capabilities'
    },
    anthropic: {
      name: 'Anthropic Claude',
      icon: <Zap className="w-5 h-5" />,
      models: [
        { id: 'claude-3-opus', name: 'Claude 3 Opus (Most Capable)' },
        { id: 'claude-3-sonnet', name: 'Claude 3 Sonnet (Balanced)' },
        { id: 'claude-3-haiku', name: 'Claude 3 Haiku (Fast)' }
      ],
      description: 'Advanced AI focused on safety and helpfulness'
    },
    huggingface: {
      name: 'Hugging Face',
      icon: <Globe className="w-5 h-5" />,
      models: [
        { id: 'microsoft/DialoGPT-medium', name: 'DialoGPT Medium (Free)' },
        { id: 'gpt2', name: 'GPT-2 (Free)' },
        { id: 'distilbert-base-uncased', name: 'DistilBERT (Free)' }
      ],
      description: 'Free open-source models, runs locally or in cloud'
    },
    local: {
      name: 'Local Models',
      icon: <Server className="w-5 h-5" />,
      models: [
        { id: 'llama2-7b', name: 'Llama 2 7B (Local)' },
        { id: 'mistral-7b', name: 'Mistral 7B (Local)' },
        { id: 'codellama-7b', name: 'Code Llama 7B (Local)' }
      ],
      description: 'Run models locally for privacy and zero API costs'
    }
  }

  const handleConfigUpdate = () => {
    const newConfig: LLMConfig = {
      provider: activeTab,
      apiKey: apiKey,
      model: selectedModel,
      isEnabled: isEnabled
    }
    onConfigChange(newConfig)
  }

  const handleTabChange = (tab: string) => {
    setActiveTab(tab)
    setSelectedModel(llmProviders[tab as keyof typeof llmProviders].models[0].id)
    handleConfigUpdate()
  }

  const handleModelChange = (model: string) => {
    setSelectedModel(model)
    handleConfigUpdate()
  }

  const handleApiKeyChange = (key: string) => {
    setApiKey(key)
    handleConfigUpdate()
  }

  const handleToggle = () => {
    setIsEnabled(!isEnabled)
    handleConfigUpdate()
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg border border-chakra-200">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-chakra-500 rounded-full flex items-center justify-center">
            <Brain className="w-5 h-5 text-white" />
          </div>
          <div>
            <h3 className="text-xl font-bold text-chakra-800">AI/LLM Configuration</h3>
            <p className="text-chakra-600">Choose your preferred AI model for vulnerability analysis</p>
          </div>
        </div>
        <div className="flex items-center space-x-3">
          <span className={`px-3 py-1 rounded-full text-sm font-medium ${
            isEnabled 
              ? 'bg-green-100 text-green-800' 
              : 'bg-gray-100 text-gray-800'
          }`}>
            {isEnabled ? 'Enabled' : 'Disabled'}
          </span>
          <button
            onClick={handleToggle}
            className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
              isEnabled ? 'bg-chakra-500' : 'bg-gray-300'
            }`}
          >
            <span
              className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                isEnabled ? 'translate-x-6' : 'translate-x-1'
              }`}
            />
          </button>
        </div>
      </div>

      {/* Provider Tabs */}
      <div className="flex space-x-1 mb-6 bg-gray-100 p-1 rounded-lg">
        {Object.entries(llmProviders).map(([key, provider]) => (
          <button
            key={key}
            onClick={() => handleTabChange(key)}
            className={`flex items-center space-x-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${
              activeTab === key
                ? 'bg-white text-chakra-800 shadow-sm'
                : 'text-gray-600 hover:text-gray-800'
            }`}
          >
            {provider.icon}
            <span>{provider.name}</span>
          </button>
        ))}
      </div>

      {/* Provider Details */}
      <div className="space-y-6">
        <div className="bg-gray-50 p-4 rounded-lg">
          <div className="flex items-center space-x-2 mb-2">
            {llmProviders[activeTab as keyof typeof llmProviders].icon}
            <h4 className="font-semibold text-chakra-800">
              {llmProviders[activeTab as keyof typeof llmProviders].name}
            </h4>
          </div>
          <p className="text-sm text-gray-600 mb-4">
            {llmProviders[activeTab as keyof typeof llmProviders].description}
          </p>
        </div>

        {/* Model Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Select Model
          </label>
          <select
            value={selectedModel}
            onChange={(e) => handleModelChange(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-chakra-500"
          >
            {llmProviders[activeTab as keyof typeof llmProviders].models.map((model) => (
              <option key={model.id} value={model.id}>
                {model.name}
              </option>
            ))}
          </select>
        </div>

        {/* API Key Input */}
        {activeTab !== 'local' && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              API Key
            </label>
            <div className="relative">
              <input
                type="password"
                value={apiKey}
                onChange={(e) => handleApiKeyChange(e.target.value)}
                placeholder={`Enter your ${llmProviders[activeTab as keyof typeof llmProviders].name} API key`}
                className="w-full px-3 py-2 pr-10 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-chakra-500"
              />
              <Key className="absolute right-3 top-2.5 w-5 h-5 text-gray-400" />
            </div>
            <p className="text-xs text-gray-500 mt-1">
              Your API key is stored locally and never sent to our servers
            </p>
          </div>
        )}

        {/* Local Model Instructions */}
        {activeTab === 'local' && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex items-start space-x-3">
              <Server className="w-5 h-5 text-blue-600 mt-0.5" />
              <div>
                <h4 className="font-medium text-blue-800 mb-2">Local Model Setup</h4>
                <ul className="text-sm text-blue-700 space-y-1">
                  <li>• Install Ollama: <code className="bg-blue-100 px-1 rounded">curl -fsSL https://ollama.ai/install.sh | sh</code></li>
                  <li>• Pull model: <code className="bg-blue-100 px-1 rounded">ollama pull {selectedModel}</code></li>
                  <li>• Start Ollama: <code className="bg-blue-100 px-1 rounded">ollama serve</code></li>
                </ul>
              </div>
            </div>
          </div>
        )}

        {/* Status */}
        <div className="flex items-center space-x-2">
          {isEnabled ? (
            <CheckCircle className="w-5 h-5 text-green-500" />
          ) : (
            <AlertCircle className="w-5 h-5 text-yellow-500" />
          )}
          <span className="text-sm text-gray-600">
            {isEnabled 
              ? `${llmProviders[activeTab as keyof typeof llmProviders].name} is ready for vulnerability analysis`
              : 'Enable AI analysis to get intelligent vulnerability explanations'
            }
          </span>
        </div>
      </div>
    </div>
  )
}

