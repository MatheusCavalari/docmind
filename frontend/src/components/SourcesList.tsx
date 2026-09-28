import { useState } from "react";
import type { Source } from "../types";

interface Props {
  sources: Source[];
}

export function SourcesList({ sources }: Props) {
  const [expanded, setExpanded] = useState(false);

  if (sources.length === 0) return null;

  return (
    <div className="mt-2">
      <button
        onClick={() => setExpanded(!expanded)}
        className="text-xs text-sky-400 hover:text-sky-300 transition-colors"
      >
        {expanded ? "Hide" : "Show"} {sources.length} source{sources.length > 1 ? "s" : ""}
      </button>
      {expanded && (
        <div className="mt-2 space-y-2">
          {sources.map((source, i) => (
            <div key={i} className="text-xs bg-slate-900 rounded p-2">
              <p className="font-medium text-sky-400">{source.document}</p>
              <p className="text-slate-400 mt-1">{source.excerpt}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
