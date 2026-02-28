import Header from '../components/Header'
import HeroSection from '../components/HeroSection'

export default function LandingPage() {
    return (
        <main id="main-content">
            <a href="#main-content" className="skip-link">Skip to content</a>
            <Header />
            <HeroSection />
        </main>
    )
}
