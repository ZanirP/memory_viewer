// Contains the buttons for trigger execution
import {runNextLine, revert, runAll, saveInstructions} from "../api";

const Controls = ({ onNext }) => {
	  const handleNext = async () => {
	try {
	  await runNextLine();
	  onNext();
	} catch (err) {
	  alert('Failed to run next line', err);
	}
  };

  const handleRevert = async () => {
	try {
	  await revert();
	  onNext();
	} catch (err) {
	  alert('Failed to revert', err);
	}
  };

  const handleRunAll = async () => {
	try {
	  await runAll();
	  onNext();
	} catch (err) {
	  alert('Failed to run all', err);
	}
  };
  const handleSave = async () => {
	try{
		await saveInstructions(code.split("\n"));
		alaert('Instructions saved');
	}
	catch(err){
		alert('Failed to save instructions', err);
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