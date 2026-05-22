import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Settings from "./screens/Settings.jsx";

export default function App() {
  return (
    <main className="min-h-screen bg-slate-50 text-slate-900 antialiased">
      <Routes>
        <Route path="/" element={<Settings />} />
      </Routes>
    </main>
  );
}
