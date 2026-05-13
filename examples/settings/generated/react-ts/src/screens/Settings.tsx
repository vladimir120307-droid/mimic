import React from 'react';

export default function Settings(): React.JSX.Element {
  return (
    <section className="mx-auto max-w-md min-h-screen">
      <div className="flex flex-col gap-2 bg-surface">
        <div className="w-full px-4 py-3 flex items-center justify-between bg-background text-on_surface">
          <span>Settings</span>
        </div>
        <div className="rounded-2xl bg-white shadow-sm p-4 bg-background rounded-xl p-4">
          <p className="text-lg font-bold">Vladimir</p>
          <p className="text-[#64748B] text-sm">vladimir@example.com</p>
        </div>
        <div className="rounded-2xl bg-white shadow-sm p-4 bg-background rounded-xl pt-2 pr-4 pb-2 pl-4">
          <div className="flex flex-row items-center gap-2">
            <p className="text-base">Push notifications</p>
            <label className=" inline-flex items-center cursor-pointer"><input type="checkbox" className="sr-only peer" defaultChecked /><div className="w-11 h-6 bg-slate-200 peer-checked:bg-primary rounded-full transition-colors"></div></label>
          </div>
          <div className="flex flex-row items-center gap-2">
            <p className="text-base">Email digest</p>
            <label className=" inline-flex items-center cursor-pointer"><input type="checkbox" className="sr-only peer" defaultChecked /><div className="w-11 h-6 bg-slate-200 peer-checked:bg-primary rounded-full transition-colors"></div></label>
          </div>
          <div className="flex flex-row items-center gap-2">
            <p className="text-base">Do not disturb</p>
            <label className=" inline-flex items-center cursor-pointer"><input type="checkbox" className="sr-only peer" defaultChecked /><div className="w-11 h-6 bg-slate-200 peer-checked:bg-primary rounded-full transition-colors"></div></label>
          </div>
        </div>
        <button type="button" className="bg-primary text-background">Sign out</button>
      </div>
    </section>
  );
}
