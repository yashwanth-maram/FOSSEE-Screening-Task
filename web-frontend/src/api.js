import axios from "axios";

const api = axios.create({
  baseURL: "https://chemical-equipment-backend-g7ls.onrender.com",
  withCredentials: true,
});

// CSRF handling
api.interceptors.request.use((config) => {
  const csrfToken = document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrftoken="))
    ?.split("=")[1];

  if (csrfToken) {
    config.headers["X-CSRFToken"] = csrfToken;
  }

  return config;
});

export default api;
