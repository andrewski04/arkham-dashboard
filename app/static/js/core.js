/**
 * Core functionality for the Arkham Dashboard
 * Handles log store management and initialization
 */

// Maximum number of logs to keep in memory
const MAX_LOGS = 100;

// Initialize or restore the log store
function initializeLogStore() {
  const storedLogs = localStorage.getItem("arkhamLogStore");
  let logStore;

  if (storedLogs) {
    try {
      logStore = JSON.parse(storedLogs);
      console.log("Restored log store from localStorage");
    } catch (e) {
      console.error("Error parsing stored logs:", e);
      createNewLogStore();
    }
  } else {
    logStore = createNewLogStore();
  }

  return logStore;
}

// Create a new log store
function createNewLogStore() {
  const logStore = {
    network: [],
    server_logs: [],
    video_surveillance: [],
    biometric_access: [],
    physical_security: [],
    internal_comms: [],
    inmate_threats: [],
    lastCleared: new Date().toISOString(),
  };
  localStorage.setItem("arkhamLogStore", JSON.stringify(logStore));
  console.log("Initialized new log store");
  return logStore;
}

// Purge logs older than 2 minutes
function purgeOldLogs(logStore) {
  const twoMinutesAgo = new Date();
  twoMinutesAgo.setMinutes(twoMinutesAgo.getMinutes() - 2);

  Object.keys(logStore).forEach((category) => {
    if (category === "lastCleared") return;

    logStore[category] = logStore[category].filter((log) => {
      if (!log.timestamp) return true;
      const logTime = new Date(log.timestamp);
      return logTime > twoMinutesAgo;
    });
  });

  console.log("Purged logs older than 2 minutes");
  return logStore;
}

// Add a log to the store
function addLogToStore(logStore, category, log) {
  if (logStore[category]) {
    logStore[category].unshift(log);
    // Keep array size limited
    if (logStore[category].length > MAX_LOGS) {
      logStore[category] = logStore[category].slice(0, MAX_LOGS);
    }
  } else {
    console.error(`Category not found in logStore: ${category}`);
  }
  return logStore;
}

// Save log store to localStorage
function saveLogStore(logStore) {
  localStorage.setItem("arkhamLogStore", JSON.stringify(logStore));
}

// Determine current page based on URL path
function getCurrentPage() {
  const path = window.location.pathname;
  return path.split("/").pop() || "dashboard";
}

// Export the core functions
export {
  initializeLogStore,
  purgeOldLogs,
  addLogToStore,
  saveLogStore,
  getCurrentPage,
  MAX_LOGS,
};
