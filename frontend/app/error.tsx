"use client";

import { useEffect } from "react";

export default function CustomError({ error, reset }: { error: Error; reset: () => void }) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <div style={{ textAlign: "center", padding: "4rem" }}>
      <h1>500 – Internal Server Error</h1>
      <p>Something went wrong. Please try again later.</p>
      <button onClick={() => reset()}>Try again</button>
    </div>
  );
}
