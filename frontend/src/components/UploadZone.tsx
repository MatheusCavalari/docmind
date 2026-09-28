import { useCallback, useRef, useState } from "react";

interface Props {
  onUpload: (file: File) => Promise<void>;
}

export function UploadZone({ onUpload }: Props) {
  const [dragging, setDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFile = useCallback(
    async (file: File) => {
      setError(null);
      setUploading(true);
      try {
        await onUpload(file);
      } catch (e) {
        setError(e instanceof Error ? e.message : "Upload failed");
      } finally {
        setUploading(false);
      }
    },
    [onUpload],
  );

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setDragging(false);
      const file = e.dataTransfer.files[0];
      if (file) handleFile(file);
    },
    [handleFile],
  );

  return (
    <div
      onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
      onDragLeave={() => setDragging(false)}
      onDrop={handleDrop}
      onClick={() => inputRef.current?.click()}
      className={`border-2 border-dashed rounded-lg p-4 text-center cursor-pointer transition-colors ${
        dragging ? "border-sky-400 bg-sky-400/10" : "border-slate-600 hover:border-slate-500"
      }`}
    >
      <input
        ref={inputRef}
        type="file"
        accept=".pdf,.md,.txt"
        className="hidden"
        onChange={(e) => {
          const file = e.target.files?.[0];
          if (file) handleFile(file);
          e.target.value = "";
        }}
      />
      {uploading ? (
        <p className="text-sm text-sky-400">Uploading...</p>
      ) : (
        <p className="text-sm text-slate-400">
          Drop a file here or click to upload
          <br />
          <span className="text-xs">PDF, Markdown, or TXT (max 10MB)</span>
        </p>
      )}
      {error && <p className="text-xs text-red-400 mt-2">{error}</p>}
    </div>
  );
}
