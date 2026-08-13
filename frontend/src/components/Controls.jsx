import { useRef, useState } from 'react';
import { getProgram, reset, runNextLine, revert, runAll, saveInstructions } from '../api';
import '../App.css';

const errorMessage = (error) => error.response?.data?.detail || error.message;

const Controls = ({ code, savedCode, setSavedCode, setCode, triggerUpdate, setActiveLine }) => {
  const [canRevert, setCanRevert] = useState(false);
  const [isBusy, setIsBusy] = useState(false);
  const [status, setStatus] = useState('');
  const busyRef = useRef(false);
  const isDirty = code !== savedCode;

  const saveCurrentCode = async () => {
    const response = await saveInstructions(code.split('\n'));
    setSavedCode(code);
    setActiveLine(response.data.activeLine ?? 1);
    setCanRevert(false);
    setStatus('Program saved.');
  };

  const perform = async (pendingMessage, operation) => {
    if (busyRef.current) return;
    busyRef.current = true;
    setIsBusy(true);
    setStatus(pendingMessage);
    try {
      await operation();
    } catch (error) {
      setStatus(errorMessage(error));
    } finally {
      busyRef.current = false;
      setIsBusy(false);
    }
  };

  const handleNext = () => perform('Stepping…', async () => {
    if (isDirty) await saveCurrentCode();
    const response = await runNextLine();
    const { changedRegister, changedAddress, activeLine } = response.data;
    if (activeLine != null) setActiveLine(activeLine);
    setCanRevert(Boolean(response.data.canRevert));
    setStatus(response.data.message);
    await triggerUpdate(changedRegister, changedAddress);
  });

  const handleRevert = () => perform('Reverting…', async () => {
    const response = await revert();
    const { changedRegister, changedAddress, activeLine } = response.data;
    if (activeLine != null) setActiveLine(activeLine);
    setCanRevert(Boolean(response.data.canRevert));
    setStatus(response.data.message);
    await triggerUpdate(changedRegister, changedAddress);
  });

  const handleRunAll = () => perform('Running…', async () => {
    if (isDirty) await saveCurrentCode();
    const response = await runAll();
    setActiveLine(response.data.activeLine ?? code.split('\n').length);
    setCanRevert(Boolean(response.data.canRevert));
    setStatus(`${response.data.message} (${response.data.steps} steps).`);
    await triggerUpdate();
  });

  const handleSave = () => {
    if (!code.trim()) {
      setStatus('No instructions to save.');
      return;
    }
    perform('Saving…', async () => {
      await saveCurrentCode();
      await triggerUpdate();
    });
  };

  const handleLoad = () => perform('Loading program…', async () => {
    const response = await getProgram();
    const loadedCode = response.data.instructions.join('\n');
    setCode(loadedCode);
    setSavedCode(loadedCode);
    setActiveLine(response.data.activeLine ?? 1);
    setCanRevert(Boolean(response.data.canRevert));
    setStatus(loadedCode ? 'Program loaded.' : 'No saved program exists.');
    await triggerUpdate();
  });

  const handleReset = () => perform('Resetting…', async () => {
    await reset();
    setCode('');
    setSavedCode('');
    setActiveLine(1);
    setCanRevert(false);
    setStatus('Simulator reset.');
    await triggerUpdate();
  });

  return (
    <>
      <div className="controls-toolbar">
        <button className="btn btn-primary" onClick={handleNext} disabled={isBusy}>▶ Step Next</button>
        <button className="btn btn-secondary" onClick={handleRunAll} disabled={isBusy}>⏩ Run All</button>
        <button className="btn btn-secondary" onClick={handleRevert} disabled={isBusy || !canRevert}>↩ Revert</button>
        <button className="btn btn-accent" onClick={handleSave} disabled={isBusy}>💾 Save Code{isDirty ? ' *' : ''}</button>
        <button className="btn btn-secondary" onClick={handleLoad} disabled={isBusy}>Load</button>
        <button className="btn btn-secondary" onClick={handleReset} disabled={isBusy}>Reset</button>
      </div>
      <div role="status" aria-live="polite">{status}</div>
    </>
  );
};

export default Controls;
