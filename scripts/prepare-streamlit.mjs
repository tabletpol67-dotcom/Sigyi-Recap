import { cp, mkdir, readFile, writeFile, rm } from 'node:fs/promises';
import path from 'node:path';

const root = process.cwd();
const dist = path.join(root, 'dist');
const staticDir = path.join(root, 'static');
const componentDir = path.join(root, 'streamlit_component', 'frontend');

await mkdir(staticDir, { recursive: true });
await mkdir(componentDir, { recursive: true });

await cp(dist, staticDir, { recursive: true, force: true });

const componentAssets = path.join(componentDir, 'assets');
await rm(componentAssets, { recursive: true, force: true });
await cp(path.join(dist, 'assets'), componentAssets, {
  recursive: true,
  force: true
});

let html = await readFile(path.join(dist, 'index.html'), 'utf8');
html = html.replaceAll('/app/static/', './');
await writeFile(path.join(componentDir, 'app.html'), html);

console.log('Streamlit frontend build prepared.');
