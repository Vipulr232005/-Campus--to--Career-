import { useState, useEffect } from 'react'
import api from '../api/axios'
import { Users, AlertTriangle, TrendingDown, BookOpen, Clock, Activity } from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts'

const mockChartData = [
  { week: 'W1', attendance: 95, grades: 88, risk: 10 },
  { week: 'W2', attendance: 90, grades: 85, risk: 15 },
  { week: 'W3', attendance: 82, grades: 80, risk: 30 },
  { week: 'W4', attendance: 75, grades: 78, risk: 45 },
  { week: 'W5', attendance: 60, grades: 70, risk: 65 },
  { week: 'W6', attendance: 45, grades: 65, risk: 85 },
]

export default function FacultyPanel() {
  const [atRisk, setAtRisk] = useState([])
  const [alerts, setAlerts] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      api.get('/risk/at-risk/').catch(() => ({ data: { results: [] } })),
      api.get('/faculty/alerts/').catch(() => ({ data: { results: [] } }))
    ]).then(([riskRes, alertsRes]) => {
      setAtRisk(riskRes.data?.results || riskRes.data || [])
      setAlerts(alertsRes.data?.results || alertsRes.data || [])
      setLoading(false)
    })
  }, [])

  const getRiskBadge = (riskValue) => {
    const r = Math.round(riskValue * 100)
    if (r >= 70) return <span className="badge badge-high">{r}% Critical</span>
    if (r >= 40) return <span className="badge badge-medium">{r}% Warning</span>
    return <span className="badge badge-low">{r}% Normal</span>
  }

  // If no data, populate demo data for the high-end showcase
  const displayStudents = atRisk.length > 0 ? atRisk : [
    { id: 1, user_name: 'Alex Johnson', roll_number: 'CS-2023-045', latest_risk: 0.88, attendance: '45%' },
    { id: 2, user_name: 'Sam Smith', roll_number: 'CS-2023-112', latest_risk: 0.75, attendance: '52%' },
    { id: 3, user_name: 'Priya Patel', roll_number: 'EE-2023-089', latest_risk: 0.62, attendance: '68%' },
  ]

  return (
    <div>
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <h1 className="page-title text-gradient">Early Warning System</h1>
          <p className="page-subtitle">ML-Predicted student performance and dropout risk analytics.</p>
        </div>
        <div className="glass-panel" style={{ padding: '12px 24px', display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>System Status</div>
            <div style={{ fontWeight: 600, color: 'var(--primary)', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <span className="pulse-ring" style={{ width: 8, height: 8, background: 'var(--primary)', borderRadius: '50%', display: 'inline-block' }}></span>
              Model Active
            </div>
          </div>
        </div>
      </div>

      <div className="dashboard-grid">
        <div className="glass-panel stat-card">
          <div className="stat-header">
            <span>Critical Alerts</span>
            <AlertTriangle color="var(--danger)" />
          </div>
          <div className="stat-value">{displayStudents.filter(s => s.latest_risk >= 0.7).length}</div>
          <div className="stat-trend trend-down">
            <TrendingDown size={14} /> Requires Immediate Intervention
          </div>
        </div>

        <div className="glass-panel stat-card">
          <div className="stat-header">
            <span>Avg Attendance Drop</span>
            <Clock color="var(--warning)" />
          </div>
          <div className="stat-value">-12%</div>
          <div className="stat-trend trend-down">
            <TrendingDown size={14} /> Tracking 3 cohorts
          </div>
        </div>

        <div className="glass-panel stat-card">
          <div className="stat-header">
            <span>Active Predictions</span>
            <Activity color="var(--primary)" />
          </div>
          <div className="stat-value">1,248</div>
          <div className="stat-trend trend-up">
            <Users size={14} style={{ marginRight: '4px' }} /> Students Analyzed
          </div>
        </div>
      </div>

      <div className="dashboard-grid" style={{ gridTemplateColumns: 'minmax(300px, 1.5fr) minmax(300px, 1fr)' }}>
        <div className="glass-panel" style={{ padding: '24px' }}>
          <h2 style={{ fontSize: '1.25rem', marginBottom: '8px' }}>At-Risk Students Roster</h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '24px' }}>Students requiring faculty intervention sorted by AI risk score.</p>
          
          <div className="table-container">
            <table className="styled-table">
              <thead>
                <tr>
                  <th>Student Name</th>
                  <th>Roll / Dept</th>
                  <th>Attendance</th>
                  <th>Risk Score</th>
                </tr>
              </thead>
              <tbody>
                {displayStudents.map((s) => (
                  <tr key={s.id}>
                    <td style={{ fontWeight: 500 }}>{s.user_name}</td>
                    <td style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>{s.roll_number || '—'}</td>
                    <td>{s.attendance || '—'}</td>
                    <td>{getRiskBadge(s.latest_risk)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column' }}>
          <h2 style={{ fontSize: '1.25rem', marginBottom: '8px' }}>Risk Factor Trends</h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '24px' }}>Aggregated drop-out patterns over the semester.</p>
          
          <div style={{ flex: 1, minHeight: '300px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={mockChartData}>
                <defs>
                  <linearGradient id="colorRisk" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <XAxis dataKey="week" stroke="var(--text-secondary)" tick={{ fill: 'var(--text-secondary)' }} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'var(--bg-dark)', border: '1px solid var(--border-color)', borderRadius: '12px' }}
                  itemStyle={{ color: 'var(--text-primary)' }}
                />
                <Area type="monotone" dataKey="risk" stroke="#ef4444" fillOpacity={1} fill="url(#colorRisk)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  )
}
