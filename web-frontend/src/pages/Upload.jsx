import { useState } from "react";
import api from "../api";
import Charts from "../components/Charts";
import History from "../components/History";

function Upload() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setResult(null);

    if (!file) {
      setError("Please select a CSV file");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      await api.get("/api/csrf/");
      const response = await api.post("/api/upload-csv/", formData);
      setResult(response.data);
      setFile(null);
      const fileInput = document.getElementById("csv-file");
      if (fileInput) fileInput.value = "";
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.error || "CSV upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {/* Header */}
      <header style={{ textAlign: "center", marginBottom: "3rem" }}>
        <h1>Chemical Equipment Analytics</h1>
        <p>Upload CSV files to analyze chemical equipment data</p>
      </header>

      {/* Upload Section */}
      <section className="card">
        <h2>Upload CSV File</h2>
        <p style={{ color: "var(--text-muted)", marginBottom: "1.5rem" }}>
          Required columns: Equipment Name, Type, Flowrate, Pressure, Temperature
        </p>

        <form onSubmit={handleSubmit}>
          <div className="file-input-wrapper">
            <input
              id="csv-file"
              type="file"
              accept=".csv"
              onChange={(e) => setFile(e.target.files[0])}
            />
            <button
              type="submit"
              className="btn-primary"
              disabled={loading || !file}
            >
              {loading ? "Uploading..." : "Upload and Analyze"}
            </button>
          </div>
        </form>

        {error && <div className="error-message" style={{ marginTop: "1.5rem" }}>{error}</div>}
      </section>

      {/* Analytics Results */}
      {result && (
        <section className="card">
          <h2>Analytics Results</h2>

          {/* Stats Grid */}
          <div className="stats-grid">
            <div className="stat-card">
              <span className="stat-value">{result.summary.total_equipment}</span>
              <span className="stat-label">Total Equipment</span>
            </div>
            <div className="stat-card" style={{ background: "linear-gradient(135deg, #10b981 0%, #059669 100%)" }}>
              <span className="stat-value">{result.summary.average_flowrate.toFixed(1)}</span>
              <span className="stat-label">Avg Flowrate</span>
            </div>
            <div className="stat-card" style={{ background: "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)" }}>
              <span className="stat-value">{result.summary.average_pressure.toFixed(1)}</span>
              <span className="stat-label">Avg Pressure</span>
            </div>
            <div className="stat-card" style={{ background: "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)" }}>
              <span className="stat-value">{result.summary.average_temperature.toFixed(1)}</span>
              <span className="stat-label">Avg Temperature</span>
            </div>
          </div>

          {/* Charts */}
          <div className="charts-container">
            <div className="chart-wrapper">
              <h3>Equipment Type Distribution</h3>
              <Charts summary={result.summary} chartType="distribution" />
            </div>
            <div className="chart-wrapper">
              <h3>Average Parameters</h3>
              <Charts summary={result.summary} chartType="averages" />
            </div>
          </div>
        </section>
      )}

      {/* History Section */}
      <section className="card">
        <History />
      </section>
    </div>
  );
}

export default Upload;
