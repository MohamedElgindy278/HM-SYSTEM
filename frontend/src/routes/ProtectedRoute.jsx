import { Navigate } from 'react-router-dom';
import { useAuth } from '../features/auth/context/AuthContext';
import { Loading } from '../components/ui';

function ProtectedRoute({ children }) {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <Loading size="lg" label="Loading..." fullHeight />;
  }

  if (!isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  return children;
}

export default ProtectedRoute;
