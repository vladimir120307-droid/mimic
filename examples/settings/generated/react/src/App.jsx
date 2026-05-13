import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Settings from "./screens/Settings.jsx";

export default function App() {
  return (
    <main className="min-h-screen bg-background text-on-surface antialiased">
      <Routes>
        <Route path="/" element={<Settings />} />
      </Routes>
    </main>
  );
}
