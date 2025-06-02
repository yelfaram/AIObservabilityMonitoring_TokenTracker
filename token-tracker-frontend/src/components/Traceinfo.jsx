import React from 'react';

export default function TraceInfo({ traceId }) {
  return (
    <div>
      <small>Trace/Session ID: {traceId}</small>
    </div>
  );
}