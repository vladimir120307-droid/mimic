import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function Activity() {
  const navigate = useNavigate();
  const routes = {"li1":"details","fab":"details"};
  const onTap = (id) => {
    if (routes[id]) navigate("/" + routes[id]);
  };
  return (
    <section className="mx-auto max-w-md min-h-screen">
      <div className="flex flex-col gap-2 bg-[#FFFFFF]">
        <div className="w-full px-4 py-3 flex items-center justify-between bg-[#6E56CF] text-[#FFFFFF]">
          <span>Recent activity</span>
        </div>
        <p className="text-[#94A3B8] text-base text-center">No activity yet — start recording to see something here</p>
      </div>
    </section>
  );
}
