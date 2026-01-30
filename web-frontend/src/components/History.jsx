import { useEffect, useState } from "react";
import api from "../api";

/**
 * Format date to local timezone with readable format
 */
function formatLocalTime(isoString) {
  try {
    const date = new Date(isoString);
    return date.toLocaleString(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      hour12: true,
    });
  } catch {
    return isoString;
  }
}

function History() {
  const [datasets, setDatasets] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const response = await api.get("/api/history/");
      setDatasets(response.data);
      setError("");
    } catch {
      setError("Failed to load history");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const downloadPDF = async () => {
    try {
      const response = await api.get("/api/pdf/", { responseType: "blob" });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "equipment_report.pdf");
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch {
      alert("Failed to download PDF. Make sure you have uploaded at least one dataset.");
    }
  };

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1.5rem" }}>
        <h2 style={{ margin: 0 }}>Upload History</h2>
        <button onClick={fetchHistory} className="btn-secondary">
          Refresh
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {loading ? (
        <div className="loading">Loading history...</div>
      ) : datasets.length === 0 ? (
        <p style={{ textAlign: "center", color: "var(--text-muted)", padding: "2.5rem" }}>
          No datasets uploaded yet. Upload a CSV to get started.
        </p>
      ) : (
        <div>
          {datasets.map((d) => (
            <div key={d.id} className="history-item">
              <span className="history-filename">{d.filename}</span>
              <span className="history-time">{formatLocalTime(d.uploaded_at)}</span>
            </div>
          ))}
        </div>
      )}

      <div style={{ marginTop: "2rem", textAlign: "center" }}>
        <button
          onClick={downloadPDF}
          className="btn-success"
          disabled={datasets.length === 0}
        >
          Download Latest PDF Report
        </button>
      </div>
    </div>
  );
}

export default History;
