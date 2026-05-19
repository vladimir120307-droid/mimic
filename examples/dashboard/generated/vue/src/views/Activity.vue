<template>
  <section class="mx-auto max-w-md min-h-screen">
    <div class="flex flex-col gap-2 bg-background">
      <div class="w-full px-4 py-3 flex items-center justify-between bg-primary text-background">
        <span>Recent activity</span>
      </div>
      <p class="text-[#94A3B8] text-base text-center">No activity yet — start recording to see something here</p>
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
