import React, { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import "./App.css";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000/v1/chat/stream";

function useAutoScroll(containerRef, value) {
  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;
    el.scrollTop = el.scrollHeight;
  }, [value, containerRef]);
}

export default function App() {
  const [input, setInput] = useState("");
  const [streamedText, setStreamedText] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const controllerRef = useRef(null);
  const outRef = useRef(null);

  useAutoScroll(outRef, streamedText);

  const handleSubmit = async (e) => {
    e?.preventDefault();
    if (!input.trim()) return;

    setStreamedText("");
    setError(null);
    setLoading(true);

    if (controllerRef.current) controllerRef.current.abort();
    const controller = new AbortController();
    controllerRef.current = controller;

    try {
      const res = await fetch(BACKEND_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: input }),
        signal: controller.signal,
      });

      if (!res.ok) {
        const txt = await res.text();
        throw new Error(`HTTP ${res.status}: ${txt}`);
      }

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });

        let parts = buffer.split("\n\n");
        buffer = parts.pop();

        for (const part of parts) {
          if (!part.trim()) continue;
          if (part.startsWith("data: ")) {
            const jsonStr = part.replace("data: ", "");
            if (jsonStr === "[DONE]") {
              setLoading(false);
              controllerRef.current = null;
              return;
            } else if (jsonStr.startsWith("[ERROR]")) {
              setError(jsonStr);
              setLoading(false);
              controllerRef.current = null;
              return;
            } else {
              const data = JSON.parse(jsonStr);
              for (const char of data.text) {
                setStreamedText((prev) => prev + char);
                await new Promise((r) => setTimeout(r, 10));
              }
            }
          }
        }
      }

      if (buffer.trim().startsWith("data: ")) {
        const jsonStr = buffer.replace("data: ", "");
        const data = JSON.parse(jsonStr);
        setStreamedText((prev) => prev + data.text);
      }

      setLoading(false);
      controllerRef.current = null;
    } catch (err) {
      if (err.name === "AbortError") setError("Stream aborted");
      else setError(err.message);
      setLoading(false);
      controllerRef.current = null;
    }
  };

  const stopStream = () => {
    if (controllerRef.current) controllerRef.current.abort();
  };

  return (
    <div className="app">
      <div className="chat-card">
        <h1 className="chat-title">Gemini Chat (Streaming)</h1>

        <div ref={outRef} className="chat-output">
          {streamedText ? (
            <ReactMarkdown>{streamedText}</ReactMarkdown>
          ) : (
            <div className="chat-hint">Assistant responses will stream here…</div>
          )}
          {loading && <span className="cursor">▍</span>}
        </div>

        <form onSubmit={handleSubmit} className="chat-controls">
          <textarea
            placeholder="Type your prompt..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="chat-input"
            rows={3}
          />
          <div className="chat-actions">
            <button type="submit" className="btn" disabled={loading}>
              {loading ? "Streaming..." : "Send"}
            </button>
            <button
              type="button"
              onClick={stopStream}
              className="btn secondary"
              disabled={!loading}
            >
              Stop
            </button>
            {error && <div className="error">Error: {error}</div>}
          </div>
        </form>
      </div>
    </div>
  );
}
