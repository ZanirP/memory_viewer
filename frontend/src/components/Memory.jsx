import { useState, useEffect } from 'react';
import { getMemory } from '../api';
import '../App.css';

const Memory = ({ refresh, lastChangedAddress = '0' }) => {
  const [memory, setMemory] = useState({});

  const fetchMemory = async () => {
    try {
      const response = await getMemory();
      setMemory(response.data.memory || {});
    } catch (err) {
      alert('Failed to fetch memory ' + err.message);
    }
  };

  useEffect(() => {
    fetchMemory();
  }, [refresh]);

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