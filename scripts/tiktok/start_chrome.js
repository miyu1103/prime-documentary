const { spawn } = require('child_process');
const exe = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const args = [
  '--remote-debugging-port=9222',
  '--user-data-dir=C:/temp/studio_auto/work_profile',
  '--no-first-run',
  '--no-default-browser-check',
  'https://www.tiktok.com/tiktokstudio/upload',
];
const p = spawn(exe, args, { detached: true, stdio: 'ignore' });
p.unref();
console.log('start_pid', p.pid);
