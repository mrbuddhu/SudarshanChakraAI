import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'SudarshanChakraAI - AI-Powered Vulnerability Detection',
  description: 'The Sudarshan Chakra of cybersecurity - detect vulnerabilities with divine precision',
  keywords: 'security, vulnerability detection, AI, cybersecurity, hackathon',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen bg-gradient-to-br from-chakra-50 to-chakra-100">
          {children}
        </div>
      </body>
    </html>
  )
}
