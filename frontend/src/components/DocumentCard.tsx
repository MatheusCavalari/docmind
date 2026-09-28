import type { Document } from "../types";

interface Props {
  document: Document;
  onDelete: (id: string) => void;
}

export function DocumentCard({ document, onDelete }: Props) {
  return (
    <div className="flex items-center justify-between p-3 bg-slate-800 rounded-lg">
      <div className="min-w-0 flex-1">
        <p className="text-sm font-medium text-slate-200 truncate">{document.filename}</p>
        <p className="text-xs text-slate-400">{document.chunks} chunks</p>
      </div>
      <button
        onClick={() => onDelete(document.id)}
        className="ml-2 p-1 text-slate-500 hover:text-red-400 transition-colors"
        aria-label={`Delete ${document.filename}`}
      >
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
        </svg>
      </button>
    </div>
  );
}
