import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000'
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