import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Login from "./screens/Login.tsx";

export default function App(): React.JSX.Element {
  return (
    <main className="min-h-screen bg-background text-on-surface antialiased">
      <Routes>
        <Route path="/" element={<Login />} />
      </Routes>
    </main>
  );
}
