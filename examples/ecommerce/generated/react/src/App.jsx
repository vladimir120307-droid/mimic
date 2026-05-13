import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Catalog from "./screens/Catalog.jsx";
import Product from "./screens/Product.jsx";

export default function App() {
  return (
    <main className="min-h-screen bg-background text-on-surface antialiased">
      <Routes>
        <Route path="/" element={<Catalog />} />
        <Route path="/product_detail" element={<Product />} />
      </Routes>
    </main>
  );
}
