// Exemple Playwright (à lancer avec npx playwright test)
const { test, expect } = require('@playwright/test');

test('création et suppression de tâche', async ({ page }) => {
  await page.goto('http://localhost:5173');
  await page.fill('#title', 'Tâche E2E');
  await page.fill('#description', 'Test end-to-end');
  await page.click('button[type=submit]');
  await expect(page.locator('.task h3')).toHaveText('Tâche E2E');
  await page.click('.task [data-role=delete]');
  await expect(page.locator('.task h3')).not.toHaveText('Tâche E2E');
});
