import { useState, useEffect } from 'react'
import api from '../api/axios'

export default function StudentDashboard() {
  const [profile, setProfile] = useState(null)
  const [risk, setRisk] = useState(null)
  const [attendance, setAttendance] = useState([])
  const [grades, setGrades] = useState([])

  useEffect(() => {
    api.get('/students/profile/').then((r) => setProfile(r.data)).catch(() => {})
    api.get('/risk/my-risk/').then((r) => setRisk(r.data)).catch(() => {})
    api.get('/students/attendance/').then((r) => setAttendance(r.data.results || r.data)).catch(() => {})
    api.get('/students/grades/').then((r) => setGrades(r.data.results || r.data)).catch(() => {})
  }, [])

  return (
    <div>
      <h1>Student Dashboard</h1>
      {profile && (
        <section style={{ marginBottom: 24 }}>
          <h2>Profile</h2>
          <p><strong>Name:</strong> {profile.user_name} · <strong>Roll:</strong> {profile.roll_number || '—'} · <strong>Dept:</strong> {profile.department || '—'} · <strong>CGPA:</strong> {profile.cgpa ?? '—'}</p>
        </section>
      )}
      {risk && (
        <section style={{ marginBottom: 24, padding: 16, background: risk.risk_label === 'high' ? '#ffebee' : risk.risk_label === 'medium' ? '#fff3e0' : '#e8f5e9', borderRadius: 8 }}>
          <h2>Dropout risk</h2>
          <p><strong>Score:</strong> {(risk.risk_score * 100).toFixed(1)}% · <strong>Label:</strong> {risk.risk_label}</p>
          {risk.features && <pre style={{ fontSize: 12 }}>{JSON.stringify(risk.features, null, 2)}</pre>}
        </section>
      )}
      <section style={{ marginBottom: 24 }}>
        <h2>Attendance</h2>
        <p>{attendance.length ? attendance.length + ' record(s)' : 'No records yet.'}</p>
      </section>
      <section>
        <h2>Grades</h2>
        <p>{grades.length ? grades.length + ' record(s)' : 'No records yet.'}</p>
      </section>
    </div>
  )
}
