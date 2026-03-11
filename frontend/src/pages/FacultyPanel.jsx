import { useState, useEffect } from 'react'
import api from '../api/axios'

export default function FacultyPanel() {
  const [atRisk, setAtRisk] = useState([])
  const [alerts, setAlerts] = useState([])

  useEffect(() => {
    api.get('/risk/at-risk/').then(({ data }) => setAtRisk(data.results || data)).catch(() => {})
    api.get('/faculty/alerts/').then(({ data }) => setAlerts(data.results || data)).catch(() => {})
  }, [])

  return (
    <div>
      <h1>Faculty Panel — At-Risk Students</h1>
      <section style={{ marginBottom: 24 }}>
        <h2>Students by risk (ML)</h2>
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {(atRisk.length ? atRisk : []).map((s) => (
            <li key={s.id} style={{ padding: '8px 0', borderBottom: '1px solid #eee' }}>
              {s.user_name} · {s.roll_number || '—'} · Risk: {(s.latest_risk ?? 0) * 100}%
            </li>
          ))}
        </ul>
        {!atRisk.length && <p>No risk data yet.</p>}
      </section>
      <section>
        <h2>Alerts</h2>
        <p>{alerts.length ? `${alerts.length} alert(s)` : 'No alerts.'}</p>
      </section>
    </div>
  )
}
