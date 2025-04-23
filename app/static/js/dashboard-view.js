/**
 * Dashboard-specific functionality for the Arkham Dashboard
 * Handles charts, recent activity, and system status
 */

import { setRandomInterval } from "./utils.js";
import { addLogToStore, saveLogStore } from "./core.js";

// Charts for the main dashboard
let severityChart = null;
let timeChart = null;
let categoryChart = null;
let accessResultsChart = null;

// Initialize the dashboard view
function initDashboard(logStore) {
  // Create charts
  createSeverityChart();
  createTimeChart(logStore);
  createCategoryChart();
  createAccessResultsChart();

  // Set up recent activity list
  const recentActivityList = document.getElementById("recentActivityList");
  updateRecentActivity(logStore, recentActivityList, true); // Pass logStore and a flag for initial load

  // Initial data fetch
  fetchSampleLogs(logStore, recentActivityList);

  // Set up periodic refresh with randomized intervals
  setRandomInterval(
    () => fetchSampleLogs(logStore, recentActivityList),
    2000,
    4000
  );
}

// Function to fetch sample logs from all categories
function fetchSampleLogs(logStore, recentActivityList) {
  fetch("/api/sample-logs")
    .then((response) => response.json())
    .then((data) => {
      if (!data || typeof data !== "object") {
        console.error("Invalid or empty sample logs response:", data);
        return;
      }

      console.log("Sample logs data:", data);

      // Store logs
      Object.keys(data).forEach((key) => {
        // Special handling for server logs
        if (key === "server_log") {
          logStore = addLogToStore(logStore, "server_logs", data[key]);
        } else {
          const category = key.replace("_log", "");
          if (logStore[category]) {
            logStore = addLogToStore(logStore, category, data[key]);
          }
        }
      });

      console.log("Updated logStore:", logStore);

      // Save to localStorage immediately to ensure we don't lose logs
      saveLogStore(logStore);

      // Update dashboard components
      updateSeverityChart(logStore);
      updateTimeChart();
      updateCategoryChart(logStore);
      updateAccessResultsChart(logStore);
      updateRecentActivity(logStore, recentActivityList);
      updateSystemStatus(logStore);
    })
    .catch((error) => console.error("Error fetching sample logs:", error));
}

// Create severity distribution chart
function createSeverityChart() {
  const ctx = document.getElementById("severityChart").getContext("2d");
  severityChart = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["Low", "Medium", "High", "Critical"],
      datasets: [
        {
          data: [0, 0, 0, 0],
          backgroundColor: [
            "#4caf50", // success/low
            "#ff9800", // warning/medium
            "#f44336", // danger/high
            "#9c27b0", // purple/critical
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "right",
          labels: {
            color: "#f1f1f1",
          },
        },
        title: {
          display: false,
        },
      },
    },
  });
}

// Create time-based chart
function createTimeChart() {
  const ctx = document.getElementById("timeChart").getContext("2d");
  timeChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: Array(12).fill(""),
      datasets: [
        {
          label: "Network",
          data: Array(12).fill(0),
          borderColor: "#2196f3",
          tension: 0.4,
          fill: false,
        },
        {
          label: "Security",
          data: Array(12).fill(0),
          borderColor: "#f44336",
          tension: 0.4,
          fill: false,
        },
        {
          label: "Access",
          data: Array(12).fill(0),
          borderColor: "#4caf50",
          tension: 0.4,
          fill: false,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            color: "#f1f1f1",
          },
          grid: {
            color: "rgba(255, 255, 255, 0.1)",
          },
        },
        x: {
          ticks: {
            color: "#f1f1f1",
          },
          grid: {
            color: "rgba(255, 255, 255, 0.1)",
          },
        },
      },
      plugins: {
        legend: {
          labels: {
            color: "#f1f1f1",
          },
        },
      },
    },
  });
}

// Update severity chart based on current logs
function updateSeverityChart(logStore) {
  if (!severityChart) return;

  // Count severity levels across all log types
  const severityCounts = {
    low: 0,
    medium: 0,
    high: 0,
    critical: 0,
  };

  // Check network logs
  logStore.network.forEach((log) => {
    if (log.threat_level) {
      severityCounts[log.threat_level.toLowerCase()]++;
    }
  });

  // Check inmate threats
  logStore.inmate_threats.forEach((log) => {
    if (log.threat_level) {
      severityCounts[log.threat_level.toLowerCase()]++;
    }
  });

  // Check video surveillance
  logStore.video_surveillance.forEach((log) => {
    if (log.level) {
      severityCounts[log.level.toLowerCase()]++;
    }
  });

  // Update chart data
  severityChart.data.datasets[0].data = [
    severityCounts.low,
    severityCounts.medium,
    severityCounts.high,
    severityCounts.critical,
  ];

  severityChart.update();
}

// Update time chart with alert frequency
function updateTimeChart() {
  if (
    !timeChart ||
    !timeChart.data ||
    !Array.isArray(timeChart.data.datasets) ||
    timeChart.data.datasets.length < 3 ||
    !Array.isArray(timeChart.data.labels)
  ) {
    console.error("Invalid or uninitialized timeChart object:", timeChart);
    return;
  }

  // Simulate time-based data (in a real app, we'd use actual timestamps)
  // For this prototype, we'll just shift data and add a new random point

  // Network alerts
  timeChart.data.datasets[0].data.shift();
  timeChart.data.datasets[0].data.push(Math.floor(Math.random() * 5) + 1);

  // Security alerts (physical + video)
  timeChart.data.datasets[1].data.shift();
  timeChart.data.datasets[1].data.push(Math.floor(Math.random() * 4) + 1);

  // Access alerts (biometric)
  timeChart.data.datasets[2].data.shift();
  timeChart.data.datasets[2].data.push(Math.floor(Math.random() * 3));

  // Update time labels (would use actual timestamps in a real app)
  const now = new Date();
  timeChart.data.labels.shift();
  timeChart.data.labels.push(
    now.toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit" })
  );

  timeChart.update();
}

// Create Log Count by Category chart
function createCategoryChart() {
  const ctx = document.getElementById("categoryChart").getContext("2d");
  categoryChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: [
        "Network",
        "Server",
        "Surveillance",
        "Access",
        "Security",
        "Comms",
        "Inmate",
      ],
      datasets: [
        {
          label: "Log Count",
          data: [0, 0, 0, 0, 0, 0, 0],
          backgroundColor: [
            "#2196f3", // blue
            "#ff9800", // orange
            "#4caf50", // green
            "#9c27b0", // purple
            "#f44336", // red
            "#00bcd4", // cyan
            "#ffeb3b", // yellow
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            color: "#f1f1f1",
          },
          grid: {
            color: "rgba(255, 255, 255, 0.1)",
          },
        },
        x: {
          ticks: {
            color: "#f1f1f1",
          },
          grid: {
            color: "rgba(255, 255, 255, 0.1)",
          },
        },
      },
      plugins: {
        legend: {
          display: false,
        },
        title: {
          display: false,
        },
      },
    },
  });
}

// Update Log Count by Category chart
function updateCategoryChart(logStore) {
  if (!categoryChart) return;

  const categoryCounts = {
    network: logStore.network.length,
    server_logs: logStore.server_logs.length,
    video_surveillance: logStore.video_surveillance.length,
    biometric_access: logStore.biometric_access.length,
    physical_security: logStore.physical_security.length,
    internal_comms: logStore.internal_comms.length,
    inmate_threats: logStore.inmate_threats.length,
  };

  // Introduce randomness for a more dynamic feel
  const randomizedCounts = [
    Math.max(0, categoryCounts.network + Math.floor(Math.random() * 10 - 5)),
    Math.max(
      0,
      categoryCounts.server_logs + Math.floor(Math.random() * 10 - 5)
    ),
    Math.max(
      0,
      categoryCounts.video_surveillance + Math.floor(Math.random() * 10 - 5)
    ),
    Math.max(
      0,
      categoryCounts.biometric_access + Math.floor(Math.random() * 10 - 5)
    ),
    Math.max(
      0,
      categoryCounts.physical_security + Math.floor(Math.random() * 10 - 5)
    ),
    Math.max(
      0,
      categoryCounts.internal_comms + Math.floor(Math.random() * 10 - 5)
    ),
    Math.max(
      0,
      categoryCounts.inmate_threats + Math.floor(Math.random() * 10 - 5)
    ),
  ];

  categoryChart.data.datasets[0].data = randomizedCounts;

  categoryChart.update();
}

// Create Access Control Results chart
function createAccessResultsChart() {
  const ctx = document.getElementById("accessResultsChart").getContext("2d");
  accessResultsChart = new Chart(ctx, {
    type: "pie",
    data: {
      labels: ["Granted", "Denied"],
      datasets: [
        {
          data: [0, 0],
          backgroundColor: ["#4caf50", "#f44336"], // green, red
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "right",
          labels: {
            color: "#f1f1f1",
          },
        },
        title: {
          display: false,
        },
      },
    },
  });
}

// Update Access Control Results chart
function updateAccessResultsChart(logStore) {
  if (!accessResultsChart) return;

  const accessResultsCounts = {
    granted: 0,
    denied: 0,
  };

  logStore.biometric_access.forEach((log) => {
    if (log.access_result) {
      accessResultsCounts[log.access_result.toLowerCase()]++;
    }
  });

  accessResultsChart.data.datasets[0].data = [
    accessResultsCounts.granted,
    accessResultsCounts.denied,
  ];

  accessResultsChart.update();
}

// Update recent activity list
function updateRecentActivity(logStore, listElement) {
  if (!listElement) return;

  // Clear existing items if there are too many
  if (listElement.children.length > 10) {
    listElement.innerHTML = "";
  }

  // Get the most recent log from each category
  const recentLogs = [];

  if (logStore.network.length > 0) {
    recentLogs.push({
      type: "Network",
      log: logStore.network[0],
      message: `${logStore.network[0].action} ${logStore.network[0].protocol} traffic from ${logStore.network[0].source_ip}`,
    });
  }

  if (logStore.server_logs.length > 0) {
    recentLogs.push({
      type: "Server",
      log: logStore.server_logs[0],
      message: `${logStore.server_logs[0].event} on ${logStore.server_logs[0].server}`,
    });
  }

  if (logStore.video_surveillance.length > 0) {
    recentLogs.push({
      type: "Surveillance",
      log: logStore.video_surveillance[0],
      message: `${logStore.video_surveillance[0].activity} in ${logStore.video_surveillance[0].location}`,
    });
  }

  if (logStore.biometric_access.length > 0) {
    recentLogs.push({
      type: "Access",
      log: logStore.biometric_access[0],
      message: `Access ${logStore.biometric_access[0].access_result} at ${logStore.biometric_access[0].location}`,
    });
  }

  if (logStore.physical_security.length > 0) {
    recentLogs.push({
      type: "Security",
      log: logStore.physical_security[0],
      message: `${logStore.physical_security[0].system} ${logStore.physical_security[0].status} in ${logStore.physical_security[0].location}`,
    });
  }

  if (logStore.internal_comms.length > 0) {
    recentLogs.push({
      type: "Comms",
      log: logStore.internal_comms[0],
      message: `${logStore.internal_comms[0].type} sent by ${logStore.internal_comms[0].sent_by}`,
    });
  }

  if (logStore.inmate_threats.length > 0) {
    recentLogs.push({
      type: "Inmate",
      log: logStore.inmate_threats[0],
      message: `${logStore.inmate_threats[0].name} (${logStore.inmate_threats[0].threat_level}) in ${logStore.inmate_threats[0].last_known_location}`,
    });
  }

  // Sort by timestamp (newest first) and take the top 3
  recentLogs.sort((a, b) => {
    return new Date(b.log.timestamp) - new Date(a.log.timestamp);
  });

  // Add new items to the list
  recentLogs.slice(0, 3).forEach((item) => {
    const li = document.createElement("li");
    const timestamp = new Date(item.log.timestamp);
    li.innerHTML = `<strong>${item.type}:</strong> ${
      item.message
    } <span class="timestamp">${timestamp.toLocaleTimeString()}</span>`;

    // Determine severity level for the dot
    let severityLevel = null;
    if (item.log.threat_level) {
      severityLevel = item.log.threat_level.toLowerCase();
    } else if (item.log.level) {
      severityLevel = item.log.level.toLowerCase();
    } else if (item.type === "Server" && item.log.status) {
      const status = item.log.status.toLowerCase();
      if (status === "escalated") {
        severityLevel = "high";
      } else if (status === "investigating" || status === "monitoring") {
        severityLevel = "medium";
      } else if (status === "resolved") {
        severityLevel = "low";
      }
    }

    // Add severity indicator if a level was determined
    if (severityLevel) {
      li.innerHTML =
        `<span class="status-indicator status-${severityLevel}"></span>` +
        li.innerHTML;
    }

    listElement.prepend(li);
  });
}

/**
 * Update system status indicators based on the last 30 logs for each subsystem.
 * This smooths out fluctuations and provides a more realistic overall status.
 */
function updateSystemStatus(logStore) {
  function calculateStatus(logs, getLevelFn) {
    const recentLogs = logs.slice(0, 30);
    const counts = { low: 0, medium: 0, high: 0, critical: 0 };

    recentLogs.forEach((log) => {
      const level = getLevelFn(log);
      if (level && counts.hasOwnProperty(level)) {
        counts[level]++;
      }
    });

    // Determine dominant severity
    if (counts.critical >= 5 || counts.high >= 5) {
      return { level: "high", text: "Alert" };
    } else if (counts.medium >= 5) {
      return { level: "medium", text: "Warning" };
    } else {
      return { level: "low", text: "Normal" };
    }
  }

  // Network status
  if (logStore.network.length > 0) {
    const networkStatus = document.getElementById("networkStatus");
    if (networkStatus) {
      const { level, text } = calculateStatus(logStore.network, (log) =>
        log.threat_level ? log.threat_level.toLowerCase() : "low"
      );
      networkStatus.innerHTML = `<span class="status-indicator status-${level}"></span>${text}`;
    }
  }

  // Server status
  if (logStore.server_logs.length > 0) {
    const serverStatus = document.getElementById("serverStatus");
    if (serverStatus) {
      const { level, text } = calculateStatus(logStore.server_logs, (log) => {
        const status = log.status ? log.status.toLowerCase() : "normal";
        if (status === "escalated") return "high";
        if (status === "investigating" || status === "monitoring")
          return "medium";
        return "low";
      });
      serverStatus.innerHTML = `<span class="status-indicator status-${level}"></span>${text}`;
    }
  }

  // Surveillance status
  if (logStore.video_surveillance.length > 0) {
    const surveillanceStatus = document.getElementById("surveillanceStatus");
    if (surveillanceStatus) {
      const { level, text } = calculateStatus(
        logStore.video_surveillance,
        (log) => (log.level ? log.level.toLowerCase() : "low")
      );
      surveillanceStatus.innerHTML = `<span class="status-indicator status-${level}"></span>${text}`;
    }
  }

  // Access status
  if (logStore.biometric_access.length > 0) {
    const accessStatus = document.getElementById("accessStatus");
    if (accessStatus) {
      const { level, text } = calculateStatus(
        logStore.biometric_access,
        (log) => {
          const result = log.access_result
            ? log.access_result.toLowerCase()
            : "granted";
          if (result === "denied") return "high";
          return "low";
        }
      );
      accessStatus.innerHTML = `<span class="status-indicator status-${level}"></span>${text}`;
    }
  }

  // Physical security status
  if (logStore.physical_security.length > 0) {
    const physicalStatus = document.getElementById("physicalStatus");
    if (physicalStatus) {
      const { level, text } = calculateStatus(
        logStore.physical_security,
        (log) => {
          const status = log.status ? log.status.toLowerCase() : "normal";
          if (status === "active") return "high";
          if (status === "fault") return "medium";
          return "low";
        }
      );
      physicalStatus.innerHTML = `<span class="status-indicator status-${level}"></span>${text}`;
    }
  }
}

// Export the dashboard functions
export { initDashboard };
