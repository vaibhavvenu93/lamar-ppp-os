import React from "react";
import ReactDOM from "react-dom/client";

import App from "./App";
import "./styles.css";
import "./document-intelligence.css";
import "./bid-intelligence.css";
import "./deal-room.css";

const rootElement = document.getElementById("root");

if (!rootElement) {
  throw new Error(
    "Lamar OS could not find the root application element."
  );
}

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
