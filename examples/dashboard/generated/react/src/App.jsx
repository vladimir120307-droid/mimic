import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Home from "./screens/Home.jsx";
import Activity from "./screens/Activity.jsx";

export default function App() {
  return (
    <main className="min-h-screen bg-background text-on-surface antialiased">
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/details" element={<Activity />} />
      </Routes>
    </main>
  );
}
