import { useCallback, useEffect, useMemo, useState } from "react";

import { api } from "./api/client";
import Alert from "./components/Alert";
import BoardSidebar from "./components/BoardSidebar";
import TaskForm from "./components/TaskForm";
import TaskList from "./components/TaskList";

const filters = [
  ["ALL", "All"],
  ["TODO", "To Do"],
  ["IN_PROGRESS", "In Progress"],
  ["DONE", "Done"],
];

export default function App() {
  const [boards, setBoards] = useState([]);
  const [selectedBoardId, setSelectedBoardId] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [filter, setFilter] = useState("ALL");
  const [boardsLoading, setBoardsLoading] = useState(true);
  const [tasksLoading, setTasksLoading] = useState(false);
  const [error, setError] = useState("");
  const [activeTaskId, setActiveTaskId] = useState(null);

  const selectedBoard = useMemo(
    () => boards.find((board) => board.id === selectedBoardId) || null,
    [boards, selectedBoardId],
  );

  const loadBoards = useCallback(async () => {
    setBoardsLoading(true);
    setError("");
    try {
      const data = await api.listBoards();
      setBoards(data);
      setSelectedBoardId((current) => {
        if (current && data.some((board) => board.id === current)) return current;
        return data[0]?.id ?? null;
      });
    } catch (requestError) {
      setError(requestError.message);
      setBoards([]);
      setSelectedBoardId(null);
    } finally {
      setBoardsLoading(false);
    }
  }, []);

  const loadTasks = useCallback(async () => {
    if (!selectedBoardId) {
      setTasks([]);
      return;
    }
    setTasksLoading(true);
    setError("");
    try {
      setTasks(await api.listTasks(selectedBoardId, filter));
    } catch (requestError) {
      setError(requestError.message);
      setTasks([]);
    } finally {
      setTasksLoading(false);
    }
  }, [filter, selectedBoardId]);

  useEffect(() => {
    loadBoards();
  }, [loadBoards]);

  useEffect(() => {
    loadTasks();
  }, [loadTasks]);

  async function createBoard(name) {
    setError("");
    const board = await api.createBoard(name);
    setBoards((current) => [...current, board]);
    setSelectedBoardId(board.id);
    setFilter("ALL");
  }

  async function createTask(payload) {
    setError("");
    const task = await api.createTask(selectedBoardId, payload);
    if (filter === "ALL" || filter === task.status) {
      setTasks((current) => [...current, task]);
    }
  }

  async function updateTaskStatus(taskId, status) {
    setActiveTaskId(taskId);
    setError("");
    try {
      const updated = await api.updateTaskStatus(taskId, status);
      setTasks((current) => {
        if (filter !== "ALL" && updated.status !== filter) {
          return current.filter((task) => task.id !== taskId);
        }
        return current.map((task) => (task.id === taskId ? updated : task));
      });
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setActiveTaskId(null);
    }
  }

  async function deleteTask(taskId) {
    if (!window.confirm("Delete this task permanently?")) return;
    setActiveTaskId(taskId);
    setError("");
    try {
      await api.deleteTask(taskId);
      setTasks((current) => current.filter((task) => task.id !== taskId));
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setActiveTaskId(null);
    }
  }

  async function deleteSelectedBoard() {
    if (!selectedBoard) return;
    if (!window.confirm(`Delete “${selectedBoard.name}” and all of its tasks?`)) {
      return;
    }
    setError("");
    try {
      await api.deleteBoard(selectedBoard.id);
      const remaining = boards.filter((board) => board.id !== selectedBoard.id);
      setBoards(remaining);
      setSelectedBoardId(remaining[0]?.id ?? null);
      setTasks([]);
    } catch (requestError) {
      setError(requestError.message);
    }
  }

  return (
    <div className="app-shell">
      <BoardSidebar
        boards={boards}
        selectedBoardId={selectedBoardId}
        loading={boardsLoading}
        onSelect={(boardId) => {
          setSelectedBoardId(boardId);
          setFilter("ALL");
        }}
        onCreate={createBoard}
      />

      <main className="main-content">
        <Alert message={error} onRetry={loadBoards} />

        {!selectedBoard ? (
          <section className="welcome-state">
            <div>
              <p className="eyebrow">Ready when you are</p>
              <h2>Select or create a board</h2>
              <p>A board keeps related tasks together in one place.</p>
            </div>
          </section>
        ) : (
          <>
            <header className="board-header">
              <div>
                <p className="eyebrow">Current board</p>
                <h2>{selectedBoard.name}</h2>
              </div>
              <button className="button button-ghost" onClick={deleteSelectedBoard}>
                Delete board
              </button>
            </header>

            <TaskForm onCreate={createTask} />

            <section>
              <div className="toolbar">
                <div>
                  <p className="eyebrow">Board tasks</p>
                  <h2>Work queue</h2>
                </div>
                <div className="filter-group" aria-label="Filter tasks by status">
                  {filters.map(([value, label]) => (
                    <button
                      key={value}
                      className={`filter-button ${filter === value ? "active" : ""}`}
                      onClick={() => setFilter(value)}
                    >
                      {label}
                    </button>
                  ))}
                </div>
              </div>
              <TaskList
                tasks={tasks}
                loading={tasksLoading}
                activeTaskId={activeTaskId}
                onStatusChange={updateTaskStatus}
                onDelete={deleteTask}
              />
            </section>
          </>
        )}
      </main>
    </div>
  );
}

