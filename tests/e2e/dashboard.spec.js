const { test, expect } = require("@playwright/test");

const BASE_URL = "http://127.0.0.1:5000";

test("dashboard page loads and displays charts", async ({ page }) => {
  // Use unique credentials for this test run
  const username = `dashuser_${Date.now()}`;
  const password = "password123";

  // Register user
  await page.goto(`${BASE_URL}/auth/register`);
  await page.locator("#username").fill(username);
  await page.locator("#password").fill(password);
  await page.locator('button[type="submit"]').click();
  // Wait for the redirect to the login page after registration
  await expect(page).toHaveURL(`${BASE_URL}/auth/login`);

  // Login user (already on the login page due to redirect)
  await page.locator("#username").fill(username);
  await page.locator("#password").fill(password);
  await page.locator('button[type="submit"]').click();

  // Should be on dashboard now
  await expect(page).toHaveURL(`${BASE_URL}/`);

  // Check page title or header
  await expect(page.locator("h1")).toContainText(
    "Arkham Asylum Security Dashboard"
  );

  // Wait for dashboard elements to be present before checking visibility
  await page.locator("#severityChart").waitFor({ state: "attached" });
  await page.locator("#timeChart").waitFor({ state: "attached" });
  await page.locator("#recentActivityList").waitFor({ state: "attached" });

  // Check severity chart exists
  await expect(page.locator("#severityChart")).toBeVisible();

  // Check time chart exists
  await expect(page.locator("#timeChart")).toBeVisible();

  // Check recent activity list exists
  await expect(page.locator("#recentActivityList")).toBeVisible();
});
