// Contains the buttons for trigger execution
import {runNextLine, revert, runAll, saveInstructions} from "../api";
import { getRegisters, getMemory } from "../api";


const Controls = ({ code, triggerUpdate}) => {
    const handleNext = async () => {
        try {
            console.log("Running next line");
            await runNextLine();
			console.log("Triggering update");
			triggerUpdate();	
		} catch (err) {
            console.error("Error in handleNext:", err);
        }
    };

  const handleRevert = async () => {
	try {
		console.log("Reverting");
	  await revert();
	  triggerUpdate();
	} catch (err) {
	  alert('Failed to revert' + err.message);
	}
  };

  const handleRunAll = async () => {
	try {
	  await runAll();
	  triggerUpdate();
	} catch (err) {
	  alert('Failed to run all' + err.message);
	}
  };
const handleSave = async () => {
	if (!code){
		alert("No instructions to save");
		return;
	}
	try{
		await saveInstructions(code.split("\n"));
		triggerUpdate();
		alert('Instructions saved');
	}
	catch(err){
		console.error("Save failed: ", err)
		alert('Failed to save instructions' + err.message);
	}
};

  return (
	<div className="controls">
	  <button onClick={handleNext}>Next</button>
	  <button onClick={handleRevert}>Revert</button>
	  <button onClick={handleRunAll}>Run All</button>
	  <button onClick={handleSave}>Save</button>
	</div>
  );
}

export default Controls;