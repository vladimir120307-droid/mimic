<template>
  <section class="mx-auto max-w-md min-h-screen">
    <div class="flex flex-col gap-2 bg-background">
      <div class="w-full px-4 py-3 flex items-center justify-between bg-primary text-background">
        <span>Messages</span>
      </div>
      <input type="text" placeholder="Search conversations" class=" w-full px-3 py-2 rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-violet-500" />
      <div class="flex flex-col gap-1 divide-y divide-slate-200">
        <div class="text-base font-semibold" @click='onTap("thread_0")' class="text-base font-semibold flex items-center justify-between py-3 cursor-pointer"><span>Anna</span><span class="text-slate-400">›</span></div>
        <div class="text-base font-semibold" @click='onTap("thread_1")' class="text-base font-semibold flex items-center justify-between py-3 cursor-pointer"><span>Boris</span><span class="text-slate-400">›</span></div>
        <div class="text-base font-semibold" @click='onTap("thread_2")' class="text-base font-semibold flex items-center justify-between py-3 cursor-pointer"><span>Team</span><span class="text-slate-400">›</span></div>
        <div class="text-base font-semibold" class="text-base font-semibold flex items-center justify-between py-3 cursor-pointer"><span>Mike</span><span class="text-slate-400">›</span></div>
        <div class="text-base font-semibold" class="text-base font-semibold flex items-center justify-between py-3 cursor-pointer"><span>Family</span><span class="text-slate-400">›</span></div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { useRouter } from 'vue-router';
const router = useRouter();
const routes = {"thread_0":"chat","thread_1":"chat","thread_2":"chat"};
function onTap(id) {
  if (routes[id]) router.push('/' + routes[id]);
}
</script>
