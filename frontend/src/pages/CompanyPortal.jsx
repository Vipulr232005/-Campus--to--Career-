import { useState, useEffect } from 'react'
import api from '../api/axios'
import { FileSearch, Briefcase, Zap, CheckCircle2, ChevronRight, XCircle } from 'lucide-react'

export default function CompanyPortal() {
  const [jobs, setJobs] = useState([])
  const [loading, setLoading] = useState(true)
  const [screeningId, setScreeningId] = useState(null)

  useEffect(() => {
    api.get('/companies/jobs/')
      .then(({ data }) => {
        setJobs(data.results || data)
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [])

  const runScreening = async (jobId) => {
    setScreeningId(jobId)
    try {
      const { data } = await api.post(`/screener/job/${jobId}/run/`)
      setTimeout(() => {
        alert(`Successfully ranked ${data.applications_ranked} applications with AI`)
        setScreeningId(null)
      }, 1500)
    } catch (e) {
      alert(e.response?.data?.detail || 'Failed to run AI Screening')
      setScreeningId(null)
    }
  }

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title text-gradient">AI-Powered Resume Screener</h1>
        <p className="page-subtitle">Automatically rank and shortlist candidates using our advanced explainable AI engine.</p>
      </div>

      <div className="dashboard-grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))' }}>
        {loading && <div className="glass-panel" style={{ padding: '24px' }}>Loading job listings...</div>}
        
        {!loading && jobs.length === 0 && (
          <div className="glass-panel" style={{ padding: '48px', textAlign: 'center' }}>
            <Briefcase size={48} color="var(--text-secondary)" style={{ margin: '0 auto 16px' }} />
            <h3 style={{ marginBottom: '8px' }}>No Active Postings</h3>
            <p className="page-subtitle">Publish your first job description to start receiving and screening resumes.</p>
          </div>
        )}

        {jobs.map((job) => (
          <div key={job.id} className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '20px' }}>
              <div>
                <h3 style={{ fontSize: '1.25rem', marginBottom: '4px' }}>{job.title}</h3>
                <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                  <span className="badge badge-low">{job.job_type || 'Full Time'}</span>
                  <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>ID: #{job.id}</span>
                </div>
              </div>
              <div className="pulse-ring" style={{ width: '40px', height: '40px', background: 'var(--surface-color-hover)', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--primary)' }}>
                <FileSearch size={20} />
              </div>
            </div>

            <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '24px', flex: 1 }}>
              Leverage the Explainable AI engine to score all submitted applications against the core requirements for exactly what you need.
            </div>

            <div style={{ display: 'flex', gap: '12px', marginTop: 'auto' }}>
              <button 
                className="btn-primary" 
                onClick={() => runScreening(job.id)}
                disabled={screeningId === job.id}
                style={{ flex: 1, justifyContent: 'center', opacity: screeningId === job.id ? 0.7 : 1 }}
              >
                {screeningId === job.id ? (
                  <>
                    <Zap className="spin" size={18} />
                    Analyzing Resumes...
                  </>
                ) : (
                  <>
                    <Zap size={18} />
                    Run AI Screening
                  </>
                )}
              </button>
              
              <a 
                href={`#/jobs/${job.id}/applications`} 
                className="btn-secondary" 
                style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', textDecoration: 'none' }}
              >
                <ChevronRight size={20} />
              </a>
            </div>
          </div>
        ))}

      </div>

      <div style={{ marginTop: '40px' }}>
        <h2 style={{ fontSize: '1.5rem', marginBottom: '16px' }}>How it Works</h2>
        <div className="dashboard-grid">
          <div className="glass-panel" style={{ padding: '24px' }}>
            <CheckCircle2 color="var(--primary)" size={32} style={{ marginBottom: '16px' }} />
            <h4 style={{ marginBottom: '8px' }}>1. Conceptual Mapping</h4>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Our AI reads your job description and extracts the core skills, experience, and nuanced requirements needed for the role.</p>
          </div>
          <div className="glass-panel" style={{ padding: '24px' }}>
            <Zap color="var(--primary)" size={32} style={{ marginBottom: '16px' }} />
            <h4 style={{ marginBottom: '8px' }}>2. Semantic Matching</h4>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Candidates are scored not just on keywords, but on the contextual value of their past experiences.</p>
          </div>
          <div className="glass-panel" style={{ padding: '24px' }}>
            <FileSearch color="var(--primary)" size={32} style={{ marginBottom: '16px' }} />
            <h4 style={{ marginBottom: '8px' }}>3. Explainable Shortlisting</h4>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Get transparent reasoning for every score so you can trust the AI's recommendations.</p>
          </div>
        </div>
      </div>
    </div>
  )
}
