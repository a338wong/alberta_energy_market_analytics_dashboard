const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');

const REPORT_URL = 'https://app.powerbi.com/groups/me/reports/b6382545-f3a9-4cb0-8c1f-065f8aa71b49/02e69f25b0786227ca12?experience=power-bi';
const OUTPUT_PATH = path.join(process.cwd(), 'assets', 'dashboard_preview.png');
const USER_DATA_DIR = path.join(process.cwd(), '.playwright-profile');

async function ensureDir(filePath) {
  await fs.promises.mkdir(path.dirname(filePath), { recursive: true });
}

function commitAndPush(filePath) {
  try {
    execSync(`git add "${filePath}"`, { stdio: 'inherit' });
    execSync(`git commit -m "Auto-update dashboard screenshot"`, { stdio: 'inherit' });
    execSync('git push', { stdio: 'inherit' });
  } catch (error) {
    console.log('No changes to commit or push.');
  }
}

async function main() {
  await ensureDir(OUTPUT_PATH);

  const context = await chromium.launchPersistentContext(USER_DATA_DIR, {
    headless: false,
    channel: 'chromium',
    viewport: { width: 1600, height: 1200 }
  });

  const page = context.pages()[0] || await context.newPage();

  console.log('Opening report...');
  await page.goto(REPORT_URL, { waitUntil: 'domcontentloaded', timeout: 120000 });

  console.log('You have 60 seconds to log in and load the report...');
  await page.waitForTimeout(60000);

  console.log('Taking screenshot...');
  await page.screenshot({
    path: OUTPUT_PATH,
    fullPage: true
  });

  console.log(`Saved screenshot to: ${OUTPUT_PATH}`);

  console.log('Pushing to GitHub...');
  commitAndPush(OUTPUT_PATH);

  await context.close();
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
