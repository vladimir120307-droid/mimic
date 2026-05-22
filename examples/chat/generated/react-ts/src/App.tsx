import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Inbox from "./screens/Inbox.tsx";
import Chat from "./screens/Chat.tsx";

export default function App(): React.JSX.Element {
  return (
    <main className="min-h-screen bg-background text-on-surface antialiased">
      <Routes>
        <Route path="/" element={<Inbox />} />
        <Route path="/chat" element={<Chat />} />
      </Routes>
    </main>
  );
}
