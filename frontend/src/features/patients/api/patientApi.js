import api from '../../../services/api';

export const patientApi = {
  getAll: (startNum = 1, pageSize = 20) =>
    api.get('/patients', { params: { start_num: startNum, page_size: pageSize } }),

  getById: (patientId) => api.get(`/patients/${patientId}`),

  create: (data) => api.post('/patients', data),

  update: (patientId, data) => api.put(`/patients/${patientId}`, data),

  remove: (patientId) => api.delete(`/patients/${patientId}`),
};

export default patientApi;
