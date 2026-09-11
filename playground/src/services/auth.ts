const AUTH_STORAGE_KEY = 'vue-login-playground:authenticated'

export interface LoginCredentials {
  username: string
  password: string
}

export function login(credentials: LoginCredentials): boolean {
  const isValid = credentials.username === 'admin' && credentials.password === 'vue3'

  if (!isValid)
    return false

  window.localStorage.setItem(AUTH_STORAGE_KEY, 'true')
  return true
}

export function logout(): void {
  window.localStorage.removeItem(AUTH_STORAGE_KEY)
}

export function isAuthenticated(): boolean {
  return window.localStorage.getItem(AUTH_STORAGE_KEY) === 'true'
}
