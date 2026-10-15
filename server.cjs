const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const root = __dirname;
const hermesHome = process.env.HERMES_HOME || path.join(process.env.LOCALAPPDATA || '', 'hermes');
const headers = {'Content-Type':'application/json','Cache-Control':'no-store','Access-Control-Allow-Origin':'*'};
const adapter = path.join(root, 'hermes_adapter.py');
const python = process.env.HERMES_PYTHON || 'python';
const readSessions = () => {
  try {
    const output = require('node:child_process').execFileSync(python, [adapter], {encoding: 'utf8', timeout: 1500});
    return JSON.parse(output);
  } catch (error) {
    return {updatedAt: Date.now() / 1000, sessions: [], error: 'adapter_unavailable'};
  }
};
const readJson = (file, fallback) => {
  try { return JSON.parse(fs.readFileSync(file, 'utf8')); }
  catch { return fallback; }
};
const server = http.createServer((req, res) => {
  if (req.url === '/api/status') {
    const data = readJson(path.join(root, 'data', 'status.json'), {updatedAt: new Date().toISOString(), connected: false, agents: []});
    res.writeHead(200, headers);
    return res.end(JSON.stringify(data));
  }
  if (req.url === '/api/sessions') {
    res.writeHead(200, headers);
    return res.end(JSON.stringify(readSessions()));
  }
  if (req.url === '/api/runtime') {
    const state = readJson(path.join(hermesHome, 'gateway_state.json'), {gateway_state: 'unavailable'});
    const runtime = {gatewayState: state.gateway_state || 'unknown', activeAgents: state.active_agents || 0, activeWork: state.active_work || null, sessionStore: state.session_store?.status || 'unknown', platforms: state.platforms || {}, updatedAt: state.updated_at || null};
    res.writeHead(200, headers);
    return res.end(JSON.stringify(runtime));
  }
  res.writeHead(404); res.end('Not found');
});
const port = Number(process.env.PORT || 8787);
server.listen(port, '127.0.0.1', () => console.log(`Agent Monitor API listening on http://127.0.0.1:${port}`));
