export const dashboardKeys = {
  all: ['dashboard'],

  stats: () => [...dashboardKeys.all, 'stats'],

  hospitalStatus: () => [...dashboardKeys.all, 'hospital-status'],

  todayAppointments: (page, pageSize) => [
    ...dashboardKeys.all,
    'today-appointments',
    { page, pageSize },
  ],

  recentActivity: (limit) => [...dashboardKeys.all, 'recent-activity', { limit }],

  patientGrowth: (period) => [...dashboardKeys.all, 'patient-growth', { period }],

  revenue: (period) => [...dashboardKeys.all, 'revenue', { period }],

  appointmentsAnalytics: (period) => [...dashboardKeys.all, 'appointments-analytics', { period }],

  departmentDistribution: () => [...dashboardKeys.all, 'department-distribution'],

  bedOccupancy: (period) => [...dashboardKeys.all, 'bed-occupancy', { period }],

  admissions: (period) => [...dashboardKeys.all, 'admissions', { period }],
};
