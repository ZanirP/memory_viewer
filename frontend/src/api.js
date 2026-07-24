import axios from 'axios';

const API_BASE_URL = 
  process.env.NODE_ENV === 'development' 
    ? 'http://localhost:8000' 
    : window.location.origin;
  
const api = axios.create({
  baseURL: API_BASE_URL,
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

export default api;