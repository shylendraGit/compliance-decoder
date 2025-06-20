import './globals.css';

export const metadata = {
  title: "Compliance Decoder",
  description: "AI risk analysis for supplier certificates",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-white text-gray-900">
        <main className="min-h-screen p-6">{children}</main>
      </body>
    </html>
  );
}