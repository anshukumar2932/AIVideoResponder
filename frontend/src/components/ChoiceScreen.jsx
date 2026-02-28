import { useRef, useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

function ChatIcon() {
    return (
        <svg width="40" height="40" viewBox="0 0 48 48" fill="none">
            <circle cx="24" cy="24" r="24" fill="rgba(43,142,247,0.15)" />
            <path d="M14 16h20a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H25l-5 4v-4h-6a2 2 0 0 1-2-2V18a2 2 0 0 1 2-2z"
                stroke="#2b8ef7" strokeWidth="1.5" strokeLinejoin="round" fill="none" />
            <path d="M19 22q.5-2 5-2t3 4-4 2" stroke="#7dd3fc" strokeWidth="1.2" strokeLinecap="round" fill="none" />
            <circle cx="30" cy="24" r="1.2" fill="#7dd3fc" />
        </svg>
    )
}

function VideoIcon() {
    return (
        <svg width="40" height="40" viewBox="0 0 48 48" fill="none">
            <circle cx="24" cy="24" r="24" fill="rgba(168,85,247,0.15)" />
            <rect x="10" y="16" width="20" height="14" rx="2" stroke="#a855f7" strokeWidth="1.5" fill="none" />
            <path d="M30 20l8-4v14l-8-4V20z" stroke="#c084fc" strokeWidth="1.5" strokeLinejoin="round" fill="none" />
            <path d="M36 14l-3 4" stroke="#f0abfc" strokeWidth="1" strokeLinecap="round" />
            <circle cx="38" cy="12" r="2" fill="#f0abfc" opacity="0.8" />
        </svg>
    )
}

export default function ChoiceScreen() {
    const navigate = useNavigate()
    const [selected, setSelected] = useState(null)
    const firstCardRef = useRef(null)

    useEffect(() => {
        firstCardRef.current?.focus()
    }, [])

    const cards = [
        {
            id: 'text',
            icon: <ChatIcon />,
            title: 'Text AI Help',
            description: 'Instant chatbot assistance and automated ticket replies.',
            cta: 'Start text help',
            route: '/text-help',
            gradient: 'from-blue-600/20 to-cyan-600/10',
            glow: 'rgba(43,142,247,0.35)',
            ctaColor: 'from-blue-500 to-blue-700',
        },
        {
            id: 'video',
            icon: <VideoIcon />,
            title: 'Video AI Help',
            description: 'Auto-generated troubleshooting videos and live video assistance.',
            cta: 'Start video help',
            route: '/video-help',
            gradient: 'from-purple-600/20 to-pink-600/10',
            glow: 'rgba(168,85,247,0.35)',
            ctaColor: 'from-purple-500 to-purple-700',
        },
    ]

    const handleSelect = (route) => {
        navigate(route)
    }

    const handleKeyDown = (e, route, id) => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault()
            setSelected(id)
            setTimeout(() => handleSelect(route), 160)
        }
    }

    return (
        <div className="min-h-screen flex flex-col items-center justify-center px-6 py-20"
            style={{ background: 'linear-gradient(135deg, #0f0f20 0%, #0d1a2e 100%)' }}>
            {/* Decorative background glow */}
            <div className="absolute inset-0 overflow-hidden pointer-events-none" aria-hidden="true">
                <div className="absolute top-1/3 left-1/4 w-96 h-96 bg-blue-600 rounded-full filter blur-[120px] opacity-10" />
                <div className="absolute bottom-1/3 right-1/4 w-96 h-96 bg-purple-600 rounded-full filter blur-[120px] opacity-10" />
            </div>

            <div className="relative z-10 w-full max-w-3xl animate-slide-up">
                {/* Header */}
                <div className="text-center mb-10">
                    <span className="font-bold text-white tracking-wider text-base">SUPPORTY</span>
                    <h1 className="mt-4 text-3xl md:text-4xl font-bold text-white font-display leading-tight">
                        How would you like help today?
                    </h1>
                    <p className="mt-3 text-gray-400 text-base max-w-md mx-auto">
                        Choose your preferred AI-powered support experience.
                    </p>
                </div>

                {/* Cards */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-5" role="listbox" aria-label="Support options">
                    {cards.map((card, i) => (
                        <div
                            key={card.id}
                            ref={i === 0 ? firstCardRef : null}
                            role="option"
                            tabIndex={0}
                            aria-selected={selected === card.id}
                            onClick={() => { setSelected(card.id); setTimeout(() => handleSelect(card.route), 200) }}
                            onKeyDown={(e) => handleKeyDown(e, card.route, card.id)}
                            className={`choice-card relative cursor-pointer rounded-2xl p-7 flex flex-col gap-4
                         bg-gradient-to-br ${card.gradient}
                         border border-white/10 outline-none`}
                            style={{
                                animationDelay: `${i * 80}ms`,
                                background: `linear-gradient(135deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01))`,
                                backdropFilter: 'blur(12px)',
                            }}
                        >
                            {/* Icon */}
                            <div className="flex-shrink-0">{card.icon}</div>

                            {/* Text */}
                            <div>
                                <h2 className="text-xl font-bold text-white mb-2">{card.title}</h2>
                                <p className="text-gray-400 text-sm leading-relaxed">{card.description}</p>
                            </div>

                            {/* CTA */}
                            <button
                                tabIndex={-1}
                                aria-hidden="true"
                                className={`mt-auto self-start px-5 py-2.5 rounded-xl text-sm font-semibold
                           text-white bg-gradient-to-r ${card.ctaColor}
                           transition-all duration-200 hover:shadow-lg`}
                            >
                                {card.cta} →
                            </button>
                        </div>
                    ))}
                </div>

                <p className="text-center text-gray-600 text-xs mt-6">
                    Press <kbd className="bg-white/10 px-1.5 py-0.5 rounded text-gray-400">Tab</kbd> to navigate,{' '}
                    <kbd className="bg-white/10 px-1.5 py-0.5 rounded text-gray-400">Enter</kbd> to select
                </p>
            </div>
        </div>
    )
}
