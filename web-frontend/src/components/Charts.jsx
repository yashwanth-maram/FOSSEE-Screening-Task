import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";

ChartJS.register(
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
);

const chartOptions = {
  responsive: true,
  maintainAspectRatio: true,
  plugins: {
    legend: {
      display: false,
    },
  },
  scales: {
    y: {
      beginAtZero: true,
      grid: {
        color: '#e2e8f0',
      },
    },
    x: {
      grid: {
        display: false,
      },
    },
  },
};

function Charts({ summary, chartType }) {
  // Type Distribution Chart
  if (chartType === "distribution") {
    const typeData = {
      labels: Object.keys(summary.type_distribution),
      datasets: [
        {
          label: "Equipment Count",
          data: Object.values(summary.type_distribution),
          backgroundColor: [
            '#2563eb',
            '#10b981',
            '#f59e0b',
            '#ef4444',
            '#8b5cf6',
            '#06b6d4',
          ],
          borderRadius: 6,
        },
      ],
    };
    return <Bar data={typeData} options={chartOptions} />;
  }

  // Averages Chart
  if (chartType === "averages") {
    const avgData = {
      labels: ["Flowrate", "Pressure", "Temperature"],
      datasets: [
        {
          label: "Average Values",
          data: [
            summary.average_flowrate,
            summary.average_pressure,
            summary.average_temperature,
          ],
          backgroundColor: ['#2563eb', '#10b981', '#ef4444'],
          borderRadius: 6,
        },
      ],
    };
    return <Bar data={avgData} options={chartOptions} />;
  }

  // Default: Show both charts (legacy behavior)
  const typeData = {
    labels: Object.keys(summary.type_distribution),
    datasets: [
      {
        label: "Equipment Count",
        data: Object.values(summary.type_distribution),
        backgroundColor: '#2563eb',
        borderRadius: 6,
      },
    ],
  };

  const avgData = {
    labels: ["Flowrate", "Pressure", "Temperature"],
    datasets: [
      {
        label: "Average Values",
        data: [
          summary.average_flowrate,
          summary.average_pressure,
          summary.average_temperature,
        ],
        backgroundColor: ['#2563eb', '#10b981', '#ef4444'],
        borderRadius: 6,
      },
    ],
  };

  return (
    <div>
      <h3>Equipment Type Distribution</h3>
      <Bar data={typeData} options={chartOptions} />

      <h3 style={{ marginTop: "2rem" }}>Average Parameters</h3>
      <Bar data={avgData} options={chartOptions} />
    </div>
  );
}

export default Charts;
