'use client'

import { useEffect, useRef } from 'react'

interface ChakraVisualizationProps {
  vulnerabilities: any[]
}

export default function ChakraVisualization({ vulnerabilities }: ChakraVisualizationProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas || vulnerabilities.length === 0) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    // Set canvas size
    canvas.width = 300
    canvas.height = 300

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height)

    const centerX = canvas.width / 2
    const centerY = canvas.height / 2
    const radius = 100

    // Draw Chakra background
    ctx.beginPath()
    ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI)
    ctx.fillStyle = '#fef7ee'
    ctx.fill()
    ctx.strokeStyle = '#f2750a'
    ctx.lineWidth = 2
    ctx.stroke()

    // Draw inner circles (like Chakra spokes)
    for (let i = 1; i <= 8; i++) {
      ctx.beginPath()
      ctx.arc(centerX, centerY, (radius * i) / 8, 0, 2 * Math.PI)
      ctx.strokeStyle = '#fbd5a5'
      ctx.lineWidth = 1
      ctx.stroke()
    }

    // Draw vulnerability points
    const severityColors = {
      critical: '#dc2626',
      high: '#ea580c',
      medium: '#d97706',
      low: '#059669'
    }

    vulnerabilities.forEach((vuln, index) => {
      const angle = (index * 2 * Math.PI) / vulnerabilities.length
      const distance = Math.random() * (radius * 0.7) + (radius * 0.3)
      const x = centerX + Math.cos(angle) * distance
      const y = centerY + Math.sin(angle) * distance

      // Draw vulnerability point
      ctx.beginPath()
      ctx.arc(x, y, 6, 0, 2 * Math.PI)
      ctx.fillStyle = severityColors[vuln.severity as keyof typeof severityColors] || '#6b7280'
      ctx.fill()

      // Draw pulse effect
      ctx.beginPath()
      ctx.arc(x, y, 12, 0, 2 * Math.PI)
      ctx.strokeStyle = severityColors[vuln.severity as keyof typeof severityColors] || '#6b7280'
      ctx.lineWidth = 1
      ctx.globalAlpha = 0.3
      ctx.stroke()
      ctx.globalAlpha = 1
    })

    // Draw center symbol
    ctx.beginPath()
    ctx.arc(centerX, centerY, 15, 0, 2 * Math.PI)
    ctx.fillStyle = '#f2750a'
    ctx.fill()

    // Add text
    ctx.fillStyle = '#782f0f'
    ctx.font = 'bold 12px Arial'
    ctx.textAlign = 'center'
    ctx.fillText('SUDARSHAN', centerX, centerY - 5)
    ctx.fillText('CHAKRA', centerX, centerY + 8)

  }, [vulnerabilities])

  if (vulnerabilities.length === 0) {
    return (
      <div className="text-center py-8">
        <div className="w-32 h-32 mx-auto bg-green-100 rounded-full flex items-center justify-center">
          <div className="text-green-600 text-4xl">✓</div>
        </div>
        <p className="text-green-600 mt-4">No vulnerabilities detected</p>
      </div>
    )
  }

  return (
    <div className="text-center">
      <canvas
        ref={canvasRef}
        className="mx-auto border border-chakra-200 rounded-lg"
        style={{ maxWidth: '100%', height: 'auto' }}
      />
      
      <div className="mt-4 space-y-2">
        <h4 className="font-semibold text-chakra-800">Vulnerability Distribution</h4>
        <div className="flex justify-center space-x-4 text-xs">
          <div className="flex items-center">
            <div className="w-3 h-3 bg-red-500 rounded-full mr-1"></div>
            <span>Critical</span>
          </div>
          <div className="flex items-center">
            <div className="w-3 h-3 bg-orange-500 rounded-full mr-1"></div>
            <span>High</span>
          </div>
          <div className="flex items-center">
            <div className="w-3 h-3 bg-yellow-500 rounded-full mr-1"></div>
            <span>Medium</span>
          </div>
          <div className="flex items-center">
            <div className="w-3 h-3 bg-green-500 rounded-full mr-1"></div>
            <span>Low</span>
          </div>
        </div>
      </div>
    </div>
  )
}
