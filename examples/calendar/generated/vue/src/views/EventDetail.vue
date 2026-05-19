<template>
  <section class="mx-auto max-w-md min-h-screen">
    <div class="flex flex-col gap-2 bg-surface">
      <div class="w-full px-4 py-3 flex items-center justify-between bg-primary text-surface">
        <span>Design review</span>
      </div>
      <p class="text-base">Friday May 22, 10:00 — 11:00</p>
      <p class="text-background text-sm">Conference room B / Zoom</p>
      <button type="button" class="bg-primary text-surface">Join meeting</button>
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
