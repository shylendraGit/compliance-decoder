"use client";
import React, { useState } from "react";

export default function CertificateUpload({ onResult }: { onResult: (data: any) => void }) {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setError("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("/api/upload_certificate", {
        method: "POST",
        body: formData,
      });

      const result = await res.json();
      onResult(result);
    } catch (err) {
      setError("Failed to upload or analyze file.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <input
        type="file"
        accept=".pdf"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
        className="border p-2 rounded"
      />
      <button
        onClick={handleUpload}
        disabled={!file || loading}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        {loading ? "Scanning..." : "Scan Certificate"}
      </button>
      {error && <p className="text-red-600">{error}</p>}
    </div>
  );
}
