import { useEffect, useRef, useState } from 'react';
import { getCache } from '../api';
import '../App.css';

const hex = (value) => value == null ? '—' : `0x${Number(value).toString(16).toUpperCase()}`;

const Cache = ({ refresh }) => {
  const [cache, setCache] = useState(null);
  const [error, setError] = useState('');
  const requestIdRef = useRef(0);

  useEffect(() => {
    const requestId = ++requestIdRef.current;
    getCache()
      .then((response) => {
        if (requestId === requestIdRef.current) {
          setCache(response.data);
          setError('');
        }
      })
      .catch((err) => {
        if (requestId === requestIdRef.current) setError(err.response?.data?.detail || err.message);
      });
  }, [refresh]);

  const stats = cache?.statistics;
  const last = cache?.lastAccess;

  return (
    <section className="cache-container">
      <div className="cache-heading">
        <h3>Data Cache</h3>
        {last && <span className={`cache-result cache-${last.result.toLowerCase()}`}>{last.operation.toUpperCase()} {hex(last.address)}: {last.result}</span>}
      </div>
      {error && <div role="alert">Failed to load cache: {error}</div>}
      {cache && (
        <>
          <div className="cache-stats">
            <span>Accesses <strong>{stats.accesses}</strong></span>
            <span>Hits <strong>{stats.hits}</strong></span>
            <span>Misses <strong>{stats.misses}</strong></span>
            <span>Hit rate <strong>{(stats.hitRate * 100).toFixed(1)}%</strong></span>
          </div>
          <div className="cache-table-container">
            <table className="cache-table">
              <thead><tr><th>Line</th><th>V</th><th>Tag</th><th>Block address</th><th>Data</th></tr></thead>
              <tbody>
                {cache.lines.map((line) => (
                  <tr key={line.index} className={last?.lineIndex === line.index ? 'cache-line-active' : ''}>
                    <td>{line.index}</td><td>{line.valid ? 1 : 0}</td><td>{hex(line.tag)}</td>
                    <td>{hex(line.blockAddress)}</td><td>{hex(line.data)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="cache-config">Direct-mapped · {cache.configuration.lineCount} lines · {cache.configuration.blockSize}-byte blocks · write-through/write-allocate</div>
        </>
      )}
    </section>
  );
};

export default Cache;
