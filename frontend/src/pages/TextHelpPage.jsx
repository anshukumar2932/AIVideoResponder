import { useNavigate } from 'react-router-dom'
import { useState } from 'react'

export default function TextHelpPage() {
    const navigate = useNavigate()
    const [messages, setMessages] = useState([
        { type: 'ai', text: "Hello! I'm your AI assistant. How can I help you today?" }
    ])
    const [inputText, setInputText] = useState('')
    const [loading, setLoading] = useState(false)

    const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

    const sendMessage = async () => {
        if (!inputText.trim() || loading) return

        const userMessage = inputText.trim()
        setInputText('')
        
        // Add user message to chat
        setMessages(prev => [...prev, { type: 'user', text: userMessage }])
        setLoading(true)

        try {
            // For text-based interaction, we can create a simple text endpoint
            // or simulate the audio workflow with text-to-speech
            const response = await fetch(`${API_BASE_URL}/text-support`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: userMessage })
            })

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`)
            }

            const data = await response.json()
            
            if (data.error) {
                setMessages(prev => [...prev, { type: 'ai', text: `Error: ${data.error}` }])
            } else {
                setMessages(prev => [...prev, { type: 'ai', text: data.response }])
            }
        } catch (err) {
            console.error('Error sending message:', err)
            setMessages(prev => [...prev, { 
                type: 'ai', 
                text: "Sorry, I'm having trouble connecting to the server. Please try again later." 
            }])
        } finally {
            setLoading(false)
        }
    }

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            sendMessage()
        }
    }

    return (
        <div className="min-h-screen flex flex-col items-center justify-center px-6 text-center"
            style={{ background: 'linear-gradient(135deg, #0f0f20 0%, #0d1a2e 100%)' }}>
            {/* Decorative glow */}
            <div className="absolute inset-0 pointer-events-none" aria-hidden="true">
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-blue-600 rounded-full filter blur-[160px] opacity-10" />
            </div>
            
            <div className="relative z-10 max-w-2xl w-full animate-slide-up">
                <div className="w-16 h-16 rounded-2xl flex items-center justify-center text-3xl mb-6 mx-auto"
                    style={{ background: 'rgba(43,142,247,0.15)', border: '1px solid rgba(43,142,247,0.3)' }}>
                    💬
                </div>
                
                <h1 className="text-3xl font-bold font-display text-white mb-3">Text AI Assistant</h1>
                <p className="text-gray-400 mb-8 leading-relaxed">
                    Chat with our AI to get instant help and support. Ask questions and get intelligent responses.
                </p>
                
                {/* Chat Container */}
                <div className="glass-card rounded-2xl p-6 text-left mb-6 h-96 overflow-y-auto">
                    <div className="space-y-4">
                        {messages.map((message, index) => (
                            <div key={index} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                                <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                                    message.type === 'user' 
                                        ? 'bg-blue-600 text-white' 
                                        : 'bg-gray-700 text-gray-100'
                                }`}>
                                    <p className="text-sm">{message.text}</p>
                                </div>
                            </div>
                        ))}
                        
                        {loading && (
                            <div className="flex justify-start">
                                <div className="bg-gray-700 text-gray-100 px-4 py-2 rounded-lg">
                                    <div className="flex items-center space-x-2">
                                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-500"></div>
                                        <span className="text-sm">AI is thinking...</span>
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
                
                {/* Input Area */}
                <div className="flex gap-2 mb-6">
                    <input
                        type="text"
                        value={inputText}
                        onChange={(e) => setInputText(e.target.value)}
                        onKeyPress={handleKeyPress}
                        placeholder="Type your question…"
                        disabled={loading}
                        className="flex-1 bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-500 outline-none focus:border-blue-500 disabled:opacity-50"
                    />
                    <button 
                        onClick={sendMessage}
                        disabled={loading || !inputText.trim()}
                        className="px-6 py-3 bg-blue-600 hover:bg-blue-500 disabled:bg-blue-800 disabled:cursor-not-allowed rounded-lg text-white font-medium transition-colors">
                        Send
                    </button>
                </div>
                
                <button onClick={() => navigate('/choice')}
                    className="text-gray-400 hover:text-white text-sm transition-colors">
                    ← Back to options
                </button>
            </div>
        </div>
    )
}
