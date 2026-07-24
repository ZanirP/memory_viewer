import React, { useState, useEffect, useRef } from 'react';
import { getMemory } from '../api';
import '../App.css';

const Memory = ({ refresh, lastChangedAddress = '0' }) => {
  const [memory, setMemory] = useState({});
  const activeRowRef = useRef(null);

  const fetchMemory = async () => {
    try {
      const response = await getMemory();
      setMemory(response.data.memory || {});
    } catch (err) {
      console.log("Failed to fetch memory", err);
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
              const isChanged = String(address) === String(lastChangedAddress);
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