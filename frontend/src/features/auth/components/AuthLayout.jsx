import AuthBrandPanel from './BrandPanel';

export default function AuthLayout({ children }) {
  return (
    <div className="login-screen">
      <AuthBrandPanel />

      {children}
    </div>
  );
}
