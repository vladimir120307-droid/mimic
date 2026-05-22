import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function Inbox() {
  const navigate = useNavigate();
  const routes = {"thread_0":"chat","thread_1":"chat","thread_2":"chat"};
  const onTap = (id) => {
    if (routes[id]) navigate("/" + routes[id]);
  };
  return (
    <section className="mx-auto max-w-md min-h-screen">
      <div className="flex flex-col gap-2 bg-[#FFFFFF]">
        <div className="w-full px-4 py-3 flex items-center justify-between bg-[#0EA5E9] text-[#FFFFFF]">
          <span>Messages</span>
        </div>
        <input type="text" placeholder="Search conversations" className=" w-full px-3 py-2 rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-violet-500" />
        <div className="flex flex-col gap-1 divide-y divide-slate-200">
          <div className="text-base font-semibold" onClick={() => onTap("thread_0")} className="text-base font-semibold flex items-center justify-between py-3 cursor-pointer"><span>Anna</span><span className="text-slate-400">›</span></div>
          <div className="text-base font-semibold" onClick={() => onTap("thread_1")} className="text-base font-semibold flex items-center justify-between py-3 cursor-pointer"><span>Boris</span><span className="text-slate-400">›</span></div>
          <div className="text-base font-semibold" onClick={() => onTap("thread_2")} className="text-base font-semibold flex items-center justify-between py-3 cursor-pointer"><span>Team</span><span className="text-slate-400">›</span></div>
          <div className="text-base font-semibold" className="text-base font-semibold flex items-center justify-between py-3 cursor-pointer"><span>Mike</span><span className="text-slate-400">›</span></div>
          <div className="text-base font-semibold" className="text-base font-semibold flex items-center justify-between py-3 cursor-pointer"><span>Family</span><span className="text-slate-400">›</span></div>
        </div>
      </div>
    </section>
  );
}
