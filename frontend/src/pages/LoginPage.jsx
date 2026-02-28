import { useNavigate } from 'react-router-dom'
import LoginModal from '../components/LoginModal'

export default function LoginPage() {
    const navigate = useNavigate()
    return (
        <div className="min-h-screen flex items-center justify-center"
            style={{ background: 'linear-gradient(135deg, #0f0f20 0%, #0d1a2e 100%)' }}>
            <LoginModal
                onClose={() => navigate(-1)}
                onSuccess={() => navigate('/choice')}
            />
        </div>
    )
}
