import { useState } from 'react';
import TextEditor from './components/TextEditor';
import Memory from './components/Memory';
import Registers from './components/Registers';
import Cache from './components/Cache';
import './App.css';

const App = () => {
  const [activeLine, setActiveLine] = useState(1);  
  const [refresh, setRefresh] = useState(false);

  const [lastChangedRegister, setLastChangedRegister] = useState(null);
  const [lastChangedAddress, setLastChangedAddress] = useState(null);

  async function triggerUpdate(changedRegister = null, changedAddress = null) {
    try{
      console.log('Triggering update with changedRegister:', changedRegister, 'and changedAddress:', changedAddress);


      setLastChangedRegister(changedRegister);
      setLastChangedAddress(changedAddress);
      setRefresh(previous => !previous);
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
        <Cache refresh={refresh} />
      </div>
    </div>
  );
};

export default App;
