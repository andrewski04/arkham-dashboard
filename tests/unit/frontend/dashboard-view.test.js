/**
 * @jest-environment jsdom
 */

import { initDashboard } from "../../../app/static/js/dashboard-view.js";

global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve({}),
  })
);

beforeEach(() => {
  fetch.mockClear();

  // Mock DOM elements
  document.body.innerHTML = `
    <canvas id="severityChart"></canvas>
    <canvas id="timeChart"></canvas>
    <canvas id="categoryChart"></canvas>
    <canvas id="accessResultsChart"></canvas>
    <ul id="recentActivityList"></ul>
  `;

  // Mock getContext for Chart.js
  HTMLCanvasElement.prototype.getContext = () => {
    return {};
  };

  // Mock Chart constructor
  global.Chart = jest.fn().mockImplementation(() => ({
    data: {
      datasets: [
        { data: Array(12).fill(0) }, // Network
        { data: Array(12).fill(0) }, // Security
        { data: Array(12).fill(0) }, // Access
      ],
      labels: Array(12).fill(""),
    },
    update: jest.fn(),
  }));
});

test("initDashboard initializes dashboard and fetches logs", async () => {
  const logStore = {
    network: [],
    server_logs: [],
    video_surveillance: [],
    biometric_access: [],
    physical_security: [],
    internal_comms: [],
    inmate_threats: [],
  };

  initDashboard(logStore);

  // fetch should be called at least once
  expect(fetch).toHaveBeenCalled();
});
