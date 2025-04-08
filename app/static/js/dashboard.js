/**
 * Main entry point for the Arkham Dashboard
 * Initializes the appropriate view based on the current page
 */

import {
  initializeLogStore,
  purgeOldLogs,
  saveLogStore,
  getCurrentPage,
} from "./core.js";
import { initDashboard } from "./dashboard-view.js";

document.addEventListener("DOMContentLoaded", () => {
  // Determine current page
  const page = getCurrentPage();

  // Initialize log store
  const logStore = initializeLogStore();

  // Save log store to localStorage periodically and purge old logs
  setInterval(() => {
    purgeOldLogs(logStore);
    saveLogStore(logStore);
  }, 10000);

  // Initialize the appropriate view
  if (page === "dashboard" || page === "") {
    initDashboard(logStore);
  }
  // For log pages, DataTables initializes automatically
});
