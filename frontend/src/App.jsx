import { useState } from 'react';
import TextEditor from './components/TextEditor';
import Memory from './components/Memory';
import Registers from './components/Registers';
import Controls from './components/Controls';
import { getRegisters, getMemory } from './api';
import './App.css';

const App = () => {
  const [RegistersData, setRegistersData] = useState({});
  const [MemoryData, setMemoryData] = useState({});
  const [refresh, setRefresh] = useState(false);

  async function triggerUpdate() {
    try{
      console.log('Triggering update');

      const registerResponse = await getRegisters();
      setRegistersData(registerResponse.data.Registers || {})
      const memoryResponse = await getMemory();
      setMemoryData(memoryResponse.data.Memory || {})

      setRefresh(!refresh);
      console.log('Update triggered');
    }
    catch (err){
      console.error('Error in triggerUpdate: ', err);
    }
  };

  return (
    <div className="main-page">
      <div className="left-panel">
        <h2>ARMv8 Memory Viewer</h2>
        <TextEditor triggerUpdate={triggerUpdate} />
        <Controls triggerUpdate={triggerUpdate} />
      </div>
      <div className="right-panel">
        <Registers refresh={refresh} />
        <Memory refresh={refresh} />
      </div>
    </div>
  );
};

export default App;