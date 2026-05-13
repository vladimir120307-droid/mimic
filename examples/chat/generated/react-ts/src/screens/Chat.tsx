import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function Chat(): React.JSX.Element {
  const navigate = useNavigate();
  const routes: Record<string, string> = {"thread_0":"chat","thread_1":"chat","thread_2":"chat"};
  const onTap = (id: string) => {
    if (routes[id]) navigate("/" + routes[id]);
  };
  return (
    <section className="mx-auto max-w-md min-h-screen">
      <div className="flex flex-col gap-2 bg-[#F1F5F9]">
        <div className="w-full px-4 py-3 flex items-center justify-between bg-primary text-background">
          <span>Anna</span>
        </div>
        <div className="rounded-2xl bg-white shadow-sm p-4 bg-background rounded-xl p-3">
          <span>Hey, free for lunch?</span>
        </div>
        <div className="rounded-2xl bg-white shadow-sm p-4 bg-primary text-background rounded-xl p-3">
          <span>Yes! 12:30 at the usual?</span>
        </div>
        <div className="rounded-2xl bg-white shadow-sm p-4 bg-background rounded-xl p-3">
          <span>Perfect, see you there</span>
        </div>
        <input type="text" placeholder="Type a message" className=" w-full px-3 py-2 rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-violet-500" />
        <button type="button" className="fixed bottom-6 right-6 w-14 h-14 rounded-full shadow-lg flex items-center justify-center bg-primary text-background" aria-label="action"><span className="text-2xl">+</span></button>
      </div>
    </section>
  );
}
