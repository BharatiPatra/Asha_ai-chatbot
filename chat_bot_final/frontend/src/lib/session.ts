const SESSION_KEY = "session_id";
const SESSION_TIMEOUT_MINUTES = 30;

export const getSessionId = (): string | null => {
  const raw = localStorage.getItem(SESSION_KEY);
  if (!raw) return null;

  try {
    const parsed = JSON.parse(raw);
    const now = Date.now();
    const ageInMinutes = (now - parsed.timestamp) / (1000 * 60);

    if (ageInMinutes > SESSION_TIMEOUT_MINUTES) {
      localStorage.removeItem(SESSION_KEY);
      return null;
    }

    return parsed.sessionId;
  } catch (e) {
    console.error("Invalid session data in localStorage", e);
    localStorage.removeItem(SESSION_KEY);
    return null;
  }
};

export const setSessionId = (sessionId: string): void => {
  const sessionData = {
    sessionId,
    timestamp: Date.now(),
  };
  localStorage.setItem(SESSION_KEY, JSON.stringify(sessionData));
};

export const clearSessionId = (): void => {
  localStorage.removeItem(SESSION_KEY);
};
