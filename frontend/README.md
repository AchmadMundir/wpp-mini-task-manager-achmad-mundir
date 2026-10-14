# Frontend service

React 18 with Vite. This is a browser-side application that communicates with the backend only through HTTP.

## Prerequisites

- Node.js 22 LTS (Node.js 20 also works)
- npm 10+
- A backend API URL; the frontend still starts without a running backend

## Setup and run

```bash
cp .env.example .env
npm install
npm run dev
```

The frontend is available at http://localhost:5173.

`VITE_API_BASE_URL` controls the backend base URL and defaults to `http://localhost:8000`. The URL is defined once in `src/api/client.js` and is not hardcoded across components.

## Production build check

```bash
npm run build
npm run preview
```

The generated static files are placed in `dist/`.

## UI behaviour

- Board list, selection, creation, and deletion.
- Task creation with browser validation.
- Server-side status filtering through `?status=`.
- Status updates and task deletion without full-page reloads.
- Honest loading, empty, API error, and backend-unavailable states.
- API failures are normalized by `src/api/client.js`, allowing components to display one consistent message.

## Independent-service self-check

Stop the backend and leave this service running. The application must still render its navigation and creation controls, with the message: “Unable to connect to the task service. Check that the backend is running.” It must not show a blank page or an uncaught exception.

