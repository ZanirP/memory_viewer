// Handle Writing and saving the ARMv8 assembly code
import {useState} from 'react';
import Controls from '../components/Controls';


const TextEditor = ({triggerUpdate}) => {
  const [code, setCode] = useState('');


  return (
	<div className="text-editor">
	  <textarea
		value={code}
		onChange={(e) => setCode(e.target.value)}
		rows="10"
		cols="50"
		placeholder="Write your ARMv8 assembly code here"
	  />
	  <Controls code={code} triggerUpdate={triggerUpdate} />
	</div>
  );
};

export default TextEditor;