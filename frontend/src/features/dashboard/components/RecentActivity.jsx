import { UserPlus, CheckCircle2, FilePlus2, FlaskConical, CreditCard } from 'lucide-react';

const ACTIVITY = [
  {
    id: 1,
    icon: UserPlus,
    iconBg: '#EFF6FF',
    iconColor: '#2563EB',
    text: (
      <>
        <b>Patient Registered</b> — Rana Youssef was added to the system
      </>
    ),
    time: '6 minutes ago',
  },
  {
    id: 2,
    icon: CheckCircle2,
    iconBg: '#ECFDF5',
    iconColor: '#047857',
    text: (
      <>
        <b>Appointment Completed</b> — Hany Kamal with Dr. Sarah Ahmed
      </>
    ),
    time: '22 minutes ago',
  },
  {
    id: 3,
    icon: FilePlus2,
    iconBg: '#EFF6FF',
    iconColor: '#2563EB',
    text: (
      <>
        <b>Prescription Created</b> — Dr. Khaled Hassan for Laila Mostafa
      </>
    ),
    time: '40 minutes ago',
  },
  {
    id: 4,
    icon: FlaskConical,
    iconBg: '#FFFBEB',
    iconColor: '#B45309',
    text: (
      <>
        <b>Lab Result Uploaded</b> — Blood panel for John Doe is ready for review
      </>
    ),
    time: '1 hour ago',
  },
  {
    id: 5,
    icon: CreditCard,
    iconBg: '#ECFDF5',
    iconColor: '#047857',
    text: (
      <>
        <b>Payment Completed</b> — $420 received from Ahmed Sami
      </>
    ),
    time: '1 hour ago',
  },
];

export default function RecentActivity() {
  return (
    <>
      <h2 className="section-title">Recent Activity</h2>
      <div className="card">
        <div className="timeline">
          {ACTIVITY.map((item, index) => {
            const Icon = item.icon;
            return (
              <div className="t-item" key={item.id}>
                <div className="t-dot" style={{ background: item.iconBg, color: item.iconColor }}>
                  <Icon size={15} strokeWidth={2} />
                </div>
                <div className="t-body">
                  <div className="t-text">{item.text}</div>
                  <div className="t-time">{item.time}</div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </>
  );
}
