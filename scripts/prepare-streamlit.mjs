import { cp, mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';

const root = process.cwd();
const dist = path.join(root, 'dist');
const target = path.join(root, 'static');
const component = path.join(root, 'streamlit_component', 'frontend');

await mkdir(target, { recursive: true });
await mkdir(component, { recursive: true });

await cp(dist, target, { recursive: true, force: true });
await cp(dist, component, { recursive: true, force: true });

for (const folder of [target, component]) {
  const indexPath = path.join(folder, 'index.html');
  let html = await readFile(indexPath, 'utf8');
  html = html.replaceAll('/app/static/', './');
  await writeFile(indexPath, html);
}

console.log('Prepared static and component frontend assets.');
