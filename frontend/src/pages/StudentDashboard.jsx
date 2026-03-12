import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api/axios'
import { GraduationCap, Award, CalendarDays, FileText, ChevronRight, AlertCircle, CheckCircle2 } from 'lucide-react'

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

  const riskLevel = risk?.risk_label || 'low'
  const isHighRisk = riskLevel === 'high'
  const riskColor = isHighRisk ? 'var(--danger)' : riskLevel === 'medium' ? 'var(--warning)' : 'var(--success)'

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title text-gradient">Student Dashboard</h1>
        <p className="page-subtitle">Track your performance, risk insights, resume, and job matches.</p>
      </div>

      {/* Top summary cards */}
      <div className="dashboard-grid">
        <div className="glass-panel stat-card" style={{ borderColor: isHighRisk ? 'rgba(239, 68, 68, 0.4)' : '' }}>
          <div className="stat-header">
            <span>ML Risk Prediction</span>
            <AlertCircle color={riskColor} />
          </div>
          <div className="stat-value" style={{ color: riskColor }}>
            {risk ? `${(risk.risk_score * 100).toFixed(1)}%` : '1%'}
          </div>
          <div className="stat-trend" style={{ marginTop: 'auto' }}>
            <span className={`badge ${isHighRisk ? 'badge-high' : riskLevel === 'medium' ? 'badge-medium' : 'badge-low'}`}>
              Status: {risk?.risk_label?.toUpperCase() || 'NORMAL'}
            </span>
          </div>
        </div>

        <div className="glass-panel stat-card">
          <div className="stat-header">
            <span>Current CGPA</span>
            <Award color="var(--primary)" />
          </div>
          <div className="stat-value">{profile?.cgpa ?? '3.8'}</div>
          <div className="stat-trend trend-up">
            <span className="badge badge-low" style={{ background: 'transparent', border: '1px solid var(--border-color)', color: 'var(--text-secondary)' }}>
              {profile?.department || 'Computer Science'}
            </span>
          </div>
        </div>

        <div className="glass-panel stat-card">
          <div className="stat-header">
            <span>Attendance Average</span>
            <CalendarDays color="var(--primary)" />
          </div>
          <div className="stat-value">92%</div>
          <div className="stat-trend trend-up">
            <CheckCircle2 size={14} /> On track
          </div>
        </div>
      </div>

      <div className="page-header" style={{ marginTop: '48px', marginBottom: '24px' }}>
        <h2 style={{ fontSize: '1.5rem' }}>Quick Actions</h2>
      </div>

      <div className="dashboard-grid">
        <button className="glass-panel" style={{ padding: '20px', textAlign: 'left', cursor: 'pointer', display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: 'transparent', border: '1px solid var(--border-color)' }}>
          <div>
            <div style={{ fontWeight: 600, fontSize: '1.1rem', marginBottom: '4px', color: 'var(--text-primary)' }}>Performance AI Review</div>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Why was I flagged for risk?</div>
          </div>
          <ChevronRight color="var(--primary)" />
        </button>

        <button className="glass-panel" style={{ padding: '20px', textAlign: 'left', cursor: 'pointer', display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: 'transparent', border: '1px solid var(--border-color)' }}>
          <div>
            <div style={{ fontWeight: 600, fontSize: '1.1rem', marginBottom: '4px', color: 'var(--text-primary)' }}>Resume Builder</div>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Sync your ATS-friendly profile</div>
          </div>
          <FileText color="var(--primary)" />
        </button>

        <button onClick={() => navigate('/jobs')} className="glass-panel" style={{ padding: '20px', textAlign: 'left', cursor: 'pointer', display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: 'transparent', border: '1px solid var(--border-color)' }}>
          <div>
            <div style={{ fontWeight: 600, fontSize: '1.1rem', marginBottom: '4px', color: 'var(--text-primary)' }}>Jobs & Matches</div>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>See AI-recommended roles</div>
          </div>
          <ChevronRight color="var(--primary)" />
        </button>
      </div>

      <div style={{ marginTop: '48px' }}>
        <div className="glass-panel" style={{ padding: '32px' }}>
          <h2 style={{ fontSize: '1.25rem', marginBottom: '16px' }}>Detailed Analytics</h2>
          <div className="dashboard-grid" style={{ marginBottom: 0 }}>
             <div>
               <h4 style={{ color: 'var(--text-secondary)', marginBottom: '8px' }}>Attendance Records</h4>
               <p>{attendance.length ? `${attendance.length} record(s) logged.` : 'No data in current semester.'}</p>
             </div>
             <div>
               <h4 style={{ color: 'var(--text-secondary)', marginBottom: '8px' }}>Grades Overview</h4>
               <p>{grades.length ? `${grades.length} grade entries found.` : 'Midterms starting soon.'}</p>
             </div>
          </div>
        </div>
      </div>

    </div>
  )
}
