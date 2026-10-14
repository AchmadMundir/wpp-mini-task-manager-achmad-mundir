import { useState } from "react";

export default function TaskForm({ onCreate }) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [validation, setValidation] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    if (!title.trim()) {
      setValidation("Task title is required.");
      return;
    }
    setValidation("");
    setSubmitting(true);
    try {
      await onCreate({
        title: title.trim(),
        description: description.trim() || null,
      });
      setTitle("");
      setDescription("");
    } catch (error) {
      setValidation(error.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form className="task-form" onSubmit={handleSubmit} noValidate>
      <div className="field-group">
        <label htmlFor="task-title">Task title</label>
        <input
          id="task-title"
          value={title}
          onChange={(event) => setTitle(event.target.value)}
          placeholder="What needs to be done?"
          maxLength={200}
          disabled={submitting}
        />
      </div>
      <div className="field-group field-grow">
        <label htmlFor="task-description">Description (optional)</label>
        <input
          id="task-description"
          value={description}
          onChange={(event) => setDescription(event.target.value)}
          placeholder="Add useful context"
          disabled={submitting}
        />
      </div>
      <button className="button button-primary align-end" disabled={submitting}>
        {submitting ? "Creating..." : "Create task"}
      </button>
      {validation && <p className="field-error form-error">{validation}</p>}
    </form>
  );
}

