import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function EventDetail(): React.JSX.Element {
  const navigate = useNavigate();
  const routes: Record<string, string> = {"next_event":"event_detail"};
  const onTap = (id: string) => {
    if (routes[id]) navigate("/" + routes[id]);
  };
  return (
    <section className="mx-auto max-w-md min-h-screen">
      <div className="flex flex-col gap-2 bg-surface">
        <div className="w-full px-4 py-3 flex items-center justify-between bg-primary text-surface">
          <span>Design review</span>
        </div>
        <p className="text-base">Friday May 22, 10:00 — 11:00</p>
        <p className="text-background text-sm">Conference room B / Zoom</p>
        <button type="button" className="bg-primary text-surface">Join meeting</button>
      </div>
    </section>
  );
}
