import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Month from "./screens/Month.tsx";
import EventDetail from "./screens/EventDetail.tsx";

export default function App(): React.JSX.Element {
  return (
    <main className="min-h-screen bg-background text-on-surface antialiased">
      <Routes>
        <Route path="/" element={<Month />} />
        <Route path="/event_detail" element={<EventDetail />} />
      </Routes>
    </main>
  );
}
