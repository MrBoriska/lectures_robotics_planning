import http from 'http';
import { spawn } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const rootDir = join(dirname(fileURLToPath(import.meta.url)), '..');
const PORTS = [5599, 5500];

function checkPort(port) {
  return new Promise((resolve) => {
    const req = http.get(`http://127.0.0.1:${port}/serve.json`, (res) => {
      resolve(res.statusCode < 400 || res.statusCode === 404);
    });
    req.on('error', () => resolve(false));
    req.setTimeout(800, () => {
      req.destroy();
      resolve(false);
    });
  });
}

async function main() {
  const is5599 = await checkPort(5599);
  const is5500 = await checkPort(5500);

  if (is5599) {
    console.log(`✅ [Widgets Server] Сервер уже активен на порту 5599 (5500: ${is5500})`);
    process.exit(0);
  }

  console.log(`🚀 [Widgets Server] Запуск сервера интерактивных виджетов на портах ${PORTS.join(', ')}...`);
  const serveBin = join(rootDir, 'node_modules', '.bin', 'serve');
  const child = spawn(serveBin, ['-l', '5599', '-l', '5500', '-C', '--no-port-switching', '--no-clipboard', '.'], {
    cwd: rootDir,
    detached: true,
    stdio: 'ignore'
  });
  child.unref();

  for (let i = 0; i < 15; i++) {
    await new Promise((r) => setTimeout(r, 200));
    if (await checkPort(5599) && await checkPort(5500)) {
      console.log(`🎉 [Widgets Server] Успешно запущен на http://localhost:5599 и http://localhost:5500`);
      process.exit(0);
    }
  }

  console.log(`ℹ️ [Widgets Server] Фоновый процесс запущен.`);
  process.exit(0);
}

main();
