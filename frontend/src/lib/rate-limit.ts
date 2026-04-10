const STORAGE_KEY = "onramp_doc_count"
export const SESSION_LIMIT = 10

export function getSessionCount(): number {
  return parseInt(sessionStorage.getItem(STORAGE_KEY) ?? "0", 10)
}

export function incrementSessionCount(): number {
  const next = getSessionCount() + 1
  sessionStorage.setItem(STORAGE_KEY, String(next))
  return next
}

export function isSessionLimitReached(): boolean {
  return getSessionCount() >= SESSION_LIMIT
}
