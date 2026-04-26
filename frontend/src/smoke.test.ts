import { describe, expect, it } from "vitest";

describe("baseline", () => {
  it("vitest runner is wired", () => {
    expect(1 + 1).toBe(2);
  });
});
