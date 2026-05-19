<template>
  <section class="mx-auto max-w-md min-h-screen">
    <div class="flex flex-col gap-2 bg-surface">
      <div class="w-full px-4 py-3 flex items-center justify-between bg-background text-on_surface">
        <span>Settings</span>
      </div>
      <div class="rounded-2xl bg-white shadow-sm p-4 bg-background rounded-xl p-4">
        <p class="text-lg font-bold">Vladimir</p>
        <p class="text-[#64748B] text-sm">vladimir@example.com</p>
      </div>
      <div class="rounded-2xl bg-white shadow-sm p-4 bg-background rounded-xl pt-2 pr-4 pb-2 pl-4">
        <div class="flex flex-row items-center gap-2">
          <p class="text-base">Push notifications</p>
          <label class=" inline-flex items-center cursor-pointer"><input type="checkbox" class="sr-only peer" checked /><div class="w-11 h-6 bg-slate-200 peer-checked:bg-primary rounded-full transition-colors"></div></label>
        </div>
        <div class="flex flex-row items-center gap-2">
          <p class="text-base">Email digest</p>
          <label class=" inline-flex items-center cursor-pointer"><input type="checkbox" class="sr-only peer" checked /><div class="w-11 h-6 bg-slate-200 peer-checked:bg-primary rounded-full transition-colors"></div></label>
        </div>
        <div class="flex flex-row items-center gap-2">
          <p class="text-base">Do not disturb</p>
          <label class=" inline-flex items-center cursor-pointer"><input type="checkbox" class="sr-only peer" checked /><div class="w-11 h-6 bg-slate-200 peer-checked:bg-primary rounded-full transition-colors"></div></label>
        </div>
      </div>
      <button type="button" class="bg-primary text-background">Sign out</button>
    </div>
  </section>
</template>

<script setup>
import { useRouter } from 'vue-router';
const router = useRouter();
</script>
