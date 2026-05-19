<template>
  <section class="mx-auto max-w-md min-h-screen" :style="{ backgroundColor: '#F8FAFC' }">
    <div class="flex flex-col gap-2 bg-background p-6">
      <span class="text-primary text-5xl" aria-hidden="true"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="m3.75 13.5 10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75Z" /></svg></span>
      <p class="text-3xl font-bold text-center">Welcome back</p>
      <p class="text-[#64748B] text-sm text-center">Sign in to continue to your dashboard</p>
      <input type="text" placeholder="Email address" class=" w-full px-3 py-2 rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-violet-500" />
      <input type="text" placeholder="Password" class=" w-full px-3 py-2 rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-violet-500" />
      <button type="button" class="bg-primary text-[#FFFFFF]">Sign in</button>
      <p class="text-primary text-sm text-center">Don&#x27;t have an account? Create one</p>
    </div>
  </section>
</template>

<script setup>
import { useRouter } from 'vue-router';
const router = useRouter();
</script>
