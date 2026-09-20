// Central API base URL configuration.
// In production (AWS), set VITE_API_BASE in your Amplify environment variables.
// Locally, it defaults to http://localhost:8000.
export const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';
