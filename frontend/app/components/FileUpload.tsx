'use client'

import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, File, AlertCircle, Loader2, Shield } from 'lucide-react'
import axios from 'axios'

interface FileUploadProps {
  onScanComplete: (results: any) => void
  isScanning: boolean
  setIsScanning: (scanning: boolean) => void
}

export default function FileUpload({ onScanComplete, isScanning, setIsScanning }: FileUploadProps) {
  const [error, setError] = useState<string | null>(null)

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return

    const file = acceptedFiles[0]
    setError(null)
    setIsScanning(true)

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await axios.post('http://127.0.0.1:8000/scan-code', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      onScanComplete(response.data)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error scanning file. Please try again.')
      setIsScanning(false)
    }
  }, [onScanComplete, setIsScanning])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/plain': ['.py', '.java', '.cpp', '.c', '.cs', '.php', '.js', '.ts', '.html'],
    },
    multiple: false,
  })

  return (
    <div className="card-modern p-8 rounded-2xl">
      <div className="text-center mb-8">
        <div className="w-20 h-20 gradient-bg rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-glow">
          <Shield className="w-10 h-10 text-white" />
        </div>
        <h2 className="text-3xl font-bold gradient-text mb-3">
          Upload Your Code
        </h2>
        <p className="text-gray-600 text-lg leading-relaxed">
          Drop your source code file here and let SudarshanChakraAI scan for vulnerabilities
        </p>
      </div>

      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-2xl p-12 text-center cursor-pointer transition-all duration-300 hover:scale-[1.02] ${
          isDragActive
            ? 'border-purple-500 bg-gradient-to-r from-purple-50 to-pink-50 shadow-glow'
            : 'border-gray-300 hover:border-purple-400 hover:shadow-modern'
        }`}
      >
        <input {...getInputProps()} />
        
        {isScanning ? (
          <div className="flex flex-col items-center">
            <div className="relative mb-6">
              <div className="w-16 h-16 gradient-bg rounded-2xl flex items-center justify-center shadow-glow pulse-glow">
                <Loader2 className="w-8 h-8 text-white animate-spin" />
              </div>
            </div>
            <p className="text-xl font-bold text-gray-800 mb-3">
              Scanning with Sudarshan Chakra...
            </p>
            <p className="text-gray-600 text-lg">
              Analyzing your code for vulnerabilities
            </p>
          </div>
        ) : (
          <div className="flex flex-col items-center">
            <div className="w-16 h-16 gradient-bg rounded-2xl flex items-center justify-center mb-6 shadow-glow hover:shadow-glow-purple transition-all duration-300">
              <Upload className="w-8 h-8 text-white" />
            </div>
            <p className="text-xl font-bold text-gray-800 mb-3">
              {isDragActive ? 'Drop your file here' : 'Drag & drop your code file here'}
            </p>
            <p className="text-gray-600 text-lg mb-6">
              or click to browse files
            </p>
            <div className="flex items-center space-x-2 text-sm text-gray-500 bg-gray-50 px-4 py-2 rounded-full">
              <File className="w-4 h-4" />
              <span>Supports: .py, .java, .cpp, .c, .cs, .php, .js, .ts, .html</span>
            </div>
          </div>
        )}
      </div>

      {error && (
        <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-xl flex items-center">
          <AlertCircle className="w-5 h-5 text-red-500 mr-3" />
          <span className="text-red-700 font-medium">{error}</span>
        </div>
      )}

      <div className="mt-8 text-center">
        <div className="inline-flex items-center space-x-2 text-sm text-gray-500 bg-gray-50 px-4 py-2 rounded-full">
          <div className="w-2 h-2 bg-green-400 rounded-full"></div>
          <span>Your code is processed securely and never stored permanently</span>
        </div>
      </div>
    </div>
  )
}
