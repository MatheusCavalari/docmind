import type { Document } from "../types";
import { DocumentCard } from "./DocumentCard";
import { UploadZone } from "./UploadZone";

interface Props {
  documents: Document[];
  onUpload: (file: File) => Promise<void>;
  onDelete: (id: string) => void;
}

export function Sidebar({ documents, onUpload, onDelete }: Props) {
  return (
    <aside className="w-80 border-r border-slate-700 flex flex-col max-md:hidden">
      <div className="p-4 border-b border-slate-700">
        <h1 className="text-xl font-bold text-sky-400">DocMind</h1>
        <p className="text-sm text-slate-400 mt-1">Chat with your documents</p>
      </div>
      <div className="p-4">
        <UploadZone onUpload={onUpload} />
      </div>
      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        {documents.length === 0 ? (
          <p className="text-sm text-slate-500">No documents yet.</p>
        ) : (
          documents.map((doc) => (
            <DocumentCard key={doc.id} document={doc} onDelete={onDelete} />
          ))
        )}
      </div>
    </aside>
  );
}
