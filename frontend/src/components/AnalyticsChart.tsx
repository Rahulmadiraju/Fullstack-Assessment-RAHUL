import React, { useState } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from "recharts";
import { ChartValues } from "../types";
import OverwriteModal from "./OverwriteModal";
import { supabase } from "../lib/supabaseClient";
import { devLog } from "../dev-utils";

type Props = {
  initialData?: ChartValues;
};

export default function AnalyticsChart({ initialData }: Props) {
  const [data, setData] = useState<ChartValues>(initialData ?? [
    { label: "Mon", value: 10 },
    { label: "Tue", value: 20 },
    { label: "Wed", value: 12 },
    { label: "Thu", value: 25 },
    { label: "Fri", value: 18 },
  ]);
  const [email, setEmail] = useState("");
  const [showModal, setShowModal] = useState(false);
  const [prevValues, setPrevValues] = useState<any>(null);

  async function handleSave() {
    if (!email) {
      alert("Please enter email before saving.");
      return;
    }
    // fetch existing for email from supabase table 'user_values'
    try {
      const { data: existing, error } = await supabase
        .from("user_values")
        .select("*")
        .eq("email", email)
        .limit(1);
      if (error) {
        console.warn("Supabase read error", error);
      }
      if (existing && existing.length > 0) {
        setPrevValues(existing[0].values);
        setShowModal(true);
        return;
      }
      // no existing, write
      await supabase.from("user_values").insert([{ email, values: data }]);
      alert("Values saved successfully.");
    } catch (e) {
      console.error("Save error", e);
      alert("Unable to save values (supabase not configured?)");
    }
  }

  async function confirmOverwrite() {
    setShowModal(false);
    try {
      await supabase.from("user_values").upsert([{ email, values: data }], { onConflict: ["email"] });
      alert("Values overwritten.");
    } catch (e) {
      console.error(e);
      alert("Failed to overwrite.");
    }
  }

  function handleUpdateValue(index: number, value: number) {
    const newData = data.map((d, i) => (i === index ? { ...d, value } : d));
    setData(newData);
  }

  return (
    <div className="card">
      <h2>Agent Call Analytics</h2>
      <div style={{ height: 320 }}>
        <ResponsiveContainer>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="label" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="value" stroke="#7c3aed" strokeWidth={3} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div style={{ marginTop: 16 }} className="controls">
        {data.map((d, i) => (
          <div key={d.label} style={{ display: "flex", gap: 6, alignItems: "center" }}>
            <label>{d.label}</label>
            <input
              type="number"
              value={d.value}
              onChange={(e) => handleUpdateValue(i, Number(e.target.value))}
              style={{ width: 80, padding: 6, borderRadius: 6 }}
            />
          </div>
        ))}
      </div>

      <div style={{ marginTop: 12 }} className="controls">
        <input placeholder="your email" value={email} onChange={(e) => setEmail(e.target.value)} style={{ padding: 8, borderRadius: 6 }} />
        <button onClick={handleSave} style={{ background: "var(--accent)", color: "white", padding: "8px 12px", borderRadius: 6 }}>
          Save values
        </button>
      </div>

      {showModal && prevValues && (
        <OverwriteModal previous={prevValues} onConfirm={confirmOverwrite} onCancel={() => setShowModal(false)} />
      )}
    </div>
  );
}
