import { useState } from 'react';
import Controls from './Controls';
import '../App.css';

const TextEditor = ({ triggerUpdate, activeLine = 1, setActiveLine}) => {
  const [code, setCode] = useState(
`ORR X0, X0, #5
ORR X1, X1, #1000
STR X0, [X1]
LDR X2, [X1]`
  );

  // Split code into lines so we can render line numbers and active indicators
  const lines = code.split('\n');

  return (
    <div className="text-editor-container">
      <h3>Code Editor</h3>
      
      <div className="editor-wrapper">
        {/* Line numbers column with active pointer */}
        <div className="line-numbers">
          {lines.map((_, index) => {
            const lineNumber = index + 1;
            const isActive = lineNumber === activeLine;
            return (
              <div 
                key={lineNumber} 
                className={`line-number ${isActive ? 'active-line-num' : ''}`}
              >
                {isActive ? '▶ ' : ''}{lineNumber}
              </div>
            );
          })}
        </div>

        {/* Code Input Area */}
        <textarea
          className="code-textarea"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          rows={Math.max(10, lines.length)}
          placeholder="Write your ARMv8 assembly code here..."
          spellCheck="false"
        />
      </div>

      {/* Controls passed code state */}
      <Controls code={code} triggerUpdate={triggerUpdate} 
	  activeLine={activeLine} setActiveLine={setActiveLine} />
    </div>
  );
};

export default TextEditor;