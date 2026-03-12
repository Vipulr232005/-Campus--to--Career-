import { useState } from 'react'
import { Outlet, NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'

export default function Layout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [open, setOpen] = useState(false)

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const go = (to) => {
    setOpen(false)
    navigate(to)
  }

  const goAndScroll = (to, hashId) => {
    setOpen(false)
    navigate(to)
    // allow route to render, then scroll
    setTimeout(() => {
      const el = document.getElementById(hashId)
      if (el) el.scrollIntoView({ behavior: 'smooth' })
    }, 50)
  }

  return (
    <div className="app-shell">
      <header className="app-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <NavLink to="/" className="app-header__title" style={{ textDecoration: 'none', color: 'inherit' }}>
            Campus to Career
          </NavLink>
        </div>
        {user && (
          <>
            <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: 10 }}>
              <span style={{ fontSize: 13 }}>{user.username} · {user.role}</span>
              <button
                type="button"
                onClick={handleLogout}
                style={{
                  padding: '6px 12px',
                  borderRadius: 999,
                  border: 'none',
                  background: 'rgba(255,255,255,0.9)',
                  cursor: 'pointer',
                  fontSize: 13,
                }}
              >
                Logout
              </button>
              <button
                type="button"
                className="hamburger-btn"
                onClick={() => setOpen((v) => !v)}
                aria-label="Open navigation"
              >
                <span className="hamburger-lines" />
              </button>
            </div>
            {open && (
              <div className="hamburger-menu">
                {user.role === 'student' && (
                  <>
                    <div className="hamburger-menu__groupTitle">Student</div>
                    <button onClick={() => go('/dashboard')}>Dashboard</button>
                    <button onClick={() => goAndScroll('/dashboard', 'attendance')}>Attendance</button>
                    <button onClick={() => goAndScroll('/dashboard', 'grades')}>Grades</button>
                    <button onClick={() => goAndScroll('/dashboard', 'assignments')}>Assignments</button>
                    <button onClick={() => goAndScroll('/dashboard', 'risk')}>Risk & Explain</button>
                    <button onClick={() => goAndScroll('/dashboard', 'resume')}>Resume Builder</button>
                  </>
                )}
                {user.role === 'faculty' && (
                  <>
                    <div className="hamburger-menu__groupTitle">Faculty</div>
                    <button onClick={() => go('/faculty')}>At‑risk students</button>
                    <button onClick={() => go('/faculty')}>Alerts</button>
                  </>
                )}
                {user.role === 'company' && (
                  <>
                    <div className="hamburger-menu__groupTitle">Company</div>
                    <button onClick={() => go('/company')}>Company portal</button>
                  </>
                )}
                <div className="hamburger-menu__groupTitle">Jobs</div>
                <button onClick={() => go('/jobs')}>Browse jobs</button>
              </div>
            )}
          </>
        )}
      </header>
      <main className="app-main">
        <Outlet />
      </main>
    </div>
  )
}
