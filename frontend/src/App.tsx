import { Sidebar } from "./components/Sidebar";
import { ChatArea } from "./components/ChatArea";
import { useDocuments } from "./hooks/useDocuments";
import { useChat } from "./hooks/useChat";

export default function App() {
  const { documents, upload, remove } = useDocuments();
  const { messages, sending, send } = useChat();

  return (
    <div className="flex h-screen bg-slate-900 text-slate-100">
      <Sidebar documents={documents} onUpload={upload} onDelete={remove} />
      <ChatArea
        messages={messages}
        sending={sending}
        onSend={(q) => send(q)}
        hasDocuments={documents.length > 0}
      />
    </div>
  );
}
