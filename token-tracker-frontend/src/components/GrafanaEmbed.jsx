import React from 'react';

export default function GrafanaEmbed() {
  return (
    <iframe
      src="http://localhost:3001/d/your-dashboard-id"
      width="100%"
      height="600"
      style={{ border: 'none', borderRadius: '8px' }}
      scrolling="no"
      title="Grafana Dashboard"
    />
  );
}
