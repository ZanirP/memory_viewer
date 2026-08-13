import axios from 'axios';

const API_BASE_URL = 
  import.meta.env.DEV
    ? 'http://localhost:8000' 
    : window.location.origin;

const SESSION_KEY = 'memory-viewer-session-id';
let sessionId = sessionStorage.getItem(SESSION_KEY);
if (!sessionId) {
  sessionId = crypto.randomUUID();
  sessionStorage.setItem(SESSION_KEY, sessionId);
}
  
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'X-Session-ID': sessionId },
});


export const saveInstructions = async (instructions) => {
  return api.post('/save', { instructions });
};

export const runNextLine = async () => {
  return api.post('/run-next-line');
}

export const revert = async () => {
  return api.post('/revert');
}

export const reset = async () => {
  return api.post('/reset');
}

export const runAll = async () => {
  return api.post('/run-all');
}

export const getRegisters = async () => {
  return api.get('/registers');
}

export const getMemory = async () => {
  return api.get('/memory');
}

export const getCache = async () => {
  return api.get('/cache');
}

export const getProgram = async () => {
  return api.get('/program');
}

export default api;
