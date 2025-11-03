import React from "react";

type Props = {
  previous: any;
  onConfirm: () => void;
  onCancel: () => void;
};

export default function OverwriteModal({ previous, onConfirm, onCancel }: Props) {
  return (
    <div style={{
      position: "fixed", inset: 0, display: "flex", alignItems: "center",
      justifyContent: "center", background: "rgba(0,0,0,0.5)"
    }}>
      <div style={{ width: 420 }} className="card">
        <h3>Existing values found</h3>
        <p className="muted">We found your previous values for this email. Overwrite?</p>
        <pre style={{ background: "var(--glass)", padding: 10, borderRadius: 6 }}>{JSON.stringify(previous, null, 2)}</pre>
        <div style={{ display: "flex", justifyContent: "flex-end", gap: 8, marginTop: 12 }}>
          <button onClick={onCancel}>Cancel</button>
          <button onClick={onConfirm} style={{ background: "var(--accent)", color: "white", padding: "8px 12px", borderRadius: 6 }}>Overwrite</button>
        </div>
      </div>
    </div>
  );
}
