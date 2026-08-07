export default function Card({ children, hoverable = false, className = '', ...rest }) {
  return (
    <div className={`card${hoverable ? ' hoverable' : ''} ${className}`.trim()} {...rest}>
      {children}
    </div>
  );
}
