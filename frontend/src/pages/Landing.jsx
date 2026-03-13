import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import UnicornScene from 'unicornstudio-react';
import { FileSearch, GraduationCap, ChevronRight, Activity, Users } from 'lucide-react';
import '../index.css';
import './Landing.css';

export default function Landing() {
  // Animation on scroll observer
  useEffect(() => {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('show');
        }
      });
    }, { threshold: 0.1 });

    const hiddenElements = document.querySelectorAll('.fade-up');
    hiddenElements.forEach((el) => observer.observe(el));

    return () => observer.disconnect();
  }, []);

  return (
    <div className="landing-page">
      {/* Navigation */}
      <nav className="landing-nav glass-panel">
        <div className="landing-container flex items-center justify-between">
          <div className="logo-container" style={{ marginBottom: 0 }}>
            <Activity className="logo-icon" size={28} />
            <span className="logo-text">NexusAI Core</span>
          </div>
          <div className="landing-nav-links">
            <Link to="/login" className="btn-secondary">Log In</Link>
            <Link to="/register" className="btn-primary">Get Started</Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-background">
          <UnicornScene
            projectId="Fs3goWzXg4dHI8NjElNv"
            width="100%"
            height="100%"
            scale={1}
            dpi={1.5}
            sdkUrl="https://cdn.jsdelivr.net/gh/hiunicornstudio/unicornstudio.js@2.1.4/dist/unicornStudio.umd.js"
          />
        </div>
        <div className="hero-overlay"></div>
        <div className="landing-container hero-content fade-up">
          <div className="hero-badge badge badge-low">
            <span className="pulse-dot"></span>
            AI-Powered Talent & Student Intelligence
          </div>
          <h1 className="hero-title">
            Hire <span className="text-gradient">Smarter</span>. <br />
            Retain <span className="text-gradient">Better</span>.
            <br />Powered by AI.
          </h1>
          <p className="hero-subtitle">
            One platform for SMEs to screen resumes instantly and for colleges to catch at-risk students before it's too late.
          </p>
          <div className="hero-actions flex gap-4 mt-4">
            <Link to="/company" className="btn-primary" style={{ padding: '16px 32px', fontSize: '1.1rem' }}>
              <FileSearch size={20} />
              Try Resume Screener
              <ChevronRight size={20} />
            </Link>
            <Link to="/dashboard" className="btn-secondary" style={{ padding: '16px 32px', fontSize: '1.1rem', background: 'rgba(255, 255, 255, 0.05)', backdropFilter: 'blur(10px)' }}>
              <GraduationCap size={20} />
              See Student Dashboard
            </Link>
          </div>
        </div>
      </section>

      {/* Problem Statement Section */}
      <section className="problem-section landing-container pt-24 pb-24">
        <div className="section-header text-center fade-up">
          <h2 className="section-title text-gradient">The Problems We're Solving</h2>
          <p className="section-subtitle">Why NexusAI was built for modern institutions and growing businesses.</p>
        </div>

        <div className="dashboard-grid problems-grid mt-4">
          <div className="glass-panel problem-card fade-up" style={{ transitionDelay: '100ms' }}>
            <div className="card-icon-wrapper company-theme">
              <Users size={28} />
            </div>
            <h3>For SMEs</h3>
            <p className="problem-text">
              Small businesses waste <strong>60% of hiring time</strong> reading irrelevant resumes. No HR software. No budget. No time.
            </p>
          </div>

          <div className="glass-panel problem-card fade-up" style={{ transitionDelay: '200ms' }}>
            <div className="card-icon-wrapper student-theme">
              <Activity size={28} />
            </div>
            <h3>For Colleges</h3>
            <p className="problem-text">
              Colleges identify struggling students <strong>only after exams fail</strong>. There's no early warning. No actionable data.
            </p>
          </div>
        </div>
      </section>

      {/* Features Section (Stubbed for now) */}
      <section className="features-section landing-container pb-24 fade-up">
        {/* Features can be added here later */}
      </section>

      {/* Footer */}
      <footer className="landing-footer glass-panel">
        <div className="landing-container flex justify-between items-center" style={{ padding: '24px 0' }}>
          <div className="logo-text" style={{ fontSize: '1rem' }}>NexusAI Core</div>
          <div className="footer-links" style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
            © {new Date().getFullYear()} NexusAI. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
}
