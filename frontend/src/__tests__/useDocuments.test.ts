import { renderHook, act, waitFor } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { useDocuments } from "../hooks/useDocuments";

describe("useDocuments", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it("fetches documents on mount", async () => {
    const mockDocs = [
      { id: "1", filename: "test.pdf", chunks: 5, created_at: "2026-01-01" },
    ];
    vi.spyOn(globalThis, "fetch").mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockDocs),
    } as Response);

    const { result } = renderHook(() => useDocuments());
    await waitFor(() => {
      expect(result.current.documents).toEqual(mockDocs);
    });
  });

  it("uploads a document and refreshes", async () => {
    vi.spyOn(globalThis, "fetch")
      .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve([]) } as Response)
      .mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({ id: "2", filename: "new.txt", chunks: 3, created_at: "" }),
      } as Response)
      .mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve([{ id: "2", filename: "new.txt", chunks: 3, created_at: "" }]),
      } as Response);

    const { result } = renderHook(() => useDocuments());
    await waitFor(() => expect(result.current.loading).toBe(false));

    await act(async () => {
      await result.current.upload(new File(["content"], "new.txt"));
    });

    await waitFor(() => {
      expect(result.current.documents).toHaveLength(1);
    });
  });

  it("removes a document and refreshes", async () => {
    const docs = [{ id: "1", filename: "test.pdf", chunks: 5, created_at: "" }];
    vi.spyOn(globalThis, "fetch")
      .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve(docs) } as Response)
      .mockResolvedValueOnce({ ok: true } as Response)
      .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve([]) } as Response);

    const { result } = renderHook(() => useDocuments());
    await waitFor(() => expect(result.current.documents).toHaveLength(1));

    await act(async () => {
      await result.current.remove("1");
    });

    await waitFor(() => {
      expect(result.current.documents).toHaveLength(0);
    });
  });
});
