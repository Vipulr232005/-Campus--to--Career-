import { useState, useEffect } from 'react'
import api from '../api/axios'

export default function CompanyPortal() {
  const [jobs, setJobs] = useState([])

  useEffect(() => {
    api.get('/companies/jobs/').then(({ data }) => setJobs(data.results || data)).catch(() => {})
  }, [])

  const runScreening = (jobId) => {
    api.post(`/screener/job/${jobId}/run/`).then(({ data }) => alert(`Ranked ${data.applications_ranked} applications`)).catch((e) => alert(e.response?.data?.detail || 'Failed'))
  }

  return (
    <div>
      <h1>Company Portal</h1>
      <h2>Your jobs</h2>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {(jobs.length ? jobs : []).map((j) => (
          <li key={j.id} style={{ padding: 12, marginBottom: 8, background: '#fff', borderRadius: 8, boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
            <strong>{j.title}</strong> · {j.job_type}
            <div style={{ marginTop: 8 }}>
              <a href={`#/jobs/${j.id}/applications`}>View applications</a>
              {' · '}
              <button type="button" onClick={() => runScreening(j.id)}>Run AI screening</button>
            </div>
          </li>
        ))}
      </ul>
      {!jobs.length && <p>No jobs posted yet.</p>}
    </div>
  )
}
