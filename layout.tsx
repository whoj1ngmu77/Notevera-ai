import type { Metadata } from 'next';
import './globals.css';
import { Toaster } from 'react-hot-toast';
import { AuthProvider } from '@/context/AuthContext';

export const metadata: Metadata = {
  title: 'Notevera AI – Smart AI Learning Assistant',
  description: 'Transform scattered study materials into structured notes, study plans, and oral exam practice with AI.',
  keywords: ['AI', 'learning', 'study planner', 'notes generator', 'education'],
  authors: [{ name: 'Notevera AI' }],
  openGraph: {
    title: 'Notevera AI',
    description: 'AI-powered smart learning assistant for students',
    type: 'website',
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Orbitron:wght@400;700;900&family=Fira+Code:wght@400;500&display=swap"
          rel="stylesheet"
        />
      </head>
      <body>
        <AuthProvider>
          <Toaster
            position="top-right"
            toastOptions={{
              style: {
                background: 'rgba(13,0,37,0.95)',
                color: '#f0e8ff',
                border: '1px solid rgba(168,85,247,0.4)',
                borderRadius: '12px',
                backdropFilter: 'blur(16px)',
              },
              success: { iconTheme: { primary: '#a855f7', secondary: '#fff' } },
              error: { iconTheme: { primary: '#f472b6', secondary: '#fff' } },
            }}
          />
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
