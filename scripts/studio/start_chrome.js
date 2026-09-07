// Start the one Chrome that every Studio/TikTok UI automation attaches to.
//
// There is exactly one browser profile for this, at C:/temp/studio_auto/work_profile. It is
// deliberately NOT the owner's normal Chrome profile and NOT a copy of one: Chrome refuses
// --remote-debugging-port on the default profile, and since Chrome 127 the profile directory
// cannot be copied at all (App-Bound Encryption). A dedicated --user-data-dir, signed in once by
// hand, is the only way in. The profile holds a live Google session, so it is a credential store:
// it stays outside the repository and is never copied into it.
//
// This supersedes scripts/tiktok/start_chrome.js, which starts the same profile on the same port
// with a TikTok start page. Only one of them needs to be running; do not add a third.
//
//   node scripts/studio/start_chrome.js                     # opens YouTube Studio
//   node scripts/studio/start_chrome.js https://example.com # any other start page
//
// If the window opens on a Google sign-in page, sign in by hand once. Nothing else in this
// repository can do that step, and nothing else needs it done more than once.

'use strict';

const { spawn } = require('child_process');
const fs = require('fs');

const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const PROFILE = 'C:/temp/studio_auto/work_profile';
const PORT = 9222;

if (!fs.existsSync(CHROME)) {
  console.error(`Chrome not found at ${CHROME}`);
  process.exit(1);
}
const fresh = !fs.existsSync(PROFILE);
fs.mkdirSync(PROFILE, { recursive: true });

const url = process.argv[2] || 'https://studio.youtube.com/';
const p = spawn(CHROME, [
  `--remote-debugging-port=${PORT}`,
  `--user-data-dir=${PROFILE}`,
  '--no-first-run',
  '--no-default-browser-check',
  url,
], { detached: true, stdio: 'ignore' });
p.unref();

console.log(`chrome pid ${p.pid}  port ${PORT}  profile ${PROFILE}`);
if (fresh) {
  console.log('This profile is brand new: sign in to the Prime Documentary channel by hand now.');
  console.log('That is a one-time step. Afterwards the session persists in the profile directory.');
}
