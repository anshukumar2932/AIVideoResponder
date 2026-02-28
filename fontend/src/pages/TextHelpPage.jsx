import { useNavigate } from 'react-router-dom'

export default function TextHelpPage() {
    const navigate = useNavigate()
    return (
        <div className="min-h-screen flex flex-col items-center justify-center px-6 text-center"
            style={{ background: 'linear-gradient(135deg, #0f0f20 0%, #0d1a2e 100%)' }}>
            {/* Decorative glow */}
            <div className="absolute inset-0 pointer-events-none" aria-hidden="true">
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-blue-600 rounded-full filter blur-[160px] opacity-10" />
            </div>
            <div className="relative z-10 max-w-lg animate-slide-up">
                <div className="w-16 h-16 rounded-2xl flex items-center justify-center text-3xl mb-6 mx-auto"
                    style={{ background: 'rgba(43,142,247,0.15)', border: '1px solid rgba(43,142,247,0.3)' }}>
                    💬
                </div>
                <h1 className="text-3xl font-bold font-display text-white mb-3">Text AI Help</h1>
                <p className="text-gray-400 mb-8 leading-relaxed">
                    Chat with our AI to troubleshoot and resolve tickets via text. Instant chatbot assistance and automated ticket replies.
                </p>
                <div className="glass-card rounded-2xl p-6 text-left mb-8">
                    <p className="text-gray-300 text-sm italic">"Hello! I'm your Supporty AI assistant. How can I help you today?"</p>
                    <div className="mt-4 flex gap-2">
                        <input
                            type="text"
                            placeholder="Type your question…"
                            className="flex-1 bg-white/5 border border-white/10 rounded-lg px-3 py-2 text-sm text-white placeholder-gray-500 outline-none focus:border-blue-500"
                        />
                        <button className="px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded-lg text-sm text-white font-medium transition-colors">
                            Send
                        </button>
                    </div>
                </div>
                <button onClick={() => navigate('/choice')}
                    className="text-gray-400 hover:text-white text-sm transition-colors">
                    ← Back to options
                </button>
            </div>
        </div>
    )
}
