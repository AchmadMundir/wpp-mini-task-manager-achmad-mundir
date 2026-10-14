# REST API contract

Base URL: `http://localhost:8000`

All request and response bodies use JSON. Every error has one shape:

```json
{
  "error": "VALIDATION_FAILED",
  "message": "title must not be empty",
  "field": "title"
}
```

The optional `field` property is present only for field-level validation errors.

## `GET /api/boards`

Lists boards, oldest first.

Success `200`:

```json
[
  {
    "id": 1,
    "name": "Q3 Website Refresh",
    "created_at": "2026-10-14T08:00:00Z"
  }
]
```

Unexpected error `500`:

```json
{"error":"INTERNAL_ERROR","message":"A database error occurred. Please try again later."}
```

## `POST /api/boards`

Request:

```json
{"name":"Q3 Website Refresh"}
```

Success `201`:

```json
{"id":1,"name":"Q3 Website Refresh","created_at":"2026-10-14T08:00:00Z"}
```

Validation error `422`:

```json
{"error":"VALIDATION_FAILED","message":"Value error, name must not be empty","field":"name"}
```

## `DELETE /api/boards/{boardId}`

Deletes a board and its tasks through the database foreign-key cascade.

Success `204`: no response body.

Not found `404`:

```json
{"error":"NOT_FOUND","message":"Board with id 999 was not found"}
```

## `GET /api/boards/{boardId}/tasks`

Optional query parameter: `status=TODO`, `status=IN_PROGRESS`, or `status=DONE`.

Example: `GET /api/boards/1/tasks?status=IN_PROGRESS`

Success `200`:

```json
[
  {
    "id": 12,
    "board_id": 1,
    "title": "Prepare campaign report",
    "description": "Compile the Q3 results",
    "status": "IN_PROGRESS",
    "created_at": "2026-10-14T08:00:00Z",
    "updated_at": "2026-10-14T09:30:00Z"
  }
]
```

An existing board without matching tasks returns `200` with `[]`.

Invalid filter `422`:

```json
{"error":"VALIDATION_FAILED","message":"status must be one of: TODO, IN_PROGRESS, DONE","field":"status"}
```

Unknown board `404`:

```json
{"error":"NOT_FOUND","message":"Board with id 999 was not found"}
```

## `POST /api/boards/{boardId}/tasks`

Request:

```json
{
  "title": "Prepare campaign report",
  "description": "Compile the Q3 results"
}
```

Success `201`:

```json
{
  "id": 12,
  "board_id": 1,
  "title": "Prepare campaign report",
  "description": "Compile the Q3 results",
  "status": "TODO",
  "created_at": "2026-10-14T08:00:00Z",
  "updated_at": "2026-10-14T08:00:00Z"
}
```

Validation error `422`:

```json
{"error":"VALIDATION_FAILED","message":"Value error, title must not be empty","field":"title"}
```

Unknown board `404`:

```json
{"error":"NOT_FOUND","message":"Board with id 999 was not found"}
```

## `PATCH /api/tasks/{taskId}`

Only status updates are supported.

Request:

```json
{"status":"DONE"}
```

Success `200`:

```json
{
  "id": 12,
  "board_id": 1,
  "title": "Prepare campaign report",
  "description": "Compile the Q3 results",
  "status": "DONE",
  "created_at": "2026-10-14T08:00:00Z",
  "updated_at": "2026-10-14T10:00:00Z"
}
```

Invalid status `422`:

```json
{"error":"VALIDATION_FAILED","message":"status must be one of: TODO, IN_PROGRESS, DONE","field":"status"}
```

Unknown task `404`:

```json
{"error":"NOT_FOUND","message":"Task with id 999 was not found"}
```

## `DELETE /api/tasks/{taskId}`

Success `204`: no response body.

Unknown task `404`:

```json
{"error":"NOT_FOUND","message":"Task with id 999 was not found"}
```

