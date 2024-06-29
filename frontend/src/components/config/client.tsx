import axios from 'axios';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

export const currency_api_url = import.meta.env.VITE_CURRENCY_API_URL;

export const client_currency = axios.create({
  baseURL: currency_api_url,
  withCredentials: true,
});
