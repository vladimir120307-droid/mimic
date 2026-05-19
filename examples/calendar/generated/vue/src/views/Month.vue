<template>
  <section class="mx-auto max-w-md min-h-screen">
    <div class="flex flex-col gap-2 bg-surface">
      <div class="w-full px-4 py-3 flex items-center justify-between bg-primary text-surface">
        <span>May 2026</span>
      </div>
      <div class="flex flex-row items-center gap-2">
        <p class="text-background text-xs text-center">Mon</p>
        <p class="text-background text-xs text-center">Tue</p>
        <p class="text-background text-xs text-center">Wed</p>
        <p class="text-background text-xs text-center">Thu</p>
        <p class="text-background text-xs text-center">Fri</p>
        <p class="text-background text-xs text-center">Sat</p>
        <p class="text-background text-xs text-center">Sun</p>
      </div>
      <div class="flex flex-col gap-1 divide-y divide-slate-200">
        <div class="text-sm text-center" class="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>1</span><span class="text-slate-400">›</span></div>
        <div class="text-sm text-center" class="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>2</span><span class="text-slate-400">›</span></div>
        <div class="text-sm text-center" class="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>3</span><span class="text-slate-400">›</span></div>
        <div class="text-sm text-center" class="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>4</span><span class="text-slate-400">›</span></div>
        <div class="text-sm text-center" class="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>5</span><span class="text-slate-400">›</span></div>
        <div class="text-sm text-center" class="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>6</span><span class="text-slate-400">›</span></div>
        <div class="text-sm text-center" class="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>7</span><span class="text-slate-400">›</span></div>
        <div class="text-sm text-center" class="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>8</span><span class="text-slate-400">›</span></div>
        <div class="text-sm text-center" class="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>9</span><span class="text-slate-400">›</span></div>
        <div class="text-sm text-center" class="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>10</span><span class="text-slate-400">›</span></div>
        <div class="text-sm text-center" class="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>11</span><span class="text-slate-400">›</span></div>
        <div class="text-sm text-center" class="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>12</span><span class="text-slate-400">›</span></div>
        <div class="text-sm text-center" class="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>13</span><span class="text-slate-400">›</span></div>
        <div class="text-sm text-center" class="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>14</span><span class="text-slate-400">›</span></div>
        <div class="text-sm text-center" class="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>15</span><span class="text-slate-400">›</span></div>
        <div class="text-sm text-center" class="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>16</span><span class="text-slate-400">›</span></div>
        <div class="text-sm text-center" class="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>17</span><span class="text-slate-400">›</span></div>
        <div class="text-sm text-center" class="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>18</span><span class="text-slate-400">›</span></div>
        <div class="text-sm text-center" class="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>19</span><span class="text-slate-400">›</span></div>
        <div class="text-sm text-center" class="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>20</span><span class="text-slate-400">›</span></div>
        <div class="text-sm text-center" class="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>21</span><span class="text-slate-400">›</span></div>
        <div class="text-sm text-center" class="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>22</span><span class="text-slate-400">›</span></div>
        <div class="text-sm text-center" class="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>23</span><span class="text-slate-400">›</span></div>
        <div class="text-sm text-center" class="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>24</span><span class="text-slate-400">›</span></div>
        <div class="text-sm text-center" class="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>25</span><span class="text-slate-400">›</span></div>
        <div class="text-sm text-center" class="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>26</span><span class="text-slate-400">›</span></div>
        <div class="text-sm text-center" class="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>27</span><span class="text-slate-400">›</span></div>
        <div class="text-sm text-center" class="text-sm text-center flex items-center justify-between py-3 cursor-pointer"><span>28</span><span class="text-slate-400">›</span></div>
      </div>
      <div class="rounded-2xl bg-white shadow-sm p-4 bg-[#ECFDF5] rounded-xl p-4" @click='onTap("next_event")'>
        <p class="text-base font-bold">Next: Design review</p>
        <p class="text-background text-sm">Tomorrow, 10:00</p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { useRouter } from 'vue-router';
const router = useRouter();
const routes = {"next_event":"event_detail"};
function onTap(id) {
  if (routes[id]) router.push('/' + routes[id]);
}
</script>
