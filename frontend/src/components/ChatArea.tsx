import { useEffect, useRef, useState } from "react";
import type { Message } from "../types";
import { MessageBubble } from "./MessageBubble";

interface Props {
  messages: Message[];
  sending: boolean;
  onSend: (question: string) => void;
  hasDocuments: boolean;
}

export function ChatArea({ messages, sending, onSend, hasDocuments }: Props) {
  const [input, setInput] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const question = input.trim();
    if (!question || sending) return;
    setInput("");
    onSend(question);
  };

  if (!hasDocuments) {
    return (
      <main className="flex-1 flex items-center justify-center text-slate-500">
        Upload a document and start asking questions.
      </main>
    );
  }

  return (
    <main className="flex-1 flex flex-col">
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.length === 0 && (
          <div className="flex items-center justify-center h-full text-slate-500">
            Ask a question about your documents.
          </div>
        )}
        {messages.map((msg, i) => (
          <MessageBubble key={i} message={msg} />
        ))}
        <div ref={bottomRef} />
      </div>
      <form onSubmit={handleSubmit} className="p-4 border-t border-slate-700">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question..."
            disabled={sending}
            className="flex-1 bg-slate-800 text-slate-200 rounded-lg px-4 py-2 text-sm placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-sky-400"
          />
          <button
            type="submit"
            disabled={sending || !input.trim()}
            className="bg-sky-500 hover:bg-sky-400 disabled:bg-slate-700 disabled:text-slate-500 text-white rounded-lg px-4 py-2 text-sm font-medium transition-colors"
          >
            Send
          </button>
        </div>
      </form>
    </main>
  );
}
