export default function App() {
  return (
    <div className="flex h-screen bg-slate-900 text-slate-100">
      <aside className="w-80 border-r border-slate-700 flex flex-col">
        <div className="p-4 border-b border-slate-700">
          <h1 className="text-xl font-bold text-sky-400">DocMind</h1>
          <p className="text-sm text-slate-400 mt-1">Chat with your documents</p>
        </div>
        <div className="flex-1 p-4 text-slate-500 text-sm">
          No documents yet. Upload one to get started.
        </div>
      </aside>
      <main className="flex-1 flex flex-col">
        <div className="flex-1 flex items-center justify-center text-slate-500">
          Upload a document and start asking questions.
        </div>
      </main>
    </div>
  );
}
