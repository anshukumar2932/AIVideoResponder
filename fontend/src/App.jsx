import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import LandingPage from './pages/LandingPage'
import LoginPage from './pages/LoginPage'
import ChoicePage from './pages/ChoicePage'
import TextHelpPage from './pages/TextHelpPage'
import VideoHelpPage from './pages/VideoHelpPage'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/choice" element={<ChoicePage />} />
        <Route path="/text-help" element={<TextHelpPage />} />
        <Route path="/video-help" element={<VideoHelpPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
