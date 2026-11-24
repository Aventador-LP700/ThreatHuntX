import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',
  use: {
    baseURL: process.env.THX_URL || 'http://127.0.0.1:8080',
    trace: 'retain-on-failure',
    launchOptions: { executablePath: process.env.THX_CHROMIUM || undefined },
  },
  reporter: 'list',
  workers: 1,
})
