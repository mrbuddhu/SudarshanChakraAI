'use client'

import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, File, AlertCircle, Loader2 } from 'lucide-react'
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

      const response = await axios.post('http://localhost:8000/scan-code', formData, {
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
    <div className="bg-white p-8 rounded-lg shadow-lg border border-chakra-200">
      <div className="text-center mb-6">
        <h3 className="text-2xl font-bold text-chakra-800 mb-2">Upload Your Code</h3>
        <p className="text-chakra-600">
          Drop your source code file here and let SudarshanChakraAI scan for vulnerabilities
        </p>
      </div>

      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
          isDragActive
            ? 'border-chakra-500 bg-chakra-50'
            : 'border-chakra-300 hover:border-chakra-400'
        }`}
      >
        <input {...getInputProps()} />
        
        {isScanning ? (
          <div className="flex flex-col items-center">
            <Loader2 className="w-12 h-12 text-chakra-500 animate-spin mb-4" />
            <p className="text-lg font-semibold text-chakra-800 mb-2">
              Scanning with Sudarshan Chakra...
            </p>
            <p className="text-chakra-600">
              Analyzing your code for vulnerabilities
            </p>
          </div>
        ) : (
          <div className="flex flex-col items-center">
            <Upload className="w-12 h-12 text-chakra-500 mb-4" />
            <p className="text-lg font-semibold text-chakra-800 mb-2">
              {isDragActive ? 'Drop your file here' : 'Drag & drop your code file here'}
            </p>
            <p className="text-chakra-600 mb-4">
              or click to browse files
            </p>
            <div className="flex items-center space-x-2 text-sm text-chakra-500">
              <File className="w-4 h-4" />
              <span>Supports: .py, .java, .cpp, .c, .cs, .php, .js, .ts, .html</span>
            </div>
          </div>
        )}
      </div>

      {error && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center">
          <AlertCircle className="w-5 h-5 text-red-500 mr-3" />
          <span className="text-red-700">{error}</span>
        </div>
      )}

      <div className="mt-6 text-center">
        <p className="text-sm text-chakra-500">
          Your code is processed securely and never stored permanently
        </p>
      </div>
    </div>
  )
}
