import { useState } from 'react';
import TextEditor from './components/TextEditor';
import Memory from './components/Memory';
import Registers from './components/Registers';
import Controls from './components/Controls';
import './App.css';

const App = () => {
  const [refresh, setRefresh] = useState(false);

  const triggerUpdate = () => {
    setRefresh(!refresh);
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