import {
  LayoutDashboard,
  Users,
  UserRound,
  Stethoscope,
  BriefcaseMedical,
  CalendarDays,
  Pill,
  ClipboardList,
  BedDouble,
  CreditCard,
  Building2,
  ShieldCheck,
  Settings,
  Activity,
  FileText,
} from 'lucide-react';

export const sidebarItems = [
  {
    section: 'Main',
    items: [
      {
        title: 'Dashboard',
        icon: LayoutDashboard,
        path: '/',
      },
    ],
  },

  {
    section: 'Hospital',
    items: [
      {
        title: 'Patients',
        icon: Users,
        path: '/patients',
      },
      {
        title: 'Doctors',
        icon: Stethoscope,
        path: '/doctors',
      },
      {
        title: 'Nurses',
        icon: UserRound,
        path: '/nurses',
      },
      {
        title: 'Departments',
        icon: Building2,
        path: '/departments',
      },
      {
        title: 'Wards',
        icon: BedDouble,
        path: '/wards',
      },
    ],
  },

  {
    section: 'Clinical',
    items: [
      {
        title: 'Appointments',
        icon: CalendarDays,
        path: '/appointments',
      },
      {
        title: 'Encounters',
        icon: ClipboardList,
        path: '/encounters',
      },
      {
        title: 'Prescriptions',
        icon: Pill,
        path: '/prescriptions',
      },
      {
        title: 'Medical Records',
        icon: FileText,
        path: '/medical-records',
      },
    ],
  },

  {
    section: 'Administration',
    items: [
      {
        title: 'Employees',
        icon: BriefcaseMedical,
        path: '/employees',
      },
      {
        title: 'Payments',
        icon: CreditCard,
        path: '/payments',
      },
      {
        title: 'Reports',
        icon: Activity,
        path: '/reports',
      },
    ],
  },

  {
    section: 'System',
    items: [
      {
        title: 'Roles & Permissions',
        icon: ShieldCheck,
        path: '/roles',
      },
      {
        title: 'Settings',
        icon: Settings,
        path: '/settings',
      },
    ],
  },
];

export function getPageTitle(pathname) {
  for (const section of sidebarItems) {
    const item = section.items.find((item) => item.path === pathname);

    if (item) {
      return item.title;
    }
  }

  return 'Dashboard';
}
