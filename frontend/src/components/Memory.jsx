import React, { useState, useEffect, useRef } from 'react';
import { getMemory } from '../api';
import '../App.css';

const Memory = ({ refresh, lastChangedAddress }) => {
  const [memory, setMemory] = useState({});
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const activeRowRef = useRef(null);
  const requestIdRef = useRef(0);

  const fetchMemory = async () => {
    const requestId = ++requestIdRef.current;
    try {
      setIsLoading(true);
      setError('');
      const response = await getMemory();
      if (requestId === requestIdRef.current) setMemory(response.data.memory || {});
    } catch (err) {
      if (requestId === requestIdRef.current) setError(err.response?.data?.detail || err.message);
    } finally {
      if (requestId === requestIdRef.current) setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchMemory();
  }, [refresh]);

  // Smoothly scroll to the updated memory row whenever lastChangedAddress changes
  useEffect(() => {
    if (activeRowRef.current) {
      activeRowRef.current.scrollIntoView({
        behavior: 'smooth',
        block: 'nearest',
      });
    }
  }, [lastChangedAddress, memory]);

  return (
    <div className="memory-container">
      <h3>Memory</h3>
      {isLoading && <div role="status">Loading memory…</div>}
      {error && <div role="alert">Failed to load memory: {error}</div>}
      <div className="memory-table-container">
        <table className="memory-table">
          <thead>
            <tr>
              <th>Address</th>
              <th>Value</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(memory).map(([address, value]) => {
              const isChanged = lastChangedAddress !== null && address.toUpperCase() === String(lastChangedAddress).toUpperCase();
              return (
                <tr 
                  key={address} 
                  ref={isChanged ? activeRowRef : null} // Attach ref if changed
                  className={isChanged ? "pulse-highlight" : ""}
                >
                  <td>{address}</td>
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

export default Memory;
