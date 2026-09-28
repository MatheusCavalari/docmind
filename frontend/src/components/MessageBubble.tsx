import type { Message } from "../types";
import { SourcesList } from "./SourcesList";

interface Props {
  message: Message;
}

export function MessageBubble({ message }: Props) {
  const isUser = message.role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[80%] rounded-lg px-4 py-3 ${
          isUser ? "bg-sky-600 text-white" : "bg-slate-800 text-slate-200"
        }`}
      >
        <p className="text-sm whitespace-pre-wrap">{message.content}</p>
        {!isUser && message.sources && <SourcesList sources={message.sources} />}
      </div>
    </div>
  );
}
