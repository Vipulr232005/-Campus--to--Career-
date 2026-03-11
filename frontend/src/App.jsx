import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import Login from './pages/Login'
import Register from './pages/Register'
import StudentDashboard from './pages/StudentDashboard'
import FacultyPanel from './pages/FacultyPanel'
import CompanyPortal from './pages/CompanyPortal'
import Jobs from './pages/Jobs'
import { useAuth } from './hooks/useAuth'

function Protected({ children, allowedRoles }) {
  const { user, loading } = useAuth()
  if (loading) return <div>Loading...</div>
  if (!user) return <Navigate to="/login" replace />
  if (allowedRoles && !allowedRoles.includes(user.role)) return <Navigate to="/" replace />
  return children
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/" element={<Layout />}>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={
            <Protected allowedRoles={['student']}>
              <StudentDashboard />
            </Protected>
          } />
          <Route path="faculty" element={
            <Protected allowedRoles={['faculty']}>
              <FacultyPanel />
            </Protected>
          } />
          <Route path="company" element={
            <Protected allowedRoles={['company']}>
              <CompanyPortal />
            </Protected>
          } />
          <Route path="jobs" element={<Jobs />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
