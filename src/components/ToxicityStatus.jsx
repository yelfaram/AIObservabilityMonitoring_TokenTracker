import React from 'react';

export default function ToxicityStatus({ toxicity, hallucination }) {
  return (
    <div>
      <p>
        Toxicity: {toxicity ? <span style={{ color: 'red' }}>Detected ⚠️</span> : <span style={{ color: 'green' }}>None ✔️</span>}
      </p>
      <p>
        Hallucination: {hallucination ? <span style={{ color: 'red' }}>Detected ⚠️</span> : <span style={{ color: 'green' }}>None ✔️</span>}
      </p>
    </div>
  );
}