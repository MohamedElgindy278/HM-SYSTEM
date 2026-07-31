import { useApiQuery } from '../../../hooks/useApiQuery';
import { useApiMutation } from '../../../hooks/useApiMutation';
import { patientApi } from '../api/patientApi';

export function usePatientsList(startNum = 1, pageSize = 20) {
  return useApiQuery(() => patientApi.getAll(startNum, pageSize));
}

export function usePatient(patientId) {
  return useApiQuery(() => patientApi.getById(patientId), {
    enabled: !!patientId,
  });
}

export function useCreatePatient() {
  return useApiMutation((data) => patientApi.create(data));
}

export function useUpdatePatient() {
  return useApiMutation((patientId, data) => patientApi.update(patientId, data));
}

export function useDeletePatient() {
  return useApiMutation((patientId) => patientApi.remove(patientId));
}
