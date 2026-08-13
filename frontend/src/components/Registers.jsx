import React, { useState, useEffect, useRef } from 'react';
import { getRegisters } from '../api';
import '../App.css';

const Registers = ({ refresh, lastChangedRegister }) => {
  const [registers, setRegisters] = useState({});
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const activeRowRef = useRef(null);
  const requestIdRef = useRef(0);

  const fetchRegisters = async () => {
    const requestId = ++requestIdRef.current;
    try {
      setIsLoading(true);
      setError('');
      const response = await getRegisters();
      if (requestId === requestIdRef.current) setRegisters(response.data.registers || {});
    } catch (err) {
      if (requestId === requestIdRef.current) setError(err.response?.data?.detail || err.message);
    } finally {
      if (requestId === requestIdRef.current) setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchRegisters();
  }, [refresh]);

  // Smoothly scroll to the updated register row whenever lastChangedRegister changes
  useEffect(() => {
    if (activeRowRef.current) {
      activeRowRef.current.scrollIntoView({
        behavior: 'smooth',
        block: 'nearest',
      });
    }
  }, [lastChangedRegister, registers]);

  return (
    <div className="registers-container">
      <h3>Registers</h3>
      {isLoading && <div role="status">Loading registers…</div>}
      {error && <div role="alert">Failed to load registers: {error}</div>}
      <div className="registers-table-container">
        <table className="registers-table">
          <thead>
            <tr>
              <th>Register</th>
              <th>Value</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(registers).map(([register, value]) => {
              const isChanged = lastChangedRegister && register.toUpperCase() === String(lastChangedRegister).toUpperCase();
              return (
                <tr 
                  key={register} 
                  ref={isChanged ? activeRowRef : null} // Attach ref if changed
                  className={isChanged ? "pulse-highlight" : ""}
                >
                  <td>{register}</td>
                  <td>{value}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Registers;
