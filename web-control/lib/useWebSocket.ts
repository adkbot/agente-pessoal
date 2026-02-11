'use client'

import { useEffect, useState, useCallback } from 'react'

interface CommandMessage {
    type: 'command'
    timestamp: string
    command: string
    permission: string
    params?: any
}

interface ResponseMessage {
    type: 'response'
    timestamp: string
    status: 'success' | 'denied' | 'error'
    result: any
    error: string | null
}

export function useWebSocket() {
    const [isConnected, setIsConnected] = useState(false)
    const [lastResponse, setLastResponse] = useState<ResponseMessage | null>(null)

    const sendCommand = useCallback(async (command: string, permission: string) => {
        try {
            const response = await fetch('/api/relay', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    command,
                    permission,
                    params: {}
                })
            })

            const data = await response.json()
            setLastResponse(data)
            setIsConnected(true)

            return data
        } catch (error: any) {
            console.error('Command send error:', error)
            setIsConnected(false)

            const errorResponse: ResponseMessage = {
                type: 'response',
                timestamp: new Date().toISOString(),
                status: 'error',
                result: null,
                error: error.message
            }

            setLastResponse(errorResponse)
            return errorResponse
        }
    }, [])

    // Check connection on mount
    useEffect(() => {
        fetch('/api/relay')
            .then(() => setIsConnected(true))
            .catch(() => setIsConnected(false))
    }, [])

    return {
        isConnected,
        lastResponse,
        sendCommand
    }
}
