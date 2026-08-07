/**
 * Extracts a clean, human-readable message from any axios/API error.
 * Matches the backend's AppException shape:
 *   { response: { data: { detail: { message } } } }
 * Used everywhere an error needs to be shown to the user - hooks, pages,
 * forms alike - so the extraction logic exists in exactly one place.
 */
export function extractErrorMessage(err) {
  return (
    err?.response?.data?.detail?.message ||
    err?.response?.data?.message ||
    err?.message ||
    'Something went wrong. Please try again.'
  );
}
