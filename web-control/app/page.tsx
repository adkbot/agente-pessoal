'use client'

import { useState, useEffect } from 'react'
import { Settings, Mic, Volume2, VolumeX, Send, Circle } from 'lucide-react'
import CredentialsModal from '@/components/CredentialsModal'
import VoiceControls from '@/components/VoiceControls'
import { useWebSocket } from '@/lib/useWebSocket'

type ConnectionStatus = 'disconnected' | 'connecting' | 'connected'

export default function Home() {
  const [command, setCommand] = useState('')
  const [permission, setPermission] = useState('trade_execution')
  const [showCredentials, setShowCredentials] = useState(false)
  const [responses, setResponses] = useState<Array<{ command: string, response: string, timestamp: string }>>([])

  // WebSocket connection
  const { isConnected, sendCommand: sendWsCommand } = useWebSocket()
  const status: ConnectionStatus = isConnected ? 'connected' : 'disconnected'


  const handleSendCommand = async () => {
    if (!command.trim()) return

    const timestamp = new Date().toLocaleTimeString()

    // Send via WebSocket/HTTP relay
    const response = await sendWsCommand(command, permission)

    // Add to response history
    setResponses(prev => [{
      command,
      response: response.status === 'success'
        ? `✅ ${response.result}`
        : `❌ ${response.error || 'Error'}`,
      timestamp
    }, ...prev])

    setCommand('')
  }

  const handleVoiceCommand = (text: string) => {
    setCommand(text)
  }

  const handleVoiceResponse = (text: string) => {
    // Speech synthesis will handle this
    console.log('Voice response:', text)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 text-white">
      {/* Header */}
      <div className="border-b border-purple-500/30 bg-black/30 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-pink-600 bg-clip-text text-transparent">
              AntiGravity
            </div>
            <StatusIndicator status={status} />
          </div>

          <div className="flex items-center gap-4">
            <VoiceControls onVoiceCommand={handleVoiceCommand} />
            <button
              onClick={() => setShowCredentials(true)}
              className="p-2 rounded-lg bg-purple-600/20 hover:bg-purple-600/40 transition-colors"
              title="Credentials"
            >
              <Settings size={20} />
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto space-y-6">

          {/* Command Input */}
          <div className="bg-black/40 backdrop-blur-sm rounded-xl border border-purple-500/30 p-6 shadow-2xl">
            <h2 className="text-lg font-semibold mb-4 text-purple-300">Remote Command</h2>

            <div className="space-y-4">
              {/* Permission Selector */}
              <div>
                <label className="block text-sm text-gray-400 mb-2">Permission Level</label>
                <select
                  value={permission}
                  onChange={(e) => setPermission(e.target.value)}
                  className="w-full px-4 py-2 bg-gray-800/50 border border-purple-500/30 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                >
                  <option value="system_access">System Access</option>
                  <option value="browser_automation">Browser Automation</option>
                  <option value="trade_execution">Trade Execution</option>
                  <option value="file_modification">File Modification</option>
                  <option value="api_call">API Call</option>
                </select>
              </div>

              {/* Command Input */}
              <div>
                <label className="block text-sm text-gray-400 mb-2">Command</label>
                <div className="flex gap-2">
                  <input
                    type="text"
                    value={command}
                    onChange={(e) => setCommand(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSendCommand()}
                    placeholder="Enter command (e.g., comprar BTC 0.01)"
                    className="flex-1 px-4 py-3 bg-gray-800/50 border border-purple-500/30 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                  />
                  <button
                    onClick={handleSendCommand}
                    disabled={!command.trim()}
                    className="px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 rounded-lg hover:from-purple-500 hover:to-pink-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center gap-2"
                  >
                    <Send size={18} />
                    Send
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Response History */}
          <div className="bg-black/40 backdrop-blur-sm rounded-xl border border-purple-500/30 p-6 shadow-2xl">
            <h2 className="text-lg font-semibold mb-4 text-purple-300">Response History</h2>

            {responses.length === 0 ? (
              <p className="text-gray-500 text-center py-8">No commands sent yet</p>
            ) : (
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {responses.map((item, index) => (
                  <div key={index} className="bg-gray-800/30 rounded-lg p-4 border border-purple-500/20">
                    <div className="flex justify-between text-xs text-gray-400 mb-2">
                      <span>{item.timestamp}</span>
                    </div>
                    <div className="text-sm">
                      <div className="text-purple-300 mb-1">→ {item.command}</div>
                      <div className="text-gray-300">{item.response}</div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

        </div>
      </div>

      {/* Modals */}
      {showCredentials && (
        <CredentialsModal onClose={() => setShowCredentials(false)} />
      )}
    </div>
  )
}

function StatusIndicator({ status }: { status: ConnectionStatus }) {
  const colors = {
    connected: 'bg-green-500',
    connecting: 'bg-yellow-500',
    disconnected: 'bg-red-500'
  }

  const labels = {
    connected: 'Connected',
    connecting: 'Connecting...',
    disconnected: 'Disconnected'
  }

  return (
    <div className="flex items-center gap-2 text-sm">
      <Circle size={8} className={`${colors[status]} fill-current`} />
      <span className="text-gray-400">{labels[status]}</span>
    </div>
  )
}
