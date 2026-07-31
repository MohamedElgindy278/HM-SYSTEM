import { createBrowserRouter } from 'react-router-dom';

import Login from '../features/auth/pages/Login';
import ForgotPassword from '../features/auth/pages/ForgotPassword';
import ResetPassword from '../features/auth/pages/ResetPassword';
import ProtectedRoute from './ProtectedRoute';
import MainLayout from '../layouts/MainLayout';
import Dashboard from '../features/dashboard/pages/Dashboard';
import PatientsPage from '../features/patients/pages/PatientsPage';

const protectedLayout = (
  <ProtectedRoute>
    <MainLayout />
  </ProtectedRoute>
);

const router = createBrowserRouter([
  {
    path: '/',
    element: <Login />,
  },
  {
    path: '/forgot-password',
    element: <ForgotPassword />,
  },
  {
    path: '/reset-password',
    element: <ResetPassword />,
  },
  {
    path: '/dashboard',
    element: protectedLayout,
    children: [
      { index: true, element: <Dashboard /> },
      { path: 'patients', element: <PatientsPage /> },
    ],
  },
  {
    path: '/patients',
    element: protectedLayout,
    children: [{ index: true, element: <PatientsPage /> }],
  },
  {
    path: '/patients/create',
    element: protectedLayout,
    children: [{ index: true, element: <PatientsPage /> }],
  },
]);

export default router;
