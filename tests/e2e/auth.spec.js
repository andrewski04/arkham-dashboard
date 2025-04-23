// @ts-check
const { test, expect } = require("@playwright/test");

const BASE_URL = "http://127.0.0.1:5000"; // Assuming Flask runs on default port

test.describe("Authentication Flow", () => {
  // Use a unique username for each test run to avoid conflicts
  const username = `testuser_${Date.now()}`;
  const password = "password123";

  test("should allow a user to register", async ({ page }) => {
    await page.goto(`${BASE_URL}/auth/register`);

    // Fill out the registration form
    await page.locator("#username").fill(username);
    await page.locator("#password").fill(password);
    await page.locator('button[type="submit"]').click();

    // Expect to be redirected to the login page
    await expect(page).toHaveURL(`${BASE_URL}/auth/login`);

    // Expect a success message
    const flashMessage = page.locator(".flash-messages .alert-success"); // Target within container
    await expect(flashMessage).toBeVisible();
    await expect(flashMessage).toContainText(
      "Registration successful! Please log in."
    );
  });

  test("should show error if registering with existing username", async ({
    page,
  }) => {
    // First, register the user so they exist
    await page.goto(`${BASE_URL}/auth/register`);
    await page.locator("#username").fill(username); // Use the same username
    await page.locator("#password").fill(password);
    await page.locator('button[type="submit"]').click();
    // Wait for an element on the login page to appear after redirect
    await page.locator("#username").waitFor({ state: "visible" });

    // Now, try to register again with the same username
    await page.goto(`${BASE_URL}/auth/register`);
    await page.locator("#username").fill(username); // Same username again
    await page.locator("#password").fill("anotherpassword");
    await page.locator('button[type="submit"]').click();

    // Expect to stay on the register page
    await expect(page).toHaveURL(`${BASE_URL}/auth/register`);

    // Expect an error message
    const flashMessage = page.locator(".flash-messages .alert-danger"); // Target within container
    await expect(flashMessage).toBeVisible();
    await expect(flashMessage).toContainText(
      `User ${username} is already registered.`
    );
  });

  test("should allow a registered user to login and access dashboard", async ({
    page,
  }) => {
    // Ensure user is registered first (using the same logic as the registration test)
    await page.goto(`${BASE_URL}/auth/register`);
    await page.locator("#username").fill(username);
    await page.locator("#password").fill(password);
    await page.locator('button[type="submit"]').click();
    // Removed the unreliable URL check here.

    // Go to login page explicitly after registration attempt
    await page.goto(`${BASE_URL}/auth/login`);

    // Fill out the login form
    await page.locator("#username").fill(username);
    await page.locator("#password").fill(password);
    await page.locator('button[type="submit"]').click();

    // Expect to be redirected to the dashboard
    await expect(page).toHaveURL(`${BASE_URL}/`); // Root path is dashboard

    // Expect dashboard content to be visible
    await expect(page.locator("h1")).toContainText(
      "Arkham Asylum Security Dashboard"
    );
    await expect(page.locator(".auth-links")).toContainText(
      `Welcome, ${username}!`
    );
    await expect(page.locator(".auth-links")).toContainText("Logout");
  });

  test("should show error on login with incorrect password", async ({
    page,
  }) => {
    // Ensure user is registered first
    await page.goto(`${BASE_URL}/auth/register`);
    await page.locator("#username").fill(username);
    await page.locator("#password").fill(password);
    await page.locator('button[type="submit"]').click();
    // Wait for an element on the login page to appear after redirect
    await page.locator("#username").waitFor({ state: "visible" });

    // Go to login page (already there, but goto ensures clean state if needed)
    await page.goto(`${BASE_URL}/auth/login`);

    // Fill out the login form with wrong password
    await page.locator("#username").fill(username);
    await page.locator("#password").fill("wrongpassword");
    await page.locator('button[type="submit"]').click();

    // Expect to stay on the login page
    await expect(page).toHaveURL(`${BASE_URL}/auth/login`);

    // Expect an error message
    const flashMessage = page.locator(".flash-messages .alert-danger"); // Target within container
    await expect(flashMessage).toBeVisible();
    await expect(flashMessage).toContainText("Incorrect password.");
  });

  test("should show error on login with non-existent username", async ({
    page,
  }) => {
    // Go to login page
    await page.goto(`${BASE_URL}/auth/login`);

    // Fill out the login form with a username that doesn't exist
    await page.locator("#username").fill("nonexistentuser");
    await page.locator("#password").fill("password");
    await page.locator('button[type="submit"]').click();

    // Expect to stay on the login page
    await expect(page).toHaveURL(`${BASE_URL}/auth/login`);

    // Expect an error message
    const flashMessage = page.locator(".flash-messages .alert-danger"); // Target within container
    await expect(flashMessage).toBeVisible();
    await expect(flashMessage).toContainText("Incorrect username.");
  });

  test("should allow a logged-in user to logout", async ({ page }) => {
    // Register and login first
    await page.goto(`${BASE_URL}/auth/register`);
    await page.locator("#username").fill(username);
    await page.locator("#password").fill(password);
    await page.locator('button[type="submit"]').click();
    await page.goto(`${BASE_URL}/auth/login`);
    await page.locator("#username").fill(username);
    await page.locator("#password").fill(password);
    await page.locator('button[type="submit"]').click();
    await expect(page).toHaveURL(`${BASE_URL}/`); // Ensure login was successful

    // Click the logout link
    await page.locator('a:has-text("Logout")').click();

    // Expect to be redirected to the login page
    await expect(page).toHaveURL(`${BASE_URL}/auth/login`);

    // Expect a logout message
    const flashMessage = page.locator(".flash-messages .alert-info"); // Target within container
    await expect(flashMessage).toBeVisible();
    await expect(flashMessage).toContainText("You have been logged out.");

    // Ensure login/register links are visible again
    await expect(page.locator(".auth-links")).toContainText("Login");
    await expect(page.locator(".auth-links")).toContainText("Register");
  });

  test("should redirect unauthenticated user trying to access dashboard", async ({
    page,
  }) => {
    // Attempt to go directly to the dashboard without logging in
    await page.goto(`${BASE_URL}/`);

    // Expect to be redirected to the login page
    await expect(page).toHaveURL(`${BASE_URL}/auth/login`);

    // Optionally, check for login form elements to confirm it's the login page
    await expect(page.locator("#username")).toBeVisible();
    await expect(page.locator("#password")).toBeVisible();
  });
});
