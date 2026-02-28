import { useNavigate } from 'react-router-dom'
import { useState, useRef } from 'react'

export default function VideoHelpPage() {
    const navigate = useNavigate()
    const [videoUrl, setVideoUrl] = useState(null)
    const [loading, setLoading] = useState(false)
    const [isRecording, setIsRecording] = useState(false)
    const [audioBlob, setAudioBlob] = useState(null)
    const [userText, setUserText] = useState('')
    const [response, setResponse] = useState('')
    const [error, setError] = useState('')
    const mediaRecorderRef = useRef(null)
    const audioChunksRef = useRef([])

    const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
            mediaRecorderRef.current = new MediaRecorder(stream)
            audioChunksRef.current = []

            mediaRecorderRef.current.ondataavailable = (event) => {
                audioChunksRef.current.push(event.data)
            }

            mediaRecorderRef.current.onstop = () => {
                const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' })
                setAudioBlob(audioBlob)
                stream.getTracks().forEach(track => track.stop())
            }

            mediaRecorderRef.current.start()
            setIsRecording(true)
            setError('')
        } catch (err) {
            setError('Could not access microphone. Please check permissions.')
            console.error('Error accessing microphone:', err)
        }
    }

    const stopRecording = () => {
        if (mediaRecorderRef.current && isRecording) {
            mediaRecorderRef.current.stop()
            setIsRecording(false)
        }
    }

    const processAudio = async () => {
        if (!audioBlob) {
            setError('No audio recorded')
            return
        }

        setLoading(true)
        setError('')

        try {
            const formData = new FormData()
            formData.append('audio', audioBlob, 'recording.wav')

            const response = await fetch(`${API_BASE_URL}/support`, {
                method: 'POST',
                body: formData
            })

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`)
            }

            const data = await response.json()
            console.log("Backend response:", data)

            if (data.error) {
                setError(data.error)
            } else {
                setUserText(data.user_text)
                setResponse(data.response)
                
                // Handle video response
                if (data.video_available && data.video_url) {
                    const videoUrl = `${API_BASE_URL}${data.video_url}?t=${new Date().getTime()}`
                    console.log("Setting video URL:", videoUrl)
                    setVideoUrl(videoUrl)
                } else {
                    // Show message about video availability
                    console.log("Video not available:", data.video_message)
                    if (data.video_message) {
                        setError(`Video: ${data.video_message}`)
                    }
                }
            }
        } catch (err) {
            setError(`Failed to process audio: ${err.message}`)
            console.error('Error processing audio:', err)
        } finally {
            setLoading(false)
        }
    }

    const resetSession = () => {
        setVideoUrl(null)
        setAudioBlob(null)
        setUserText('')
        setResponse('')
        setError('')
    }

    return (
        <div className="min-h-screen flex flex-col items-center justify-center px-6 text-center"
            style={{ background: 'linear-gradient(135deg, #0f0f20 0%, #120a2e 100%)' }}>

            <div className="relative z-10 max-w-2xl animate-slide-up">
                <h1 className="text-3xl font-bold text-white mb-6">
                    Video AI Assistant
                </h1>

                {/* Error Display */}
                {error && (
                    <div className="mb-4 p-3 bg-red-500/20 border border-red-500/30 rounded-lg text-red-300 text-sm">
                        {error}
                    </div>
                )}

                {/* User Input Display */}
                {userText && (
                    <div className="mb-4 p-3 bg-blue-500/20 border border-blue-500/30 rounded-lg text-left">
                        <p className="text-blue-300 text-sm font-medium">You said:</p>
                        <p className="text-white">{userText}</p>
                    </div>
                )}

                {/* AI Response Display */}
                {response && (
                    <div className="mb-4 p-3 bg-green-500/20 border border-green-500/30 rounded-lg text-left">
                        <p className="text-green-300 text-sm font-medium">AI Response:</p>
                        <p className="text-white">{response}</p>
                    </div>
                )}

                {/* Video Display */}
                <div className="glass-card rounded-2xl overflow-hidden mb-8"
                    style={{ aspectRatio: '16/9' }}>

                    {videoUrl ? (
                        <video
                            src={videoUrl}
                            autoPlay
                            controls
                            className="w-full h-full object-cover"
                            onError={(e) => {
                                console.error('Video error:', e)
                                setError('Failed to load video')
                            }}
                        />
                    ) : (
                        <div className="w-full h-full flex items-center justify-center text-gray-400">
                            {loading ? (
                                <div className="flex flex-col items-center">
                                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-500 mb-2"></div>
                                    <p>Processing your request...</p>
                                </div>
                            ) : (
                                "Record your question to get AI video response"
                            )}
                        </div>
                    )}
                </div>

                {/* Recording Controls */}
                <div className="flex gap-3 justify-center mb-4">
                    {!isRecording ? (
                        <button
                            onClick={startRecording}
                            disabled={loading}
                            className="px-5 py-2.5 rounded-xl bg-red-600 hover:bg-red-700 text-white disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2">
                            🎤 Start Recording
                        </button>
                    ) : (
                        <button
                            onClick={stopRecording}
                            className="px-5 py-2.5 rounded-xl bg-red-800 hover:bg-red-900 text-white flex items-center gap-2 animate-pulse">
                            ⏹️ Stop Recording
                        </button>
                    )}

                    {audioBlob && !loading && (
                        <button
                            onClick={processAudio}
                            className="px-5 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-700 text-white">
                            🚀 Get AI Response
                        </button>
                    )}

                    {(videoUrl || userText) && (
                        <button
                            onClick={resetSession}
                            className="px-5 py-2.5 rounded-xl border border-white/20 text-white hover:bg-white/10">
                            🔄 New Question
                        </button>
                    )}
                </div>

                {/* Instructions */}
                <div className="text-sm text-gray-400 mb-6">
                    {!audioBlob && !isRecording && "Click 'Start Recording' and ask your question"}
                    {isRecording && "Speak your question clearly, then click 'Stop Recording'"}
                    {audioBlob && !loading && "Click 'Get AI Response' to process your question"}
                    {loading && "Please wait while we process your request..."}
                </div>

                <button onClick={() => navigate('/choice')}
                    className="text-gray-400 hover:text-white transition-colors">
                    ← Back to options
                </button>
            </div>
        </div>
    )
}