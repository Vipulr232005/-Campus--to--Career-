import { useState, useEffect } from 'react'
import { Outlet, NavLink, useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import { LayoutDashboard, Users, GraduationCap, Briefcase, FileSearch, LogOut, Sparkles } from 'lucide-react'

export default function Layout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const navItems = []

  if (user) {
    if (user.role === 'student') {
      navItems.push({ name: 'Dashboard', path: '/dashboard', icon: <LayoutDashboard size={20} /> })
      navItems.push({ name: 'My Performance', path: '/dashboard#grades', icon: <GraduationCap size={20} /> })
    }
    
    if (user.role === 'faculty') {
      navItems.push({ name: 'Early Warning System', path: '/faculty', icon: <Users size={20} /> })
    }

    if (user.role === 'company') {
      navItems.push({ name: 'AI Resume Screener', path: '/company', icon: <FileSearch size={20} /> })
    }

    navItems.push({ name: 'Jobs', path: '/jobs', icon: <Briefcase size={20} /> })
  }

  return (
    <div className="app-layout">
      {user && (
        <aside className="sidebar">
          <div className="logo-container">
            <Sparkles className="logo-icon" size={28} />
            <span className="logo-text">NexusAI Core</span>
          </div>

          <nav className="nav-menu">
            {navItems.map((item) => {
              const isActive = location.pathname === item.path || (location.pathname === '/' && item.path === '/dashboard')
              return (
                <NavLink
                  key={item.name}
                  to={item.path}
                  className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
                  onClick={(e) => {
                    if (item.path.includes('#')) {
                      e.preventDefault()
                      navigate(item.path.split('#')[0])
                      setTimeout(() => {
                        const el = document.getElementById(item.path.split('#')[1])
                        if (el) el.scrollIntoView({ behavior: 'smooth' })
                      }, 50)
                    }
                  }}
                >
                  {item.icon}
                  {item.name}
                </NavLink>
              )
            })}
          </nav>

          <div style={{ marginTop: 'auto' }}>
            <div className="glass-panel" style={{ padding: '16px', marginBottom: '16px' }}>
              <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '4px' }}>Logged in as</div>
              <div style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{user.username}</div>
              <div className="badge badge-low" style={{ display: 'inline-block', marginTop: '8px', fontSize: '0.65rem' }}>{user.role}</div>
            </div>

            <button
              onClick={handleLogout}
              className="nav-link"
              style={{ width: '100%', background: 'transparent', cursor: 'pointer', border: '1px solid var(--danger)', color: 'var(--danger)' }}
            >
              <LogOut size={20} />
              Sign Out
            </button>
          </div>
        </aside>
      )}

      <main className="main-content">
        <Outlet />
      </main>
    </div>
  )
}
