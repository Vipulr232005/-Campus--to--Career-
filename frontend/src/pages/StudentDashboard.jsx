import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api/axios'

export default function StudentDashboard() {
  const [profile, setProfile] = useState(null)
  const [risk, setRisk] = useState(null)
  const [attendance, setAttendance] = useState([])
  const [grades, setGrades] = useState([])
  const navigate = useNavigate()

  useEffect(() => {
    api.get('/students/profile/').then((r) => setProfile(r.data)).catch(() => {})
    api.get('/risk/my-risk/').then((r) => setRisk(r.data)).catch(() => {})
    api.get('/students/attendance/').then((r) => setAttendance(r.data.results || r.data)).catch(() => {})
    api.get('/students/grades/').then((r) => setGrades(r.data.results || r.data)).catch(() => {})
  }, [])

  const riskClass =
    !risk ? '' : risk.risk_label === 'high'
      ? 'risk-card--high'
      : risk.risk_label === 'medium'
      ? 'risk-card--medium'
      : 'risk-card--low'

  return (
    <div>
      <h1 style={{ marginTop: 0, marginBottom: 8 }}>Student Dashboard</h1>
      <p style={{ marginTop: 0, color: 'var(--text-muted)', fontSize: 14 }}>
        One place for your performance, risk insights, resume and jobs.
      </p>

      {/* Top summary cards */}
      <div className="card-grid">
        <div className={`card ${riskClass}`}>
          <div className="card__title">Dropout risk (ML)</div>
          <div className="card__value">
            {risk ? `${(risk.risk_score * 100).toFixed(1)}%` : '—'}
          </div>
          <div style={{ marginTop: 8 }}>
            {risk && (
              <span className="card__pill">
                Status: {risk.risk_label?.toUpperCase()}
              </span>
            )}
          </div>
        </div>

        <div className="card">
          <div className="card__title">CGPA</div>
          <div className="card__value">{profile?.cgpa ?? '—'}</div>
          <div style={{ marginTop: 8 }}>
            <span className="card__pill">
              {profile?.department || 'No department'}
            </span>
          </div>
        </div>

        <div className="card">
          <div className="card__title">Attendance records</div>
          <div className="card__value">{attendance.length}</div>
          <div style={{ marginTop: 8 }}>
            <span className="card__pill">
              {grades.length} grade entries
            </span>
          </div>
        </div>
      </div>

      {/* Navigation chips to each feature */}
      <h2 style={{ marginTop: 24, marginBottom: 12 }}>Go to</h2>
      <div className="card-grid">
        <button
          type="button"
          className="btn-chip"
          onClick={() => document.getElementById('attendance')?.scrollIntoView({ behavior: 'smooth' })}
        >
          <span>
            <div className="btn-chip__label">Attendance</div>
            <div className="btn-chip__sub">View your daily presence and trends</div>
          </span>
          <span>›</span>
        </button>

        <button
          type="button"
          className="btn-chip"
          onClick={() => document.getElementById('grades')?.scrollIntoView({ behavior: 'smooth' })}
        >
          <span>
            <div className="btn-chip__label">Grades</div>
            <div className="btn-chip__sub">Per course / semester performance</div>
          </span>
          <span>›</span>
        </button>

        <button
          type="button"
          className="btn-chip"
          onClick={() => document.getElementById('assignments')?.scrollIntoView({ behavior: 'smooth' })}
        >
          <span>
            <div className="btn-chip__label">Assignments</div>
            <div className="btn-chip__sub">Deadlines and submissions</div>
          </span>
          <span>›</span>
        </button>

        <button
          type="button"
          className="btn-chip"
          onClick={() => document.getElementById('risk')?.scrollIntoView({ behavior: 'smooth' })}
        >
          <span>
            <div className="btn-chip__label">Risk & Explainability</div>
            <div className="btn-chip__sub">Why you were flagged or not</div>
          </span>
          <span>›</span>
        </button>

        <button
          type="button"
          className="btn-chip"
          onClick={() => document.getElementById('resume')?.scrollIntoView({ behavior: 'smooth' })}
        >
          <span>
            <div className="btn-chip__label">Resume Builder</div>
            <div className="btn-chip__sub">ATS‑friendly profile → resume</div>
          </span>
          <span>›</span>
        </button>

        <button
          type="button"
          className="btn-chip"
          onClick={() => navigate('/jobs')}
        >
          <span>
            <div className="btn-chip__label">Jobs & Matches</div>
            <div className="btn-chip__sub">See postings for you</div>
          </span>
          <span>›</span>
        </button>
      </div>

      {/* Section anchors */}
      <section id="attendance" style={{ marginTop: 32 }}>
        <h2>Attendance</h2>
        <p style={{ color: 'var(--text-muted)' }}>
          {attendance.length ? `${attendance.length} record(s).` : 'No attendance data yet.'}
        </p>
      </section>

      <section id="grades" style={{ marginTop: 24 }}>
        <h2>Grades</h2>
        <p style={{ color: 'var(--text-muted)' }}>
          {grades.length ? `${grades.length} record(s).` : 'No grades yet.'}
        </p>
      </section>

      <section id="assignments" style={{ marginTop: 24 }}>
        <h2>Assignments</h2>
        <p style={{ color: 'var(--text-muted)' }}>
          Coming soon: per‑course assignment list and status.
        </p>
      </section>

      <section id="risk" style={{ marginTop: 24 }}>
        <h2>Risk explainability</h2>
        <p style={{ color: 'var(--text-muted)', fontSize: 13 }}>
          This will use the explainability API to show which features (attendance, grades,
          assignments) contributed to your current risk score.
        </p>
      </section>

      <section id="resume" style={{ marginTop: 24 }}>
        <h2>Resume Builder</h2>
        <p style={{ color: 'var(--text-muted)' }}>
          A dedicated form here can sync with your profile and let you export a resume PDF.
        </p>
      </section>
    </div>
  )
}
