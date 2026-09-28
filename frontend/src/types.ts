export interface Document {
  id: string;
  filename: string;
  chunks: number;
  created_at: string;
}

export interface Source {
  document: string;
  excerpt: string;
}

export interface Message {
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
}
