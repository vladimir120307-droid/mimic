import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function Month() {
  const navigate = useNavigate();
  const routes = {"next_event":"event_detail"};
  const onTap = (id) => {
    if (routes[id]) navigate("/" + routes[id]);
  };
  return (
    <section className="mx-auto max-w-md min-h-screen">
      <div className="flex flex-col gap-2 bg-[#FFFFFF]">
        <div className="w-full px-4 py-3 flex items-center justify-between bg-[#10B981] text-[#FFFFFF]">
          <span>May 2026</span>
        </div>
        <div className="flex flex-row items-center gap-2">
          <p className="text-[#64748B] text-xs text-center">Mon</p>
          <p className="text-[#64748B] text-xs text-center">Tue</p>
          <p className="text-[#64748B] text-xs text-center">Wed</p>
          <p className="text-[#64748B] text-xs text-center">Thu</p>
          <p className="text-[#64748B] text-xs text-center">Fri</p>
          <p className="text-[#64748B] text-xs text-center">Sat</p>
          <p className="text-[#64748B] text-xs text-center">Sun</p>
        </div>
        <div className="flex flex-col gap-1 divide-y divide-slate-200">
          <div className="text-sm text-center" className="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>1</span><span className="text-slate-400">›</span></div>
          <div className="text-sm text-center" className="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>2</span><span className="text-slate-400">›</span></div>
          <div className="text-sm text-center" className="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>3</span><span className="text-slate-400">›</span></div>
          <div className="text-sm text-center" className="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>4</span><span className="text-slate-400">›</span></div>
          <div className="text-sm text-center" className="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>5</span><span className="text-slate-400">›</span></div>
          <div className="text-sm text-center" className="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>6</span><span className="text-slate-400">›</span></div>
          <div className="text-sm text-center" className="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>7</span><span className="text-slate-400">›</span></div>
          <div className="text-sm text-center" className="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>8</span><span className="text-slate-400">›</span></div>
          <div className="text-sm text-center" className="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>9</span><span className="text-slate-400">›</span></div>
          <div className="text-sm text-center" className="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>10</span><span className="text-slate-400">›</span></div>
          <div className="text-sm text-center" className="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>11</span><span className="text-slate-400">›</span></div>
          <div className="text-sm text-center" className="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>12</span><span className="text-slate-400">›</span></div>
          <div className="text-sm text-center" className="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>13</span><span className="text-slate-400">›</span></div>
          <div className="text-sm text-center" className="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>14</span><span className="text-slate-400">›</span></div>
          <div className="text-sm text-center" className="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>15</span><span className="text-slate-400">›</span></div>
          <div className="text-sm text-center" className="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>16</span><span className="text-slate-400">›</span></div>
          <div className="text-sm text-center" className="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>17</span><span className="text-slate-400">›</span></div>
          <div className="text-sm text-center" className="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>18</span><span className="text-slate-400">›</span></div>
          <div className="text-sm text-center" className="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>19</span><span className="text-slate-400">›</span></div>
          <div className="text-sm text-center" className="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>20</span><span className="text-slate-400">›</span></div>
          <div className="text-sm text-center" className="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>21</span><span className="text-slate-400">›</span></div>
          <div className="text-sm text-center" className="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>22</span><span className="text-slate-400">›</span></div>
          <div className="text-sm text-center" className="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>23</span><span className="text-slate-400">›</span></div>
          <div className="text-sm text-center" className="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>24</span><span className="text-slate-400">›</span></div>
          <div className="text-sm text-center" className="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>25</span><span className="text-slate-400">›</span></div>
          <div className="text-sm text-center" className="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>26</span><span className="text-slate-400">›</span></div>
          <div className="text-sm text-center" className="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>27</span><span className="text-slate-400">›</span></div>
          <div className="text-sm text-center" className="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>28</span><span className="text-slate-400">›</span></div>
        </div>
        <div className="rounded-2xl bg-white shadow-sm p-4 bg-[#ECFDF5] rounded-xl p-4" onClick={() => onTap("next_event")}>
          <p className="text-base font-bold">Next: Design review</p>
          <p className="text-[#64748B] text-sm">Tomorrow, 10:00</p>
        </div>
      </div>
    </section>
  );
}
