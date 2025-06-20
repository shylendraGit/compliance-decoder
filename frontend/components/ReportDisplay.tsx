'use client';

export default function ReportDisplay({ report }: { report: any }) {
  return (
    <div className="mt-6 bg-gray-50 p-4 rounded border">
      <h2 className="text-lg font-bold mb-2">Scan Result</h2>
      <p className="text-sm">
        <strong>Risk Level:</strong> {report.risk_level}
      </p>
      {report.flags && report.flags.length > 0 && (
        <ul className="mt-2 list-disc list-inside text-sm text-red-600">
          {report.flags.map((flag: string, idx: number) => (
            <li key={idx}>{flag}</li>
          ))}
        </ul>
      )}
      <p className="text-sm mt-2 text-gray-700">
        <strong>GPT Risk Summary:</strong>{' '}
        {report.summary}
      </p>
    </div>
  );
}
