import { useState, useEffect, useCallback, useRef } from 'react';

/**
 * Generic hook for fetching data from the backend.
 *
 * Every service already returns:
 * {
 *   status_code,
 *   message,
 *   data
 * }
 *
 * So this hook never deals with AxiosResponse.
 */

const defaultTransform = (response) => response.data;

function extractErrorMessage(error) {
  return error?.message || 'Something went wrong. Please try again.';
}

export function useApiQuery(fetcher, deps = [], options = {}) {
  const { enabled = true, transform = defaultTransform } = options;

  const [data, setData] = useState(null);

  const [loading, setLoading] = useState(enabled);

  const [error, setError] = useState(null);

  const isMounted = useRef(true);

  const run = useCallback(async () => {
    if (!enabled) {
      setLoading(false);
      return;
    }

    setLoading(true);

    setError(null);

    try {
      const response = await fetcher();

      if (!isMounted.current) return;

      setData(transform(response));
    } catch (err) {
      if (!isMounted.current) return;

      setError(extractErrorMessage(err));
    } finally {
      if (isMounted.current) {
        setLoading(false);
      }
    }
  }, deps);

  useEffect(() => {
    isMounted.current = true;

    run();

    return () => {
      isMounted.current = false;
    };
  }, [run]);

  return {
    data,
    loading,
    error,
    refetch: run,
  };
}

export default useApiQuery;
