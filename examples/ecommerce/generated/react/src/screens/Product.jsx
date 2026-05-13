import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function Product() {
  const navigate = useNavigate();
  const routes = {"prod_0":"product_detail","prod_1":"product_detail","prod_2":"product_detail","prod_3":"product_detail"};
  const onTap = (id) => {
    if (routes[id]) navigate("/" + routes[id]);
  };
  return (
    <section className="mx-auto max-w-md min-h-screen">
      <div className="flex flex-col gap-2 bg-background">
        <div className="bg-surface">
        </div>
        <p className="text-2xl font-bold">Linen shirt</p>
        <p className="text-primary text-lg">$48</p>
        <p className="text-[#64748B] text-sm">Soft, breathable linen with a relaxed cut. Ethically sourced.</p>
        <button type="button" className="bg-on_surface text-background">Add to cart</button>
      </div>
    </section>
  );
}
