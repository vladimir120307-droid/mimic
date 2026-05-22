import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Inbox from "./screens/Inbox.jsx";
import Chat from "./screens/Chat.jsx";

export default function App() {
  return (
    <main className="min-h-screen bg-slate-50 text-slate-900 antialiased">
      <Routes>
        <Route path="/" element={<Inbox />} />
        <Route path="/chat" element={<Chat />} />
      </Routes>
    </main>
  );
}
