import axios from 'axios'

const axiosInstance = axios.create({
  baseURL: process.env.API_BASE_URL,
  headers: {
    common: {
      'Content-Type': 'application/vnd.api+json',
    }
  },
  data: {},  // this is necessary to get custom header to work. see axios/#86
});

// every request will have the API's bearer token inserted into the headers
axiosInstance.interceptors.request.use(function (config) {
  const token = localStorage.getItem('token');

  if (token) {
    config.headers.common.Authorization = 'Bearer' + ' ' + token.replace(/['"]+/g, '');
  }

  return config;
});

export default axiosInstance;
