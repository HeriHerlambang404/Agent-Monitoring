# Agent Monitor — Handoff

## Status saat ini

Dashboard React + Vite sudah terhubung ke runtime Hermes secara lokal.

## Fitur yang sudah selesai

- Dashboard karakter agent
- Polling data setiap 3 detik
- API lokal Node.js
- Endpoint runtime gateway Hermes
- Endpoint session Hermes
- Adapter Python SQLite read-only
- Session nyata ditampilkan sebagai agent workspace
- Panel live Hermes sessions
- Statistik live untuk active agents, tool calls, token, dan gateway
- Output adapter ASCII-safe untuk menghindari `UnicodeEncodeError` Windows CMD
- Detail recent messages/tool activity session dibaca dari tabel `messages` Hermes secara read-only

## Cara menjalankan

Terminal 1:

```bash
cd C:\Users\Hello\projects\agent-monitor
npm run api
```

Terminal 2:

```bash
cd C:\Users\Hello\projects\agent-monitor
npm run dev
```

Buka `http://localhost:5173`.

## Endpoint

- `http://127.0.0.1:8787/api/status`
- `http://127.0.0.1:8787/api/runtime`
- `http://127.0.0.1:8787/api/sessions`

## File penting

- `src/App.jsx` — komponen utama dan integrasi polling
- `server.cjs` — server API
- `hermes_adapter.py` — pembaca `state.db` Hermes
- `data/status.json` — fallback fixture
- `README.md` — dokumentasi penggunaan

## Verifikasi terakhir

- `npm run build` berhasil
- `npm run lint` berhasil dengan beberapa warning non-blocking tentang `key` JSX dan unused variable
- Adapter berhasil membaca 9 session
- Endpoint `/api/sessions` berhasil merespons data

## Pekerjaan berikutnya

1. Ganti task queue fixture dengan event/task Hermes nyata.
2. Ganti progress estimasi berbasis message count dengan progress berbasis event/tool.
3. Tambahkan detail session saat baris session diklik.
4. Tambahkan SSE/WebSocket agar live tanpa polling.
5. Perbaiki warning lint JSX `key`.
6. Tambahkan error state dan indikator API secara lebih jelas.

## Catatan keamanan

Adapter harus tetap read-only. Jangan menampilkan atau menyimpan credential Hermes ke dashboard atau file dokumentasi.
