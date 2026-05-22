import React from 'react';

export default function Login(): React.JSX.Element {
  return (
    <section className="mx-auto max-w-md min-h-screen" style={{ backgroundColor: "#F8FAFC" }}>
      <div className="flex flex-col gap-2 bg-background p-6">
        <span className="text-primary text-5xl" aria-hidden="true">●</span>
        <p className="text-3xl font-bold text-center">Welcome back</p>
        <p className="text-[#64748B] text-sm text-center">Sign in to continue to your dashboard</p>
        <input type="text" placeholder="Email address" className=" w-full px-3 py-2 rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-violet-500" />
        <input type="text" placeholder="Password" className=" w-full px-3 py-2 rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-violet-500" />
        <button type="button" className="bg-primary text-[#FFFFFF]">Sign in</button>
        <p className="text-primary text-sm text-center">Don&#x27;t have an account? Create one</p>
      </div>
    </section>
  );
}
