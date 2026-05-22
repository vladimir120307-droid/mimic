import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Month from "./screens/Month.jsx";
import Event Detail from "./screens/Event Detail.jsx";

export default function App() {
  return (
    <main className="min-h-screen bg-slate-50 text-slate-900 antialiased">
      <Routes>
        <Route path="/" element={<Month />} />
        <Route path="/event_detail" element={<Event Detail />} />
      </Routes>
    </main>
  );
}
