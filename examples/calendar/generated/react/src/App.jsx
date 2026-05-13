import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Month from "./screens/Month.jsx";
import EventDetail from "./screens/EventDetail.jsx";

export default function App() {
  return (
    <main className="min-h-screen bg-background text-on-surface antialiased">
      <Routes>
        <Route path="/" element={<Month />} />
        <Route path="/event_detail" element={<EventDetail />} />
      </Routes>
    </main>
  );
}
