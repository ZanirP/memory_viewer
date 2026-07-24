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
  const [activeLine, setActiveLine] = useState(1);  
  const [refresh, setRefresh] = useState(false);

  const [lastChangedRegister, setLastChangedRegister] = useState(null);
  const [lastChangedAddress, setLastChangedAddress] = useState(null);

  async function triggerUpdate(changedRegister = null, changedAddress = null) {
    try{
      console.log('Triggering update with changedRegister:', changedRegister, 'and changedAddress:', changedAddress);


      setLastChangedRegister(changedRegister);
      setLastChangedAddress(changedAddress);
      const registerResponse = await getRegisters();
      setRegistersData(registerResponse.data.Registers || {})
      const memoryResponse = await getMemory();
      setMemoryData(memoryResponse.data.Memory || {})

      setRefresh(!refresh);
    }
    catch (err){
      console.error('Error in triggerUpdate: ', err);
    }
  };

  return (
    <div className="main-page">
      <div className="left-panel">
        <h2>ARMv8 Memory Viewer</h2>
        <TextEditor 
          triggerUpdate={triggerUpdate} 
          activeLine={activeLine} 
          setActiveLine={setActiveLine} 
        />
      </div>
      <div className="right-panel">
        <Registers refresh={refresh} lastChangedRegister={lastChangedRegister} />
        <Memory refresh={refresh} lastChangedAddress={lastChangedAddress} />
      </div>
    </div>
  );
};

export default App;