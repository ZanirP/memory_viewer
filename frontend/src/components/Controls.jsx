import { runNextLine, revert, runAll, saveInstructions } from "../api";
import '../App.css';

const Controls = ({ code, triggerUpdate, activeLine, setActiveLine }) => {
  const handleNext = async () => {
    try {
      await runNextLine();
	  setActiveLine(prevLine => prevLine + 1);
      triggerUpdate();    
    } catch (err) {
      console.error("Error in handleNext:", err);
    }
  };

  const handleRevert = async () => {
    try {
      await revert();
	  setActiveLine(prev => Math.max(1, prev - 1));
      triggerUpdate();
    } catch (err) {
      alert('Failed to revert: ' + err.message);
    }
  };

  const handleRunAll = async () => {
    try {
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
      <button className="btn btn-secondary" onClick={handleRevert}>
        ↩ Revert
      </button>
      <button className="btn btn-accent" onClick={handleSave}>
        💾 Save Code
      </button>
    </div>
  );
};

export default Controls;