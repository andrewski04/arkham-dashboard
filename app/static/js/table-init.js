import { formatTimestamp, setRandomInterval } from "./utils.js";

document.addEventListener("DOMContentLoaded", () => {
  const logTableElement = document.getElementById("logTable");

  if (logTableElement) {
    const endpoint = logTableElement.dataset.endpoint; // Get API endpoint from data-endpoint
    const columnsJson = logTableElement.dataset.columns; // Get column definitions as JSON string

    if (!endpoint || !columnsJson) {
      console.error(
        "Table is missing 'data-endpoint' or 'data-columns' attribute!"
      );
      return;
    }

    let columnsConfig;
    try {
      columnsConfig = JSON.parse(columnsJson); // Parse the JSON string
    } catch (e) {
      console.error("Error parsing data-columns JSON:", e);
      return;
    }

    // Define columns based on the parsed data-columns attribute
    const columns = columnsConfig.map((col) => {
      const columnDefinition = {
        data: col.data, // Key in the JSON data object
        title: col.title, // Header title for the column
        orderable: col.orderable !== false, // Enable sorting by default unless explicitly set to false
      };

      // Custom rendering for timestamp
      if (col.data === "timestamp") {
        columnDefinition.render = function (data, type, row) {
          // Use 'display' type for rendering formatted timestamp
          return type === "display" ? formatTimestamp(data) : data;
        };
      }
      // Custom rendering for specific status/label columns
      if (
        ["threat_level", "status", "access_result", "action"].includes(col.data)
      ) {
        columnDefinition.render = function (data, type, row) {
          if (type === "display") {
            // Sanitize data for CSS class: lowercase, replace spaces with hyphens
            const safeData = data
              ? String(data).toLowerCase().replace(/\s+/g, "-")
              : "";
            // Wrap data in a span with a class for styling
            return `<span class="log-label ${safeData}">${data}</span>`;
          }
          // For other types (sort, filter), return raw data
          return data;
        };
      }

      return columnDefinition;
    });

    // Initialize DataTables using the vanilla JS constructor
    const dt = new DataTable(logTableElement, {
      processing: true, // Show processing indicator
      serverSide: false, // DataTables handles processing client-side
      ajax: {
        url: endpoint, // API endpoint to fetch data
        dataSrc: "", // Data source is the root of the JSON array
      },
      columns: columns, // Define table columns
      // Default sort by timestamp descending (find the index of the timestamp column)
      order: [[columns.findIndex((col) => col.data === "timestamp"), "desc"]],
      // Enable features
      searching: true,
      paging: true,
      info: true,
      lengthChange: true,
      pageLength: 15, // Default number of rows per page
      lengthMenu: [
        [10, 15, 25, 50, -1], // Values
        [10, 15, 25, 50, "All"], // Display text
      ], // Page length options
    });

    // Periodically refresh the table data every 2-4 seconds with random interval
    setRandomInterval(
      () => {
        dt.ajax.reload(null, false); // false = keep current paging
      },
      2000, // min delay 2s
      4000 // max delay 4s
    );
  }
});
