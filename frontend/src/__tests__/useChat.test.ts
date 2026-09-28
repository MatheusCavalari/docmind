import { renderHook, act } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { useChat } from "../hooks/useChat";

describe("useChat", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it("starts with empty messages", () => {
    const { result } = renderHook(() => useChat());
    expect(result.current.messages).toEqual([]);
    expect(result.current.sending).toBe(false);
  });

  it("clears messages", () => {
    const { result } = renderHook(() => useChat());
    act(() => result.current.clear());
    expect(result.current.messages).toEqual([]);
  });
});
