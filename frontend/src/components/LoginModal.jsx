import { useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'

function LockIcon() {
    return (
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-gray-400">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
            <path d="M7 11V7a5 5 0 0 1 10 0v4" />
        </svg>
    )
}

function MailIcon() {
    return (
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-gray-400">
            <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" />
            <polyline points="22,6 12,13 2,6" />
        </svg>
    )
}

function EyeIcon({ open }) {
    return open ? (
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
            <circle cx="12" cy="12" r="3" />
        </svg>
    ) : (
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94" />
            <path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19" />
            <line x1="1" y1="1" x2="23" y2="23" />
        </svg>
    )
}

import { useState } from 'react'

export default function LoginModal({ onClose, onSuccess }) {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [showPw, setShowPw] = useState(false)
    const [errors, setErrors] = useState({})
    const [loading, setLoading] = useState(false)
    const overlayRef = useRef(null)
    const dialogRef = useRef(null)
    const firstFocusRef = useRef(null)
    const navigate = useNavigate()

    // Focus trap
    useEffect(() => {
        firstFocusRef.current?.focus()
        const prevActive = document.activeElement

        const trapFocus = (e) => {
            if (!dialogRef.current) return
            const focusable = dialogRef.current.querySelectorAll(
                'a[href], button:not([disabled]), input, textarea, select, [tabindex]:not([tabindex="-1"])'
            )
            const first = focusable[0]
            const last = focusable[focusable.length - 1]
            if (e.key === 'Tab') {
                if (e.shiftKey && document.activeElement === first) {
                    e.preventDefault(); last.focus()
                } else if (!e.shiftKey && document.activeElement === last) {
                    e.preventDefault(); first.focus()
                }
            }
            if (e.key === 'Escape') onClose()
        }

        document.addEventListener('keydown', trapFocus)
        document.body.style.overflow = 'hidden'
        return () => {
            document.removeEventListener('keydown', trapFocus)
            document.body.style.overflow = ''
            prevActive?.focus()
        }
    }, [onClose])

    const validate = () => {
        const errs = {}
        if (!email.trim()) errs.email = 'Email or username is required.'
        else if (email.includes('@') && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email))
            errs.email = 'Please enter a valid email address.'
        if (!password) errs.password = 'Password is required.'
        else if (password.length < 6) errs.password = 'Password must be at least 6 characters.'
        return errs
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        const errs = validate()
        if (Object.keys(errs).length) { setErrors(errs); return }
        setLoading(true)
        // Simulated auth delay
        await new Promise(r => setTimeout(r, 900))
        setLoading(false)
        onSuccess()
    }

    return (
        <div
            ref={overlayRef}
            className="fixed inset-0 z-[100] flex items-center justify-center p-4"
            style={{ background: 'rgba(0,0,0,0.65)', backdropFilter: 'blur(4px)' }}
            onClick={(e) => e.target === overlayRef.current && onClose()}
            aria-hidden="false"
        >
            <div
                ref={dialogRef}
                role="dialog"
                aria-modal="true"
                aria-labelledby="login-title"
                className="relative w-full max-w-md animate-fade-scale"
                style={{
                    background: 'linear-gradient(145deg, #1a1a2e, #16213e)',
                    border: '1px solid rgba(255,255,255,0.1)',
                    borderRadius: '16px',
                    boxShadow: '0 25px 60px rgba(0,0,0,0.6), 0 0 0 1px rgba(255,255,255,0.05)',
                    padding: '2.5rem',
                }}
            >
                {/* Close */}
                <button
                    onClick={onClose}
                    aria-label="Close login dialog"
                    className="absolute top-4 right-4 text-gray-400 hover:text-white transition-colors
                     w-8 h-8 flex items-center justify-center rounded-full hover:bg-white/10"
                >
                    ✕
                </button>

                {/* Brand inside modal */}
                <div className="mb-6">
                    <span className="font-bold text-white tracking-wider text-lg">SUPPORTY</span>
                </div>

                <h2 id="login-title" className="text-2xl font-bold text-white mb-1">
                    Sign in to your account
                </h2>
                <p className="text-gray-400 text-sm mb-6">
                    Use your account email — we&apos;ll never share it.
                </p>

                <form onSubmit={handleSubmit} noValidate className="space-y-4">
                    {/* Email */}
                    <div>
                        <label htmlFor="login-email" className="block text-sm font-medium text-gray-300 mb-1.5">
                            Email or username
                        </label>
                        <div className="relative">
                            <div className="absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none">
                                <MailIcon />
                            </div>
                            <input
                                ref={firstFocusRef}
                                id="login-email"
                                type="text"
                                autoComplete="username email"
                                value={email}
                                onChange={e => { setEmail(e.target.value); setErrors(prev => ({ ...prev, email: '' })) }}
                                placeholder="you@company.com"
                                aria-describedby={errors.email ? 'email-error' : undefined}
                                aria-invalid={!!errors.email}
                                className={`w-full pl-10 pr-4 py-3 rounded-lg text-white placeholder-gray-500
                           text-sm transition-all duration-150 outline-none
                           ${errors.email
                                        ? 'border-red-500 bg-red-900/10 border focus:border-red-400'
                                        : 'border border-white/10 bg-white/5 focus:border-blue-500 focus:bg-white/8'
                                    }`}
                            />
                        </div>
                        {errors.email && (
                            <p id="email-error" role="alert" className="mt-1.5 text-xs text-red-400 flex items-center gap-1">
                                <span aria-hidden="true">⚠</span> {errors.email}
                            </p>
                        )}
                    </div>

                    {/* Password */}
                    <div>
                        <label htmlFor="login-password" className="block text-sm font-medium text-gray-300 mb-1.5">
                            Password
                        </label>
                        <div className="relative">
                            <div className="absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none">
                                <LockIcon />
                            </div>
                            <input
                                id="login-password"
                                type={showPw ? 'text' : 'password'}
                                autoComplete="current-password"
                                value={password}
                                onChange={e => { setPassword(e.target.value); setErrors(prev => ({ ...prev, password: '' })) }}
                                placeholder="••••••••"
                                aria-describedby={errors.password ? 'pw-error' : undefined}
                                aria-invalid={!!errors.password}
                                className={`w-full pl-10 pr-12 py-3 rounded-lg text-white placeholder-gray-500
                           text-sm transition-all duration-150 outline-none
                           ${errors.password
                                        ? 'border-red-500 bg-red-900/10 border focus:border-red-400'
                                        : 'border border-white/10 bg-white/5 focus:border-blue-500'
                                    }`}
                            />
                            <button
                                type="button"
                                onClick={() => setShowPw(!showPw)}
                                aria-label={showPw ? 'Hide password' : 'Show password'}
                                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white transition-colors p-1"
                            >
                                <EyeIcon open={showPw} />
                            </button>
                        </div>
                        {errors.password && (
                            <p id="pw-error" role="alert" className="mt-1.5 text-xs text-red-400 flex items-center gap-1">
                                <span aria-hidden="true">⚠</span> {errors.password}
                            </p>
                        )}
                    </div>

                    {/* Forgot password */}
                    <div className="flex justify-end">
                        <a href="#" className="text-xs text-blue-400 hover:text-blue-300 transition-colors">
                            Forgot password?
                        </a>
                    </div>

                    {/* Submit */}
                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full py-3 rounded-lg font-semibold text-white text-sm
                       transition-all duration-200 flex items-center justify-center gap-2
                       disabled:opacity-60 disabled:cursor-not-allowed
                       hover:shadow-lg hover:shadow-blue-900/40 active:scale-[0.98]"
                        style={{ background: 'linear-gradient(135deg, #2b8ef7, #1565c0)' }}
                    >
                        {loading ? (
                            <>
                                <svg className="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                                </svg>
                                Signing in…
                            </>
                        ) : 'Sign in'}
                    </button>

                    {/* SSO */}
                    <div className="relative flex items-center gap-3 py-1">
                        <div className="flex-1 h-px bg-white/10" />
                        <span className="text-xs text-gray-500">or</span>
                        <div className="flex-1 h-px bg-white/10" />
                    </div>
                    <button
                        type="button"
                        className="w-full py-2.5 rounded-lg border border-white/10 text-gray-300 text-sm
                       hover:border-white/25 hover:text-white transition-all duration-200
                       flex items-center justify-center gap-2"
                    >
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" /><polyline points="17 8 12 3 7 8" /><line x1="12" y1="3" x2="12" y2="15" /></svg>
                        Sign in with SSO
                    </button>
                </form>
            </div>
        </div>
    )
}
