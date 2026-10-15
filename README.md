# Agent Monitor

Dashboard lokal untuk memonitor session dan kesehatan runtime Hermes.

## Menjalankan

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

- `GET /api/status` — status dashboard
- `GET /api/runtime` — status gateway Hermes
- `GET /api/sessions` — session Hermes dari `state.db`

## Sumber data Hermes

Adapter membaca secara read-only `%LOCALAPPDATA%\\hermes\\state.db` dan `gateway_state.json`.
Gunakan `HERMES_HOME` untuk override lokasi Hermes dan `HERMES_PYTHON` untuk memilih interpreter Python.

## Verifikasi

```bash
npm run build
npm run lint
```

## File penting

- `src/App.jsx` — UI dan polling live
- `server.cjs` — API lokal
- `hermes_adapter.py` — adapter SQLite read-only
- `data/status.json` — fallback fixture
- `HANDOFF.md` — catatan pengembangan lanjutan
