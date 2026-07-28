import AuthBrandPanel from './BrandPanel';

import './AuthLayout.css'
import './Form.css'

export default function AuthLayout({ children }) {
  return (
    <div className="login-screen">
      <AuthBrandPanel />

      {children}
    </div>
  );
}
