import React from 'react';

export default function Settings() {
  return (
    <section className="mx-auto max-w-md min-h-screen">
      <div className="flex flex-col gap-2 bg-[#F1F5F9]">
        <div className="w-full px-4 py-3 flex items-center justify-between bg-[#FFFFFF] text-[#0F172A]">
          <span>Settings</span>
        </div>
        <div className="rounded-2xl bg-white shadow-sm p-4 bg-[#FFFFFF] rounded-xl p-4">
          <p className="text-lg font-bold">Vladimir</p>
          <p className="text-[#64748B] text-sm">vladimir@example.com</p>
        </div>
        <div className="rounded-2xl bg-white shadow-sm p-4 bg-[#FFFFFF] rounded-xl pt-2 pr-4 pb-2 pl-4">
          <div className="flex flex-row items-center gap-2">
            <p className="text-base">Push notifications</p>
            <div></div>
          </div>
          <div className="flex flex-row items-center gap-2">
            <p className="text-base">Email digest</p>
            <div></div>
          </div>
          <div className="flex flex-row items-center gap-2">
            <p className="text-base">Do not disturb</p>
            <div></div>
          </div>
        </div>
        <button type="button" className="bg-[#E11D48] text-[#FFFFFF]">Sign out</button>
      </div>
    </section>
  );
}
