import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function Home() {
  const navigate = useNavigate();
  const routes = {"li1":"details","fab":"details"};
  const onTap = (id) => {
    if (routes[id]) navigate("/" + routes[id]);
  };
  return (
    <section className="mx-auto max-w-md min-h-screen">
      <div className="flex flex-col gap-2 bg-background">
        <div className="w-full px-4 py-3 flex items-center justify-between bg-primary text-background">
          <p className="text-background text-xl font-bold">mimic</p>
        </div>
        <div className="rounded-2xl bg-white shadow-sm p-4 bg-[#EEF2FF] rounded-xl p-4">
          <p className="text-2xl font-bold">Good morning, Vladimir</p>
        </div>
        <div className="flex flex-col gap-1 divide-y divide-slate-200">
          <div onClick={() => onTap("li1")} className=" flex items-center justify-between py-3 cursor-pointer"><span>Recent activity</span><span className="text-slate-400">›</span></div>
          <div className=" flex items-center justify-between py-3 cursor-pointer"><span>Saved projects</span><span className="text-slate-400">›</span></div>
          <div className=" flex items-center justify-between py-3 cursor-pointer"><span>Settings</span><span className="text-slate-400">›</span></div>
        </div>
        <button type="button" className="fixed bottom-6 right-6 w-14 h-14 rounded-full shadow-lg flex items-center justify-center bg-primary text-background" onClick={() => onTap("fab")} aria-label="action"><span className="text-2xl">+</span></button>
      </div>
    </section>
  );
}
