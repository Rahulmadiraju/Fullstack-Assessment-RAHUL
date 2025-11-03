import React from "react";
import AnalyticsChart from "./components/AnalyticsChart";
import { devLog } from "./dev-utils";

export default function App() {
  devLog("App mounted - debug log");
  return (
    <div className="container">
      <div className="header">
        <div>
          <h1 style={{ margin: 0 }}>Agent Analytics</h1>
          <p style={{ margin: 0, color: "var(--muted)" }}>Imaginary call analytics dashboard — styled similar to superbryn.com</p>
        </div>
        <div style={{ textAlign: "right", color: "var(--muted)" }}>
          <div>Written by Rahul M — internship assessment project</div>
        </div>
      </div>

      <AnalyticsChart />
    </div>
  );
}
