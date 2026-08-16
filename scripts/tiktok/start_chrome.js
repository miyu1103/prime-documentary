const { spawn } = require('child_process');
const exe = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const args = [
  '--remote-debugging-port=9222',
  // work_profile   = v1 (@prime.documentary8), abandoned
  // work_profile_v2 = ended up signed into BOTH accounts, which is how three posts went to v1
  // work_profile_new = one profile, one account. Keep it that way.
  '--user-data-dir=C:/temp/studio_auto/work_profile_new',
  '--no-first-run',
  '--no-default-browser-check',
  'https://www.tiktok.com/tiktokstudio/upload',
];
const p = spawn(exe, args, { detached: true, stdio: 'ignore' });
p.unref();
console.log('start_pid', p.pid);
