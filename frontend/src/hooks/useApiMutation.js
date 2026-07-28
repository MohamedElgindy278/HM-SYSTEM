import { useState, useCallback } from 'react';

function extractErrorMessage(err) {
  return err?.message || 'Something went wrong. Please try again.';
}

export function useApiMutation(mutationFn) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const mutate = useCallback(
    async (...args) => {
      setLoading(true);
      setError(null);

      try {
        const response = await mutationFn(...args);
        return response.data;
      } catch (err) {
        setError(extractErrorMessage(err));
        throw err;
      } finally {
        setLoading(false);
      }
    },
    [mutationFn]
  );

  const reset = useCallback(() => setError(null), []);

  return { mutate, loading, error, reset };
}

export default useApiMutation;
