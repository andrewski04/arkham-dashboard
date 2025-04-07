document.addEventListener("DOMContentLoaded", () => {
  const endpoints = {
    "network-chart": "/api/network-monitoring",
    "biometric-chart": "/api/biometric-access",
    "inmate-threats-chart": "/api/inmate-threats",
    "internal-comms-chart": "/api/internal-comms",
    "physical-security-chart": "/api/physical-security",
    "server-logs-chart": "/api/server-logs",
    "video-surveillance-chart": "/api/video-surveillance",
  };

  const fetchDataAndUpdate = async (elementId, url) => {
    const targetElement = document.getElementById(elementId);
    if (!targetElement) {
      console.error(`Element with ID ${elementId} not found.`);
      return;
    }

    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();

      // Use Plotly to display data as a table
      targetElement.classList.remove("data-display"); // Remove text display class
      // targetElement.innerHTML = ""; // Let Plotly.react handle updates directly

      const keys = Object.keys(data);
      const values = Object.values(data).map((val) => JSON.stringify(val)); // Ensure all values are strings

      const tableData = [
        {
          type: "table",
          header: {
            values: [["<b>Property</b>"], ["<b>Value</b>"]],
            align: ["left", "left"],
            line: { width: 1, color: "black" },
            fill: { color: "#333" }, // Dark header
            font: { family: "Arial", size: 12, color: "white" },
          },
          cells: {
            values: [keys, values],
            align: ["left", "left"],
            line: { color: "black", width: 1 },
            fill: { color: ["#f4f4f4", "white"] }, // Alternating row colors
            font: { family: "Arial", size: 11, color: ["black"] },
          },
        },
      ];

      const layout = {
        title: null, // Remove default Plotly title, we have the H2
        margin: { l: 10, r: 10, b: 10, t: 10, pad: 4 }, // Minimize margins
        autosize: true,
      };

      Plotly.react(elementId, tableData, layout, {
        responsive: true,
        displayModeBar: false,
      });
      // Explicitly trigger resize after updating the plot
      Plotly.Plots.resize(targetElement);
    } catch (error) {
      console.error(`Error fetching or plotting data for ${url}:`, error);
      // Display error message inside the container
      targetElement.innerHTML = `<div class="data-display">Error loading data: ${error.message}</div>`;
    }
  };

  // Initial fetch and update for all endpoints
  Object.entries(endpoints).forEach(([elementId, url]) => {
    fetchDataAndUpdate(elementId, url);
  });

  // Set interval to fetch and update every 5 seconds
  setInterval(() => {
    Object.entries(endpoints).forEach(([elementId, url]) => {
      fetchDataAndUpdate(elementId, url);
    });
  }, 5000);
});
