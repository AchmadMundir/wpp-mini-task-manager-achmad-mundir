const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"
).replace(/\/$/, "");

export class ApiError extends Error {
  constructor(message, status = 0, code = "NETWORK_ERROR", field = null) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.code = code;
    this.field = field;
  }
}

async function request(path, options = {}) {
  let response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
    });
  } catch {
    throw new ApiError(
      "Unable to connect to the task service. Check that the backend is running.",
    );
  }

  if (!response.ok) {
    let details = {};
    try {
      details = await response.json();
    } catch {
      details = {};
    }
    throw new ApiError(
      details.message || `Request failed with status ${response.status}`,
      response.status,
      details.error || "REQUEST_FAILED",
      details.field || null,
    );
  }

  if (response.status === 204) return null;
  return response.json();
}

export const api = {
  listBoards: () => request("/api/boards"),
  createBoard: (name) =>
    request("/api/boards", {
      method: "POST",
      body: JSON.stringify({ name }),
    }),
  deleteBoard: (boardId) =>
    request(`/api/boards/${boardId}`, { method: "DELETE" }),
  listTasks: (boardId, status) => {
    const query = status === "ALL" ? "" : `?status=${encodeURIComponent(status)}`;
    return request(`/api/boards/${boardId}/tasks${query}`);
  },
  createTask: (boardId, payload) =>
    request(`/api/boards/${boardId}/tasks`, {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  updateTaskStatus: (taskId, status) =>
    request(`/api/tasks/${taskId}`, {
      method: "PATCH",
      body: JSON.stringify({ status }),
    }),
  deleteTask: (taskId) =>
    request(`/api/tasks/${taskId}`, { method: "DELETE" }),
};

