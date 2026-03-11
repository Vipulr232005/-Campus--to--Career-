import { useState, useEffect } from 'react'
import api from '../api/axios'

export default function Jobs() {
  const [jobs, setJobs] = useState([])

  useEffect(() => {
    api.get('/companies/jobs/').then(({ data }) => setJobs(data.results || data)).catch(() => {})
  }, [])

  return (
    <div>
      <h1>Job listings</h1>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {(jobs.length ? jobs : []).map((j) => (
          <li key={j.id} style={{ padding: 16, marginBottom: 8, background: '#fff', borderRadius: 8, boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
            <strong>{j.title}</strong> · {j.company_name} · {j.job_type}
            <p style={{ margin: '8px 0', color: '#555', fontSize: 14 }}>{j.description?.slice(0, 200)}…</p>
          </li>
        ))}
      </ul>
      {!jobs.length && <p>No jobs available.</p>}
    </div>
  )
}
