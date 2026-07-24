import React, { useState, useEffect, useRef } from 'react';
import { getRegisters } from '../api';
import '../App.css';

const Registers = ({ refresh, lastChangedRegister = 'X0' }) => {
  const [registers, setRegisters] = useState({});
  const activeRowRef = useRef(null);

  const fetchRegisters = async () => {
    try {
      const response = await getRegisters();
      setRegisters(response.data.registers || {});
    } catch (err) {
      console.log("Failed to fetch registers", err);
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
              const isChanged = register === lastChangedRegister;
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