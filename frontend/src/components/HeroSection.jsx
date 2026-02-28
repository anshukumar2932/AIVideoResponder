import { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import LoginModal from './LoginModal'

const LOGOS = [
    { name: 'Creatio', text: 'Creatio' },
    { name: 'HubSpot', text: 'HubSpot' },
    { name: 'Zendesk', text: 'Zendesk' },
    { name: 'Bitrix24', text: 'Bitrix24' },
    { name: 'Apptivo', text: 'Apptivo' },
    { name: 'FreshBooks', text: 'FreshBooks' },
    { name: 'Pipedrive', text: 'Pipedrive' },
]

export default function HeroSection() {
    const navigate = useNavigate()
    const [loginOpen, setLoginOpen] = useState(false)
    const heroRef = useRef(null)
    const artRef = useRef(null)
    const rafRef = useRef(null)

    // Parallax
    useEffect(() => {
        let ticking = false
        const onScroll = () => {
            if (!ticking) {
                rafRef.current = requestAnimationFrame(() => {
                    if (artRef.current) {
                        const y = window.scrollY * 0.15
                        artRef.current.style.transform = `translateY(${y}px)`
                    }
                    ticking = false
                })
                ticking = true
            }
        }
        window.addEventListener('scroll', onScroll, { passive: true })
        return () => {
            window.removeEventListener('scroll', onScroll)
            if (rafRef.current) cancelAnimationFrame(rafRef.current)
        }
    }, [])

    const handleLoginSuccess = () => {
        setLoginOpen(false)
        navigate('/choice')
    }

    return (
        <>
            {/* Hero */}
            <section
                ref={heroRef}
                className="relative min-h-screen overflow-hidden hero-frame"
                aria-label="Hero section"
            >
                {/* BG art with parallax — CSS gradient scene */}
                <div
                    ref={artRef}
                    className="absolute inset-0 will-change-transform overflow-hidden"
                    aria-hidden="true"
                    style={{
                        background: `
              linear-gradient(180deg,
                #0c1445 0%,
                #0f2070 12%,
                #1a50c8 30%,
                #2b7de8 48%,
                #5aabf5 65%,
                #aad4f8 80%,
                #d8eeff 92%,
                #eef7ff 100%
              )`,
                    }}
                >
                    {/* Atmospheric glow */}
                    <div style={{ position: 'absolute', top: '20%', left: '50%', transform: 'translateX(-50%)', width: '60%', height: '50%', background: 'radial-gradient(ellipse, rgba(100,180,255,0.25) 0%, transparent 70%)', pointerEvents: 'none' }} />

                    {/* Cloud layers */}
                    {[
                        { bottom: '42%', left: '5%', w: '30%', h: '80px', o: 0.22 },
                        { bottom: '38%', right: '6%', w: '24%', h: '60px', o: 0.18 },
                        { bottom: '50%', left: '22%', w: '38%', h: '100px', o: 0.12 },
                        { bottom: '54%', right: '20%', w: '28%', h: '70px', o: 0.1 },
                    ].map((c, i) => (
                        <div key={i} style={{ position: 'absolute', bottom: c.bottom, left: c.left, right: c.right, width: c.w, height: c.h, background: `radial-gradient(ellipse 100% 60% at 50% 60%, rgba(255,255,255,${c.o}), transparent)`, borderRadius: '50%', filter: 'blur(20px)' }} />
                    ))}

                    {/* Mountain silhouettes */}
                    <svg style={{ position: 'absolute', bottom: '18%', left: 0, right: 0, width: '100%', height: '35%' }} viewBox="0 0 1440 220" preserveAspectRatio="none" fill="none">
                        <path d="M0 220 L0 160 L100 80 L200 150 L320 55 L430 130 L540 28 L640 110 L740 38 L840 120 L960 58 L1080 130 L1200 62 L1310 135 L1440 72 L1440 220 Z" fill="rgba(160,195,230,0.3)" />
                        <path d="M0 220 L0 175 L90 115 L190 165 L300 95 L410 155 L520 75 L620 145 L720 85 L840 155 L960 100 L1080 165 L1200 105 L1330 160 L1440 118 L1440 220 Z" fill="rgba(185,215,245,0.4)" />
                        <path d="M540 28 L514 80 L566 80 Z" fill="rgba(255,255,255,0.75)" />
                        <path d="M320 55 L295 100 L348 100 Z" fill="rgba(255,255,255,0.65)" />
                        <path d="M740 38 L714 84 L768 84 Z" fill="rgba(255,255,255,0.68)" />
                        <path d="M1200 62 L1177 102 L1226 102 Z" fill="rgba(255,255,255,0.55)" />
                    </svg>

                    {/* Left pillar / archway */}
                    <svg style={{ position: 'absolute', bottom: 0, left: '3%', height: '78%', width: 'auto' }} viewBox="0 0 170 500" fill="none">
                        <defs>
                            <linearGradient id="stL" x1="0" y1="0" x2="1" y2="0">
                                <stop offset="0%" stopColor="#b8a898" />
                                <stop offset="45%" stopColor="#e2d8cc" />
                                <stop offset="100%" stopColor="#9a8878" />
                            </linearGradient>
                        </defs>
                        <rect x="8" y="70" width="52" height="430" rx="3" fill="url(#stL)" />
                        <rect x="8" y="70" width="52" height="430" rx="3" fill="rgba(0,20,80,0.14)" />
                        {[70, 130, 190, 250, 310, 370, 430].map((y, i) => <rect key={i} x="8" y={y} width="52" height="2.5" fill="rgba(0,0,0,0.18)" rx="1" />)}
                        <rect x="0" y="50" width="68" height="24" rx="3" fill="#d0c4b4" />
                        <rect x="4" y="44" width="60" height="10" rx="2" fill="#c4b8a4" />
                        <rect x="105" y="90" width="48" height="410" rx="3" fill="url(#stL)" />
                        <rect x="105" y="90" width="48" height="410" rx="3" fill="rgba(0,20,80,0.10)" />
                        {[90, 150, 210, 270, 330, 390, 450].map((y, i) => <rect key={i} x="105" y={y} width="48" height="2" fill="rgba(0,0,0,0.14)" rx="1" />)}
                        <rect x="97" y="70" width="64" height="22" rx="3" fill="#d0c4b4" />
                        <path d="M8 50 Q86 -12 153 70" stroke="#c0b4a0" strokeWidth="9" fill="none" strokeLinecap="round" />
                        <path d="M8 50 Q86 -12 153 70" stroke="rgba(0,0,0,0.14)" strokeWidth="3" fill="none" />
                        <ellipse cx="80" cy="498" rx="85" ry="7" fill="rgba(0,0,0,0.2)" />
                        <rect x="16" y="484" width="28" height="14" rx="2" fill="#a89888" />
                        <rect x="94" y="488" width="20" height="10" rx="2" fill="#b0a090" />
                    </svg>

                    {/* Right pillar / archway (mirrored) */}
                    <svg style={{ position: 'absolute', bottom: 0, right: '3%', height: '72%', width: 'auto', transform: 'scaleX(-1)' }} viewBox="0 0 170 500" fill="none">
                        <defs>
                            <linearGradient id="stR" x1="0" y1="0" x2="1" y2="0">
                                <stop offset="0%" stopColor="#b8a898" />
                                <stop offset="55%" stopColor="#ddd3c3" />
                                <stop offset="100%" stopColor="#9a8878" />
                            </linearGradient>
                        </defs>
                        <rect x="8" y="70" width="52" height="430" rx="3" fill="url(#stR)" />
                        <rect x="8" y="70" width="52" height="430" rx="3" fill="rgba(0,20,80,0.12)" />
                        {[70, 130, 190, 250, 310, 370, 430].map((y, i) => <rect key={i} x="8" y={y} width="52" height="2.5" fill="rgba(0,0,0,0.14)" rx="1" />)}
                        <rect x="0" y="50" width="68" height="24" rx="3" fill="#d0c4b4" />
                        <rect x="105" y="90" width="48" height="410" rx="3" fill="url(#stR)" />
                        {[90, 150, 210, 270, 330, 390, 450].map((y, i) => <rect key={i} x="105" y={y} width="48" height="2" fill="rgba(0,0,0,0.12)" rx="1" />)}
                        <rect x="97" y="70" width="64" height="22" rx="3" fill="#d0c4b4" />
                        <path d="M8 50 Q86 -12 153 70" stroke="#c0b4a0" strokeWidth="9" fill="none" strokeLinecap="round" />
                        <path d="M8 50 Q86 -12 153 70" stroke="rgba(0,0,0,0.12)" strokeWidth="3" fill="none" />
                        <ellipse cx="80" cy="498" rx="85" ry="7" fill="rgba(0,0,0,0.16)" />
                        <rect x="16" y="484" width="28" height="14" rx="2" fill="#a89888" />
                    </svg>

                    {/* Frozen ground / ice */}
                    <div style={{ position: 'absolute', bottom: 0, left: 0, right: 0, height: '20%', background: 'linear-gradient(180deg, rgba(170,210,245,0.35) 0%, rgba(130,185,230,0.6) 60%, rgba(100,160,215,0.8) 100%)', borderTop: '1px solid rgba(255,255,255,0.2)' }} />
                    {/* Shimmer reflection on ice */}
                    <div style={{ position: 'absolute', bottom: '12%', left: '25%', right: '25%', height: '2px', background: 'linear-gradient(90deg, transparent, rgba(255,255,255,0.5), transparent)', filter: 'blur(2px)' }} />
                    <div style={{ position: 'absolute', bottom: '8%', left: '35%', right: '38%', height: '2px', background: 'linear-gradient(90deg, transparent, rgba(255,255,255,0.35), transparent)', filter: 'blur(3px)' }} />
                </div>

                {/* Vignette */}
                <div
                    className="absolute inset-0"
                    style={{
                        background: 'linear-gradient(to bottom, rgba(10,15,40,0.38) 0%, rgba(10,15,40,0.15) 40%, rgba(10,15,40,0.55) 100%)',
                    }}
                    aria-hidden="true"
                />

                {/* Content */}
                <div className="relative z-10 max-w-[1200px] mx-auto px-6 flex flex-col items-center justify-start pt-40 pb-24 text-center min-h-screen">
                    {/* Badge */}
                    <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm text-gray-200 mb-8 font-medium"
                        style={{ background: 'rgba(255,255,255,0.15)', backdropFilter: 'blur(10px)', border: '1px solid rgba(255,255,255,0.2)' }}>
                        <span className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse" aria-hidden="true" />
                        Smarter support, happier customers.
                    </div>

                    {/* H1 */}
                    <h1 className="font-display font-bold text-white leading-tight max-w-3xl
                         text-[2.1rem] sm:text-5xl md:text-6xl lg:text-[4rem]"
                        style={{ textShadow: '0 2px 20px rgba(0,0,0,0.4)' }}>
                        Customer support platform combines multi-channel ticket management
                    </h1>

                    {/* Subhead */}
                    <p className="mt-6 text-gray-200 max-w-2xl mx-auto leading-relaxed
                        text-sm sm:text-base md:text-lg"
                        style={{ textShadow: '0 1px 8px rgba(0,0,0,0.5)' }}>
                        Manage tickets, chats, calls, and knowledge base articles in a unified
                        platform designed for growing businesses. Enhance customer satisfaction,
                        resolve issues faster.
                    </p>

                    {/* CTAs */}
                    <div className="mt-10 flex flex-col sm:flex-row items-center gap-4 w-full sm:w-auto">
                        <button
                            onClick={() => setLoginOpen(true)}
                            className="group relative px-7 py-3.5 rounded-full bg-gray-900 text-white font-semibold text-base
                         hover:bg-gray-800 hover:shadow-2xl transition-all duration-200 active:scale-95
                         flex items-center gap-2 w-full sm:w-auto justify-center"
                        >
                            See It Investigate
                            <span className="inline-block transition-transform duration-200 group-hover:translate-x-1" aria-hidden="true">→</span>
                        </button>

                        <button
                            onClick={() => setLoginOpen(true)}
                            className="px-7 py-3.5 rounded-full border-2 border-white text-white font-semibold text-base
                         bg-white/10 backdrop-blur-sm
                         hover:bg-white hover:text-gray-900 hover:shadow-xl
                         transition-all duration-200 active:scale-95 w-full sm:w-auto"
                        >
                            Book a demo
                        </button>
                    </div>

                    {/* Trusted logos */}
                    <div className="mt-16 w-full max-w-2xl">
                        <p className="text-gray-400 text-xs uppercase tracking-widest mb-4">Trusted by leaders in</p>
                        <div className="flex flex-wrap justify-center gap-x-8 gap-y-4">
                            {LOGOS.map((l) => (
                                <span key={l.name}
                                    className="text-white/50 font-semibold text-sm tracking-wide hover:text-white/80 transition-colors duration-200 cursor-default"
                                >
                                    {l.text}
                                </span>
                            ))}
                        </div>
                    </div>
                </div>
            </section>

            {/* Features teaser below hero */}
            <section className="relative z-10 bg-[#0f0f20] py-24 px-6">
                <div className="max-w-[1200px] mx-auto">
                    <h2 className="text-center text-3xl md:text-4xl font-bold font-display text-white mb-4">
                        Everything your support team needs
                    </h2>
                    <p className="text-center text-gray-400 max-w-xl mx-auto mb-14 text-base">
                        One platform to handle every customer interaction — from first contact to resolution.
                    </p>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        {[
                            { icon: '🎫', title: 'Ticket Management', desc: 'Unified inbox for all channels — email, chat, social, and voice.' },
                            { icon: '🤖', title: 'AI Responses', desc: 'Instantly draft replies with context-aware AI suggestions.' },
                            { icon: '🎥', title: 'Video Assistance', desc: 'Generate step-by-step video walkthroughs automatically.' },
                        ].map((f) => (
                            <div key={f.title} className="glass-card rounded-2xl p-7 group hover:border-white/20 transition-all duration-200">
                                <div className="text-3xl mb-4">{f.icon}</div>
                                <h3 className="text-white font-bold text-lg mb-2">{f.title}</h3>
                                <p className="text-gray-400 text-sm leading-relaxed">{f.desc}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {loginOpen && (
                <LoginModal
                    onClose={() => setLoginOpen(false)}
                    onSuccess={handleLoginSuccess}
                />
            )}
        </>
    )
}
