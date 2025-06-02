import React from "react";

function MetadataSidebar({ metadata }) {
  if (!metadata) {
    return <p>No metadata available.</p>;
  }

  const {
    latency_s,
    token_usage = {},
    model,
    trace_id,
    toxicity_score,
    flagged_toxic,
    total_time,
  } = metadata;

  return (
    <div
      style={{
        width: "80%",
        padding: "1rem",
        background: "#f2f2f2",
        borderRadius: "8px",
        marginTop: "1rem",
      }}
    >
      <h3>Metadata</h3>
      <p>
        <strong>Trace ID:</strong> {trace_id}
      </p>
      <p>
        <strong>Model:</strong> {model}
      </p>
      <p>
        <strong>Latency:</strong> {latency_s?.toFixed(4)} s
      </p>

      <h4>Token Usage</h4>
      <p>Prompt: {token_usage.prompt_tokens}</p>
      <p>Completion: {token_usage.response_tokens}</p>
      <p>Total: {token_usage.total_tokens}</p>

      <h4>Toxicity</h4>
      <p>Score: {toxicity_score?.toFixed(4)}</p>
      <p>Flagged: {flagged_toxic ? "Yes ⚠️" : "No ✔️"}</p>

      <p>
        <strong>Total Time:</strong> {total_time}
      </p>
    </div>
  );
}

export default MetadataSidebar;
