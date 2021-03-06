import React from "react";
import ReactDOM from "react-dom";
import App from "./App";
import App2 from "./App2";
import App3 from "./App3";
import "bootstrap/dist/css/bootstrap.min.css";

import { DarkModeContextProvider } from "./context/darkModeContext";
import App4 from "./App4";

ReactDOM.render(
  <React.StrictMode>
    <DarkModeContextProvider>
      <App />
    </DarkModeContextProvider>
  </React.StrictMode>,
  document.getElementById("root")
);
