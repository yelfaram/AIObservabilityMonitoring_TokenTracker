import React, { useState } from "react";
import ChatWindow from "./components/chatWindow";
import TraceInfo from "./components/TraceInfo";
import MetadataSidebar from "./components/MetadataSidebar";
import Feedback from "./components/Feedback";
import GrafanaEmbed from "./components/GrafanaEmbed";

import "./components/ChatWindow.css";
import "./components/MetricsPanel.css";
import "./App.css";

const App = () => {
  const [metadata, setMetadata] = useState({});
  const [botResponse, setBotResponse] = useState("");

  return (
    <div className="app-wrapper">
      <div className="main-container">
        <ChatWindow
          setMetadata={setMetadata}
          setBotResponse={setBotResponse}
          botResponse={botResponse}
        />
        <div className="metrics-panel">
          <h2 className="metrics-title">Observability Panel</h2>
          <TraceInfo metadata={metadata?.trace_id} />
          <MetadataSidebar metadata={metadata} />
          <Feedback traceId={metadata?.trace_id} />
        </div>
        <div className="grafana-panel">
          <h3 className="grafana-title">Grafana Dashboard</h3>
          <GrafanaEmbed />
        </div>
      </div>
    </div>
  );
};

export default App;
