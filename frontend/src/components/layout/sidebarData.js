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
  DoorOpen,
  DoorClosed,
  ListOrdered,
} from 'lucide-react';

export const sidebarItems = [
  {
    section: 'Main',
    items: [
      {
        title: 'Home',
        icon: LayoutDashboard,
        path: '/dashboard',
        permission: null,
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
        permission: 'patient:read',
      },
      {
        title: 'Doctors',
        icon: Stethoscope,
        path: '/doctors',
        permission: 'doctor:read',
      },
      {
        title: 'Nurses',
        icon: UserRound,
        path: '/nurses',
        permission: null,
      },
      {
        title: 'Departments',
        icon: Building2,
        path: '/departments',
        permission: 'department:read',
      },
      {
        title: 'Wards',
        icon: BedDouble,
        path: '/wards',
        permission: null,
      },
      {
        title: 'Clinics',
        icon: DoorOpen,
        path: '/clinics',
        permission: 'clinic:read',
      },
      {
        title: 'Rooms',
        icon: DoorClosed,
        path: '/rooms',
        permission: 'room:read',
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
        permission: 'appointment:read',
      },
      {
        title: 'Patient Queue',
        icon: ListOrdered,
        path: '/patient-queue',
        permission: 'patient_queue:read',
      },
      {
        title: 'Encounters',
        icon: ClipboardList,
        path: '/encounters',
        permission: null,
      },
      {
        title: 'Prescriptions',
        icon: Pill,
        path: '/prescriptions',
        permission: null,
      },
      {
        title: 'Medical Records',
        icon: FileText,
        path: '/medical-records',
        permission: null,
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
        permission: null,
      },
      {
        title: 'Payments',
        icon: CreditCard,
        path: '/payments',
        permission: null,
      },
      {
        title: 'Reports',
        icon: Activity,
        path: '/reports',
        permission: null,
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
        permission: 'user:read',
      },
      {
        title: 'Settings',
        icon: Settings,
        path: '/settings',
        permission: null,
      },
    ],
  },
];

export function getVisibleSidebarItems(userPermissions = []) {
  const permissionSet = new Set(userPermissions);

  return sidebarItems
    .map((section) => ({
      ...section,
      items: section.items.filter(
        (item) => item.permission === null || permissionSet.has(item.permission)
      ),
    }))
    .filter((section) => section.items.length > 0);
}

export function getPageTitle(pathname) {
  for (const section of sidebarItems) {
    const item = section.items.find((item) => item.path === pathname);

    if (item) {
      return item.title;
    }
  }

  return 'Dashboard';
}
