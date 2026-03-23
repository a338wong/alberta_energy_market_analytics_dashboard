const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');

const REPORT_URL = 'https://app.powerbi.com/groups/me/reports/b6382545-f3a9-4cb0-8c1f-065f8aa71b49/02e69f25b0786227ca12?experience=power-bi';
const OUTPUT_PATH = path.join(process.cwd(), 'assets', 'dashboard_preview.png');
const USER_DATA_DIR = path.join(process.cwd(), '.playwright-profile');

const CLIP = {
  x: 160,
  y: 90,
  width: 1400,
  height: 845
};

async function ensureDir(filePath) {
  await fs.promises.mkdir(path.dirname(filePath), { recursive: true });
}

function workingTreeHasOtherChanges() {
  try {
    const output = execSync('git status --porcelain', { encoding: 'utf8' }).trim();
    if (!output) return false;

    const lines = output.split('\n').map((s) => s.trim()).filter(Boolean);
    const otherChanges = lines.filter(
      (line) => !line.endsWith('assets/dashboard_preview.png')
    );

    return otherChanges.length > 0;
  } catch {
    return true;
  }
}

function commitAndPushScreenshot(filePath) {
  try {
    execSync(`git add "${filePath}"`, { stdio: 'inherit' });

    try {
      execSync(`git diff --cached --quiet -- "${filePath}"`, { stdio: 'pipe' });
      console.log('No new screenshot changes to commit.');
      return;
    } catch {
      // staged diff exists
    }

    execSync(`git commit -m "Auto-update dashboard screenshot"`, { stdio: 'inherit' });

    if (workingTreeHasOtherChanges()) {
      console.log('Skipped auto-push because other local files have changes.');
      console.log('Run `git status` and commit or discard those changes first, then push manually.');
      return;
    }

    execSync('git pull --rebase origin main', { stdio: 'inherit' });
    execSync('git push origin main', { stdio: 'inherit' });
  } catch (error) {
    console.error('Git step failed.');
    console.error(error.message);
  }
}

async function main() {
  await ensureDir(OUTPUT_PATH);

  const context = await chromium.launchPersistentContext(USER_DATA_DIR, {
    headless: true,
    channel: 'chromium',
    viewport: { width: 1600, height: 1200 }
  });

  const page = context.pages()[0] || await context.newPage();

  console.log('Opening report...');
  await page.goto(REPORT_URL, { waitUntil: 'domcontentloaded', timeout: 120000 });

  console.log('Waiting for report to render...');
  await page.waitForTimeout(10000);

  console.log('Taking clipped screenshot...');
  await page.screenshot({
    path: OUTPUT_PATH,
    clip: CLIP
  });

  console.log(`Saved screenshot to: ${OUTPUT_PATH}`);

  console.log('Committing and pushing screenshot...');
  commitAndPushScreenshot(OUTPUT_PATH);

  await context.close();
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
