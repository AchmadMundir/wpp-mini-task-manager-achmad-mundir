import TaskCard from "./TaskCard";

export default function TaskList({
  tasks,
  loading,
  activeTaskId,
  onStatusChange,
  onDelete,
}) {
  if (loading) {
    return <div className="state-card">Loading tasks...</div>;
  }

  if (tasks.length === 0) {
    return (
      <div className="state-card">
        <h3>No tasks here yet</h3>
        <p>Create a task or choose a different status filter.</p>
      </div>
    );
  }

  return (
    <div className="task-list">
      {tasks.map((task) => (
        <TaskCard
          key={task.id}
          task={task}
          busy={activeTaskId === task.id}
          onStatusChange={onStatusChange}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
}

