import { useNavigate } from 'react-router-dom'

export default function VideoHelpPage() {
    const navigate = useNavigate()
    return (
        <div className="min-h-screen flex flex-col items-center justify-center px-6 text-center"
            style={{ background: 'linear-gradient(135deg, #0f0f20 0%, #120a2e 100%)' }}>
            {/* Decorative glow */}
            <div className="absolute inset-0 pointer-events-none" aria-hidden="true">
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-purple-600 rounded-full filter blur-[160px] opacity-10" />
            </div>
            <div className="relative z-10 max-w-lg animate-slide-up">
                <div className="w-16 h-16 rounded-2xl flex items-center justify-center text-3xl mb-6 mx-auto"
                    style={{ background: 'rgba(168,85,247,0.15)', border: '1px solid rgba(168,85,247,0.3)' }}>
                    🎥
                </div>
                <h1 className="text-3xl font-bold font-display text-white mb-3">Video AI Help</h1>
                <p className="text-gray-400 mb-8 leading-relaxed">
                    Generate a step-by-step video walkthrough or start a live assisted video. Auto-generated troubleshooting made easy.
                </p>
                {/* Mock video player */}
                <div className="glass-card rounded-2xl overflow-hidden mb-8"
                    style={{ aspectRatio: '16/9' }}>
                    <div className="w-full h-full flex flex-col items-center justify-center gap-3"
                        style={{ background: 'linear-gradient(135deg, rgba(168,85,247,0.15), rgba(236,72,153,0.1))' }}>
                        <button className="w-16 h-16 rounded-full bg-purple-600 hover:bg-purple-500 flex items-center justify-center transition-all duration-200 hover:scale-110 shadow-lg shadow-purple-900/50">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
                                <polygon points="5,3 19,12 5,21" />
                            </svg>
                        </button>
                        <p className="text-gray-400 text-sm">AI Video walkthrough ready</p>
                    </div>
                </div>
                <div className="flex gap-3 justify-center">
                    <button className="px-5 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-sm font-semibold transition-colors">
                        Generate Video
                    </button>
                    <button className="px-5 py-2.5 rounded-xl border border-white/20 text-white text-sm font-semibold hover:border-white/40 transition-colors">
                        Live Session
                    </button>
                </div>
                <button onClick={() => navigate('/choice')}
                    className="mt-6 text-gray-400 hover:text-white text-sm transition-colors">
                    ← Back to options
                </button>
            </div>
        </div>
    )
}
