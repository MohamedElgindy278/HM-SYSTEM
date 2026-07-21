function getGreeting() {
  const hour = new Date().getHours();
  if (hour < 12) return 'Good Morning';
  if (hour < 17) return 'Good Afternoon';
  return 'Good Evening';
}

export default function Header({ name = '' }) {
  return (
    <div className="welcome">
      <h1 className="welcome-title">
        {getGreeting()}, {name} <span className="wave">👋</span>
      </h1>
    </div>
  );
}
