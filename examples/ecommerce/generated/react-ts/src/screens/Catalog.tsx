import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function Catalog(): React.JSX.Element {
  const navigate = useNavigate();
  const routes: Record<string, string> = {"prod_0":"product_detail","prod_1":"product_detail","prod_2":"product_detail","prod_3":"product_detail"};
  const onTap = (id: string) => {
    if (routes[id]) navigate("/" + routes[id]);
  };
  return (
    <section className="mx-auto max-w-md min-h-screen">
      <div className="flex flex-col gap-2 bg-[#F8FAFC]">
        <div className="w-full px-4 py-3 flex items-center justify-between bg-background text-on_surface">
          <span>Shop</span>
        </div>
        <input type="text" placeholder="Search products" className=" w-full px-3 py-2 rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-violet-500" />
        <div className="relative">
          <div className="rounded-2xl bg-white shadow-sm p-4 bg-background rounded-lg shadow-md p-3" onClick={() => onTap("prod_0")}>
            <img src="https://picsum.photos/seed/linen/400/400" alt="Linen shirt" className="rounded" />
            <p className="text-sm font-semibold">Linen shirt</p>
            <p className="text-primary text-base font-bold">$48</p>
          </div>
          <div className="rounded-2xl bg-white shadow-sm p-4 bg-background rounded-lg shadow-md p-3" onClick={() => onTap("prod_1")}>
            <img src="https://picsum.photos/seed/sweater/400/400" alt="Knit sweater" className="rounded" />
            <p className="text-sm font-semibold">Knit sweater</p>
            <p className="text-primary text-base font-bold">$72</p>
          </div>
          <div className="rounded-2xl bg-white shadow-sm p-4 bg-background rounded-lg shadow-md p-3" onClick={() => onTap("prod_2")}>
            <img src="https://picsum.photos/seed/coat/400/400" alt="Wool coat" className="rounded" />
            <p className="text-sm font-semibold">Wool coat</p>
            <p className="text-primary text-base font-bold">$195</p>
          </div>
          <div className="rounded-2xl bg-white shadow-sm p-4 bg-background rounded-lg shadow-md p-3" onClick={() => onTap("prod_3")}>
            <img src="https://picsum.photos/seed/trousers/400/400" alt="Cotton trousers" className="rounded" />
            <p className="text-sm font-semibold">Cotton trousers</p>
            <p className="text-primary text-base font-bold">$56</p>
          </div>
        </div>
      </div>
    </section>
  );
}
