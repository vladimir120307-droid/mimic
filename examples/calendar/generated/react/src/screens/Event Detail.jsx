import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function Event Detail() {
  const navigate = useNavigate();
  const routes = {"next_event":"event_detail"};
  const onTap = (id) => {
    if (routes[id]) navigate("/" + routes[id]);
  };
  return (
    <section className="mx-auto max-w-md min-h-screen">
      <div className="flex flex-col gap-2 bg-[#FFFFFF]">
        <div className="w-full px-4 py-3 flex items-center justify-between bg-[#10B981] text-[#FFFFFF]">
          <span>Design review</span>
        </div>
        <p className="text-base">Friday May 22, 10:00 — 11:00</p>
        <p className="text-[#64748B] text-sm">Conference room B / Zoom</p>
        <button type="button" className="bg-[#10B981] text-[#FFFFFF]">Join meeting</button>
      </div>
    </section>
  );
}
