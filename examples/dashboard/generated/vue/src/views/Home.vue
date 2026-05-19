<template>
  <section class="mx-auto max-w-md min-h-screen">
    <div class="flex flex-col gap-2 bg-background">
      <div class="w-full px-4 py-3 flex items-center justify-between bg-primary text-background">
        <p class="text-background text-xl font-bold">mimic</p>
      </div>
      <div class="rounded-2xl bg-white shadow-sm p-4 bg-[#EEF2FF] rounded-xl p-4">
        <p class="text-2xl font-bold">Good morning, Vladimir</p>
      </div>
      <div class="flex flex-col gap-1 divide-y divide-slate-200">
        <div @click='onTap("li1")' class=" flex items-center justify-between py-3 cursor-pointer"><span>Recent activity</span><span class="text-slate-400">›</span></div>
        <div class=" flex items-center justify-between py-3 cursor-pointer"><span>Saved projects</span><span class="text-slate-400">›</span></div>
        <div class=" flex items-center justify-between py-3 cursor-pointer"><span>Settings</span><span class="text-slate-400">›</span></div>
      </div>
      <button type="button" class="fixed bottom-6 right-6 w-14 h-14 rounded-full shadow-lg flex items-center justify-center bg-primary text-background" @click='onTap("fab")' aria-label="action"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" /></svg></button>
    </div>
  </section>
</template>

<script setup>
import { useRouter } from 'vue-router';
const router = useRouter();
const routes = {"li1":"details","fab":"details"};
function onTap(id) {
  if (routes[id]) router.push('/' + routes[id]);
}
</script>
