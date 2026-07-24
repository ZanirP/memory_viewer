import React, { useState, useEffect } from 'react';
import { getRegisters } from '../api';
import '../App.css';

const Registers = ({ refresh, lastChangedRegister = 'X0' }) => { // Defaults to 'X0' for testing visuals!
  const [registers, setRegisters] = useState({});

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