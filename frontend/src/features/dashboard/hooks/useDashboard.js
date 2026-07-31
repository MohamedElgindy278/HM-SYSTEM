import { useApiQuery } from '../../../hooks/useApiQuery';
import { dashboardApi } from '../api/dashboardApi';

export function useDashboardStats() {
  return useApiQuery(() => dashboardApi.getStats());
}

export function useHospitalStatus() {
  return useApiQuery(() => dashboardApi.getHospitalStatus());
}

export function useTodayAppointments(startNum = 1, pageSize = 10) {
  return useApiQuery(() => dashboardApi.getTodayAppointments(startNum, pageSize));
}

export function useRecentActivity(limit = 10) {
  return useApiQuery(() => dashboardApi.getRecentActivity(limit));
}

export function usePatientGrowth(period = 'month') {
  return useApiQuery(() => dashboardApi.getPatientGrowth(period));
}

export function useRevenueAnalytics(period = 'month') {
  return useApiQuery(() => dashboardApi.getRevenueAnalytics(period));
}

export function useAppointmentsAnalytics(period = 'month') {
  return useApiQuery(() => dashboardApi.getAppointmentsAnalytics(period));
}

export function useDepartmentDistribution() {
  return useApiQuery(() => dashboardApi.getDepartmentDistribution());
}

export function useBedOccupancy(period = 'month') {
  return useApiQuery(() => dashboardApi.getBedOccupancy(period));
}

export function useAdmissionsAnalytics(period = 'month') {
  return useApiQuery(() => dashboardApi.getAdmissionsAnalytics(period));
}
