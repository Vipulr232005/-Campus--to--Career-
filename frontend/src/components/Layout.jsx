import { Outlet, NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'

export default function Layout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <header style={{ padding: '12px 24px', background: '#1a1a2e', color: '#eee', display: 'flex', alignItems: 'center', gap: '24px' }}>
        <NavLink to="/" style={{ color: 'inherit', textDecoration: 'none', fontWeight: 700 }}>Campus to Career</NavLink>
        {user && (
          <>
            {user.role === 'student' && <NavLink to="/dashboard" style={({ isActive }) => ({ color: 'inherit', textDecoration: 'none', opacity: isActive ? 1 : 0.8 })}>Dashboard</NavLink>}
            {user.role === 'faculty' && <NavLink to="/faculty" style={({ isActive }) => ({ color: 'inherit', textDecoration: 'none', opacity: isActive ? 1 : 0.8 })}>Faculty</NavLink>}
            {user.role === 'company' && <NavLink to="/company" style={({ isActive }) => ({ color: 'inherit', textDecoration: 'none', opacity: isActive ? 1 : 0.8 })}>Company</NavLink>}
            <NavLink to="/jobs" style={({ isActive }) => ({ color: 'inherit', textDecoration: 'none', opacity: isActive ? 1 : 0.8 })}>Jobs</NavLink>
            <span style={{ marginLeft: 'auto' }}>{user.username} ({user.role})</span>
            <button type="button" onClick={handleLogout} style={{ padding: '6px 12px', cursor: 'pointer' }}>Logout</button>
          </>
        )}
      </header>
      <main style={{ flex: 1, padding: 24 }}>
        <Outlet />
      </main>
    </div>
  )
}
