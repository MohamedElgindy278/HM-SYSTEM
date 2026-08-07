import api from '../../../services/api';

export const dashboardApi = {
  getStats: () => api.get('/dashboard/stats'),

  getHospitalStatus: () => api.get('/dashboard/hospital-status'),

  getTodayAppointments: (page = 1, pageSize = 10) =>
    api.get('/dashboard/today-appointments', {
      params: { start_num: page, page_size: pageSize },
    }),

  getRecentActivity: (limit = 5) => api.get('/dashboard/recent-activity', { params: { limit } }),

  getPatientGrowth: (period = 'month') =>
    api.get('/dashboard/patient-growth', { params: { period } }),

  getRevenueAnalytics: (period = 'month') =>
    api.get('/dashboard/revenue-analytics', { params: { period } }),

  getAppointmentsAnalytics: (period = 'month') =>
    api.get('/dashboard/appointments-analytics', { params: { period } }),

  getDepartmentDistribution: () => api.get('/dashboard/department-distribution'),

  getBedOccupancy: (period = 'month') =>
    api.get('/dashboard/bed-occupancy', { params: { period } }),

  getAdmissionsAnalytics: (period = 'month') =>
    api.get('/dashboard/admissions-analytics', { params: { period } }),
};

export default dashboardApi;
