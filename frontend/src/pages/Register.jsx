import { useState } from 'react'
import { useNavigate, NavLink } from 'react-router-dom'
import api from '../api/axios'

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
        setError('Registration failed. Is the backend running at http://localhost:8000?')
        return
      }
      // DRF returns { "field": ["message"], ... } or { "detail": "..." }
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

  return (
    <div style={{ maxWidth: 420, margin: '48px auto', padding: 24, background: '#fff', borderRadius: 8, boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
      <h1 style={{ marginTop: 0 }}>Register</h1>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: 10 }}>
          <label>Username</label>
          <input name="username" value={form.username} onChange={handleChange} required style={{ width: '100%', padding: 8 }} />
        </div>
        <div style={{ marginBottom: 10 }}>
          <label>Email</label>
          <input name="email" type="email" value={form.email} onChange={handleChange} required style={{ width: '100%', padding: 8 }} />
        </div>
        <div style={{ marginBottom: 10 }}>
          <label>Password</label>
          <input name="password" type="password" value={form.password} onChange={handleChange} required minLength={8} style={{ width: '100%', padding: 8 }} />
        </div>
        <div style={{ marginBottom: 10 }}>
          <label>First name</label>
          <input name="first_name" value={form.first_name} onChange={handleChange} style={{ width: '100%', padding: 8 }} />
        </div>
        <div style={{ marginBottom: 10 }}>
          <label>Last name</label>
          <input name="last_name" value={form.last_name} onChange={handleChange} style={{ width: '100%', padding: 8 }} />
        </div>
        <div style={{ marginBottom: 10 }}>
          <label>Role</label>
          <select name="role" value={form.role} onChange={handleChange} style={{ width: '100%', padding: 8 }}>
            {ROLES.map((r) => <option key={r.value} value={r.value}>{r.label}</option>)}
          </select>
        </div>
        <div style={{ marginBottom: 10 }}>
          <label>Phone</label>
          <input name="phone" value={form.phone} onChange={handleChange} style={{ width: '100%', padding: 8 }} />
        </div>
        {form.role === 'company' && (
          <div style={{ marginBottom: 10 }}>
            <label>Company name</label>
            <input name="company_name" value={form.company_name} onChange={handleChange} style={{ width: '100%', padding: 8 }} />
          </div>
        )}
        {form.role === 'faculty' && (
          <div style={{ marginBottom: 10 }}>
            <label>Department</label>
            <input name="department" value={form.department} onChange={handleChange} style={{ width: '100%', padding: 8 }} />
          </div>
        )}
        {error && <p style={{ color: 'crimson', marginBottom: 12 }}>{error}</p>}
        <button type="submit" style={{ width: '100%', padding: 10 }}>Register</button>
      </form>
      <p style={{ marginTop: 16 }}><NavLink to="/login">Login</NavLink></p>
    </div>
  )
}
