const { test, expect } = require("@playwright/test");

test("dashboard page loads and displays charts", async ({ page }) => {
  await page.goto("http://localhost:5000/");

  // Check page title or header
  await expect(page.locator("h1")).toContainText(/dashboard/i);

  // Check severity chart exists
  await expect(page.locator("#severityChart")).toBeVisible();

  // Check time chart exists
  await expect(page.locator("#timeChart")).toBeVisible();

  // Check recent activity list exists
  await expect(page.locator("#recentActivityList")).toBeVisible();
});
