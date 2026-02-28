import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import LoginModal from '../components/LoginModal'

export default function Header() {
    const [scrolled, setScrolled] = useState(false)
    const [loginOpen, setLoginOpen] = useState(false)
    const navigate = useNavigate()

    useEffect(() => {
        const onScroll = () => setScrolled(window.scrollY > 60)
        window.addEventListener('scroll', onScroll, { passive: true })
        return () => window.removeEventListener('scroll', onScroll)
    }, [])

    const handleLoginSuccess = () => {
        setLoginOpen(false)
        navigate('/choice')
    }

    return (
        <>
            <header
                className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${scrolled
                        ? 'bg-white/95 backdrop-blur-md shadow-sm'
                        : 'bg-transparent'
                    }`}
            >
                <div className="max-w-[1200px] mx-auto px-6 h-16 flex items-center justify-between">
                    {/* Brand */}
                    <a
                        href="/"
                        className={`font-bold text-xl tracking-wider transition-colors duration-300 ${scrolled ? 'text-gray-900' : 'text-white'
                            }`}
                        aria-label="Supporty — Home"
                    >
                        SUPPORTY
                    </a>

                    {/* Demo CTA */}
                    <button
                        onClick={() => setLoginOpen(true)}
                        className="bg-gray-900 text-white px-5 py-2 rounded-full text-sm font-semibold
                       hover:bg-gray-700 hover:shadow-lg transition-all duration-200
                       active:scale-95 focus-visible:ring-2 focus-visible:ring-brand-blue"
                        aria-label="Open demo login"
                    >
                        Demo
                    </button>
                </div>
            </header>

            {loginOpen && (
                <LoginModal
                    onClose={() => setLoginOpen(false)}
                    onSuccess={handleLoginSuccess}
                />
            )}
        </>
    )
}
