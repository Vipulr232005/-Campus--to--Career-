import { useState } from 'react'
import { useNavigate, NavLink } from 'react-router-dom'
import api from '../api/axios'
import { UserPlus } from 'lucide-react'

const ROLES = [
  { value: 'student', label: 'Student' },
  { value: 'faculty', label: 'Faculty' },
  { value: 'company', label: 'Company' },
]

export default function Register() {
  const [form, setForm] = useState({ username: '', email: '', password: '', first_name: '', last_name: '', role: 'student', phone: '', company_name: '', department: '' })
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleChange = (e) => {
    setForm((f) => ({ ...f, [e.target.name]: e.target.value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      await api.post('/auth/register/', form)
      navigate('/login')
    } catch (err) {
      const data = err.response && err.response.data
      if (!data) {
        setError('Registration failed. Is the backend running?')
        return
      }
      if (typeof data === 'string') {
        setError(data)
        return
      }
      if (data.detail) {
        setError(data.detail)
        return
      }
      const parts = []
      for (const [field, messages] of Object.entries(data)) {
        const msg = Array.isArray(messages) ? messages.join(' ') : messages
        parts.push(`${field}: ${msg}`)
      }
      setError(parts.length ? parts.join(' · ') : 'Registration failed')
    }
  }

  const inputStyle = {
    width: '100%', 
    padding: '12px 16px', 
    background: 'rgba(0,0,0,0.2)', 
    border: '1px solid var(--border-color)', 
    borderRadius: 'var(--radius-md)', 
    color: 'white', 
    fontSize: '0.95rem', 
    outline: 'none'
  }

  const labelStyle = {
    display: 'block', 
    marginBottom: '8px', 
    fontSize: '0.85rem', 
    color: 'var(--text-secondary)'
  }

  return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '100vh', padding: '24px' }}>
      <div className="glass-panel" style={{ maxWidth: 500, width: '100%', padding: '40px', display: 'flex', flexDirection: 'column' }}>
        <div style={{ textAlign: 'center', marginBottom: '32px' }}>
          <div className="pulse-ring" style={{ width: 64, height: 64, margin: '0 auto 16px', borderRadius: '50%', background: 'var(--surface-color)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--primary)' }}>
            <UserPlus size={32} />
          </div>
          <h1 className="text-gradient" style={{ fontSize: '2rem', marginBottom: '8px' }}>Create Account</h1>
          <p style={{ color: 'var(--text-secondary)' }}>Get started with NexusAI Core</p>
        </div>

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div style={{ display: 'flex', gap: '16px' }}>
            <div style={{ flex: 1 }}>
              <label style={labelStyle}>First Name</label>
              <input name="first_name" value={form.first_name} onChange={handleChange} style={inputStyle} />
            </div>
            <div style={{ flex: 1 }}>
              <label style={labelStyle}>Last Name</label>
              <input name="last_name" value={form.last_name} onChange={handleChange} style={inputStyle} />
            </div>
          </div>

          <div>
            <label style={labelStyle}>Username</label>
            <input name="username" value={form.username} onChange={handleChange} required style={inputStyle} />
          </div>

          <div>
            <label style={labelStyle}>Email</label>
            <input name="email" type="email" value={form.email} onChange={handleChange} required style={inputStyle} />
          </div>

          <div>
            <label style={labelStyle}>Password</label>
            <input name="password" type="password" value={form.password} onChange={handleChange} required minLength={8} style={inputStyle} />
          </div>

          <div style={{ display: 'flex', gap: '16px' }}>
            <div style={{ flex: 1 }}>
              <label style={labelStyle}>Phone</label>
              <input name="phone" value={form.phone} onChange={handleChange} style={inputStyle} />
            </div>
            <div style={{ flex: 1 }}>
              <label style={labelStyle}>Role</label>
              <select name="role" value={form.role} onChange={handleChange} style={{ ...inputStyle, background: 'rgba(15, 23, 18, 0.9)' }}>
                {ROLES.map((r) => <option key={r.value} value={r.value}>{r.label}</option>)}
              </select>
            </div>
          </div>

          {form.role === 'company' && (
            <div>
              <label style={labelStyle}>Company Name</label>
              <input name="company_name" value={form.company_name} onChange={handleChange} style={inputStyle} required />
            </div>
          )}

          {form.role === 'faculty' && (
            <div>
              <label style={labelStyle}>Department</label>
              <input name="department" value={form.department} onChange={handleChange} style={inputStyle} required />
            </div>
          )}

          {error && <div style={{ background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.2)', padding: '12px', borderRadius: '8px', color: '#ef4444', fontSize: '0.9rem', marginTop: '8px' }}>{error}</div>}

          <button type="submit" className="btn-primary" style={{ width: '100%', justifyContent: 'center', padding: '14px', fontSize: '1rem', marginTop: '16px' }}>
            Register Now
          </button>
        </form>

        <p style={{ marginTop: '32px', textAlign: 'center', color: 'var(--text-secondary)', fontSize: '0.95rem' }}>
          Already have an account? <NavLink to="/login" style={{ color: 'var(--primary)', textDecoration: 'none', fontWeight: 600 }}>Sign in</NavLink>
        </p>
      </div>
    </div>
  )
}
