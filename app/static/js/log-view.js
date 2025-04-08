import { formatTimestamp, setRandomInterval } from "./utils.js";

$(document).ready(function () {
  const logTable = $("#logTable");

  if (logTable.length) {
    const endpoint = logTable.data("endpoint"); // Get API endpoint from data attribute
    const columnsConfig = logTable.data("columns"); // Get column definitions

    if (!endpoint || !columnsConfig) {
      console.error(
        "Table is missing 'data-endpoint' or 'data-columns' attribute!"
      );
      return;
    }

    // Define columns based on the data-columns attribute
    const columns = columnsConfig.map((col) => ({
      data: col.data, // Key in the JSON data object
      title: col.title, // Header title for the column
      render: (() => {
        if (col.data === "timestamp") {
          return function (data, type, row) {
            return type === "display" ? formatTimestamp(data) : data;
          };
        }
        if (
          ["threat_level", "status", "access_result", "action"].includes(
            col.data
          )
        ) {
          return function (data, type, row) {
            if (type === "display") {
              const safeData = data
                ? data.toLowerCase().replace(/\s+/g, "-")
                : "";
              return `<span class="log-label ${safeData}">${data}</span>`;
            }
            return data;
          };
        }
        return null; // default rendering
      })(),
    }));

    const dt = logTable.DataTable({
      processing: true, // Show processing indicator
      serverSide: false, // DataTables will handle processing client-side after initial load
      ajax: {
        url: endpoint, // API endpoint to fetch data
        dataSrc: "", // Data source is the root of the JSON array
      },
      columns: columns, // Define table columns
      order: [[columns.findIndex((col) => col.data === "timestamp"), "desc"]], // Default sort by timestamp descending
      // Enable features
      searching: true,
      paging: true,
      info: true,
      lengthChange: true,
      pageLength: 15, // Default number of rows per page
      lengthMenu: [
        [10, 15, 25, 50, -1],
        [10, 15, 25, 50, "All"],
      ], // Page length options
    });

    // Periodically refresh the table data every 2-4 seconds with random interval
    setRandomInterval(
      () => {
        dt.ajax.reload(null, false); // false = keep current paging
      },
      2000,
      4000
    );
  }
});
