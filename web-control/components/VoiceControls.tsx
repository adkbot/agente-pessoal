'use client'

import { useState, useEffect } from 'react'
import { Mic, Volume2, VolumeX } from 'lucide-react'

interface VoiceControlsProps {
    onVoiceCommand: (text: string) => void
}

export default function VoiceControls({ onVoiceCommand }: VoiceControlsProps) {
    const [isListening, setIsListening] = useState(false)
    const [isSpeaking, setIsSpeaking] = useState(true)
    const [recognition, setRecognition] = useState<any>(null)

    useEffect(() => {
        // Initialize Speech Recognition
        if (typeof window !== 'undefined') {
            const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition

            if (SpeechRecognition) {
                const recognitionInstance = new SpeechRecognition()
                recognitionInstance.continuous = false
                recognitionInstance.interimResults = false
                recognitionInstance.lang = 'pt-BR'

                recognitionInstance.onresult = (event: any) => {
                    const transcript = event.results[0][0].transcript
                    onVoiceCommand(transcript)
                    setIsListening(false)
                }

                recognitionInstance.onerror = (event: any) => {
                    console.error('Speech recognition error:', event.error)
                    setIsListening(false)
                }

                recognitionInstance.onend = () => {
                    setIsListening(false)
                }

                setRecognition(recognitionInstance)
            }
        }
    }, [onVoiceCommand])

    const toggleListening = () => {
        if (!recognition) {
            alert('Speech recognition not supported in this browser')
            return
        }

        if (isListening) {
            recognition.stop()
            setIsListening(false)
        } else {
            recognition.start()
            setIsListening(true)
        }
    }

    const toggleSpeaking = () => {
        setIsSpeaking(!isSpeaking)
    }

    return (
        <div className="flex items-center gap-2">
            {/* Microphone Button */}
            <button
                onClick={toggleListening}
                className={`p-2 rounded-lg transition-all ${isListening
                        ? 'bg-red-600 animate-pulse'
                        : 'bg-purple-600/20 hover:bg-purple-600/40'
                    }`}
                title={isListening ? 'Stop listening' : 'Start voice input'}
            >
                <Mic size={20} className={isListening ? 'text-white' : ''} />
            </button>

            {/* Speaker Button */}
            <button
                onClick={toggleSpeaking}
                className="p-2 rounded-lg bg-purple-600/20 hover:bg-purple-600/40 transition-colors"
                title={isSpeaking ? 'Mute responses' : 'Enable voice responses'}
            >
                {isSpeaking ? <Volume2 size={20} /> : <VolumeX size={20} />}
            </button>
        </div>
    )
}
