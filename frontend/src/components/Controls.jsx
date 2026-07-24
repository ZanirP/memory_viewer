import { runNextLine, revert, runAll, saveInstructions } from "../api";
import React, { useState } from 'react';
import '../App.css';

const Controls = ({ code, triggerUpdate, activeLine, setActiveLine }) => {
  const [canRevert, setCanRevert] = useState(false);
  const handleNext = async () => {
    try {

      if (activeLine === 1) {
        await saveInstructions(code.split("\n"));
      }
      const response = await runNextLine();
	  const {changedRegister, changedAddress} = response.data;
	  setActiveLine(prevLine => prevLine + 1);
    setCanRevert(true);
	  triggerUpdate(changedRegister, changedAddress);
	}   
    catch (err) {
      console.error("Error in handleNext:", err);
    }
  };

  const handleRevert = async () => {
    try {
      const response = await revert();
	  const {changedRegister, changedAddress} = response.data;
	  setActiveLine(prev => Math.max(1, prev - 1));
    setCanRevert(false);
      triggerUpdate();
    } catch (err) {
      alert('Failed to revert: ' + err.message);
    }
  };

  const handleRunAll = async () => {
    try {
      if (activeLine === 1) {
        await saveInstructions(code.split("\n"));
      }
      await runAll();
	  const totalLines = code.split("\n").length;
	  setActiveLine(totalLines);
      triggerUpdate();
    } catch (err) {
      alert('Failed to run all: ' + err.message);
    }
  };

  const handleSave = async () => {
    if (!code) {
      alert("No instructions to save");
      return;
    }
    try {
      await saveInstructions(code.split("\n"));
	  setActiveLine(1);
    setCanRevert(false);
      triggerUpdate();
      alert('Instructions saved!');
    } catch (err) {
      alert('Failed to save instructions: ' + err.message);
    }
  };

  return (
    <div className="controls-toolbar">
      <button className="btn btn-primary" onClick={handleNext}>
        ▶ Step Next
      </button>
      <button className="btn btn-secondary" onClick={handleRunAll}>
        ⏩ Run All
      </button>
      <button className="btn btn-secondary" onClick={handleRevert} disabled={!canRevert || activeLine <= 1}>
        ↩ Revert
      </button>
      <button className="btn btn-accent" onClick={handleSave}>
        💾 Save Code
      </button>
    </div>
  );
};

export default Controls;