// Exemple Playwright (à lancer avec npx playwright test)
import { test, expect } from '@playwright/test';

test('création et suppression de tâche', async ({ page }) => {
  await page.goto('http://localhost:5173');
  await page.fill('#title', 'Tâche E2E');
  await page.fill('#description', 'Test end-to-end');
  await page.click('button[type=submit]');
  const task = page.locator('.task', { hasText: 'Tâche E2E' });
  await expect(task.first().locator('h3')).toHaveText('Tâche E2E');
  await page.once('dialog', dialog => dialog.accept());
  await task.first().locator('[data-role=delete]').click();
  await page.click('#refreshBtn');
  await expect(task.first()).toBeHidden();
});
