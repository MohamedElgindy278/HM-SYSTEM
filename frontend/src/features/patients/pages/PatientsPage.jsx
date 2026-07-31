import { useMemo } from 'react';

import { usePatientsList } from '../hooks/usePatients';

export default function PatientsPage() {
  const { data, loading, error } = usePatientsList(1, 20);

  const patients = useMemo(() => data?.items ?? data?.data ?? [], [data]);

  return (
    <section className="card table-card">
      <div className="table-toolbar">
        <div>
          <h1 className="table-title">Patients</h1>
          <p className="form-hint">Browse and manage patient records.</p>
        </div>
      </div>

      <div className="table-wrap">
        {loading && <p className="form-hint">Loading patients…</p>}
        {error && <p className="form-error">{error}</p>}

        {!loading && !error && patients.length === 0 && (
          <p className="form-hint" style={{ padding: '18px 20px' }}>
            No patients were returned by the API yet.
          </p>
        )}

        {!loading && !error && patients.length > 0 && (
          <table>
            <thead>
              <tr>
                <th>Patient</th>
                <th>Identifier</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {patients.map((patient) => (
                <tr key={patient.id ?? patient.patient_id ?? patient.patientId ?? patient.name}>
                  <td>
                    <div className="cell-person">
                      <div className="mini-avatar">{patient.name?.charAt(0) ?? 'P'}</div>
                      <div>
                        <div className="person-name">{patient.name ?? 'Unknown patient'}</div>
                        <div className="person-sub">{patient.phone ?? patient.contact ?? 'No contact info'}</div>
                      </div>
                    </div>
                  </td>
                  <td>{patient.identifier ?? patient.patient_id ?? patient.id ?? '—'}</td>
                  <td>
                    <span className="badge b-info">
                      <span className="bdot" />
                      {patient.status ?? 'Active'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </section>
  );
}
