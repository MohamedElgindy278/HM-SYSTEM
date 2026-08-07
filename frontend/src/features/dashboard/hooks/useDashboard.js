import { useQuery } from '@tanstack/react-query';
import { dashboardApi } from '../api/dashboardApi';
import { dashboardKeys } from '../api/queryKeys';

/** يفك الـ envelope ويرجع data فقط */
const selectData = (response) => response?.data ?? response;

export function useDashboardStats() {
  return useQuery({
    queryKey: dashboardKeys.stats(),
    queryFn: () => dashboardApi.getStats(),
    select: selectData,
  });
}

export function useHospitalStatus() {
  return useQuery({
    queryKey: dashboardKeys.hospitalStatus(),
    queryFn: () => dashboardApi.getHospitalStatus(),
    select: selectData,
  });
}

export function useTodayAppointments(page = 1, pageSize = 10) {
  return useQuery({
    queryKey: dashboardKeys.todayAppointments(page, pageSize),
    queryFn: () => dashboardApi.getTodayAppointments(page, pageSize),
    select: selectData,
  });
}

export function useRecentActivity(limit = 10) {
  return useQuery({
    queryKey: dashboardKeys.recentActivity(limit),
    queryFn: () => dashboardApi.getRecentActivity(limit),
    select: selectData,
  });
}

export function usePatientGrowth(period = 'month') {
  return useQuery({
    queryKey: dashboardKeys.patientGrowth(period),
    queryFn: () => dashboardApi.getPatientGrowth(period),
    select: selectData,
  });
}

export function useRevenueAnalytics(period = 'month') {
  return useQuery({
    queryKey: dashboardKeys.revenue(period),
    queryFn: () => dashboardApi.getRevenueAnalytics(period),
    select: selectData,
  });
}

export function useAppointmentsAnalytics(period = 'month') {
  return useQuery({
    queryKey: dashboardKeys.appointmentsAnalytics(period),
    queryFn: () => dashboardApi.getAppointmentsAnalytics(period),
    select: selectData,
  });
}

export function useDepartmentDistribution() {
  return useQuery({
    queryKey: dashboardKeys.departmentDistribution(),
    queryFn: () => dashboardApi.getDepartmentDistribution(),
    select: selectData,
  });
}

export function useBedOccupancy(period = 'month') {
  return useQuery({
    queryKey: dashboardKeys.bedOccupancy(period),
    queryFn: () => dashboardApi.getBedOccupancy(period),
    select: selectData,
  });
}

export function useAdmissionsAnalytics(period = 'month') {
  return useQuery({
    queryKey: dashboardKeys.admissions(period),
    queryFn: () => dashboardApi.getAdmissionsAnalytics(period),
    select: selectData,
  });
}
