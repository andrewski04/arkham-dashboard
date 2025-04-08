/**
 * Utility functions for the Arkham Dashboard
 */

// Helper function to set interval with random time between min and max ms
function setRandomInterval(callback, minDelay, maxDelay) {
  let timeout;

  const runInterval = () => {
    const timeoutFunction = () => {
      callback();
      runInterval();
    };

    const delay =
      Math.floor(Math.random() * (maxDelay - minDelay + 1)) + minDelay;
    timeout = setTimeout(timeoutFunction, delay);
  };

  runInterval();

  return {
    clear() {
      clearTimeout(timeout);
    },
  };
}

/**
 * Format ISO timestamp string to "YYYY-MM-DD HH:mm:ss"
 * @param {string} isoString
 * @returns {string}
 */
function formatTimestamp(isoString) {
  const date = new Date(isoString);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  const hours = String(date.getHours()).padStart(2, "0");
  const minutes = String(date.getMinutes()).padStart(2, "0");
  const seconds = String(date.getSeconds()).padStart(2, "0");
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

export { setRandomInterval, formatTimestamp };
