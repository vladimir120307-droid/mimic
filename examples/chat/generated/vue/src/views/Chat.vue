<template>
  <section class="mx-auto max-w-md min-h-screen">
    <div class="flex flex-col gap-2 bg-[#F1F5F9]">
      <div class="w-full px-4 py-3 flex items-center justify-between bg-primary text-background">
        <span>Anna</span>
      </div>
      <div class="rounded-2xl bg-white shadow-sm p-4 bg-background rounded-xl p-3">
        <span>Hey, free for lunch?</span>
      </div>
      <div class="rounded-2xl bg-white shadow-sm p-4 bg-primary text-background rounded-xl p-3">
        <span>Yes! 12:30 at the usual?</span>
      </div>
      <div class="rounded-2xl bg-white shadow-sm p-4 bg-background rounded-xl p-3">
        <span>Perfect, see you there</span>
      </div>
      <input type="text" placeholder="Type a message" class=" w-full px-3 py-2 rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-violet-500" />
      <button type="button" class="fixed bottom-6 right-6 w-14 h-14 rounded-full shadow-lg flex items-center justify-center bg-primary text-background" aria-label="action"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M6 12 3.269 3.125A59.769 59.769 0 0 1 21.485 12 59.768 59.768 0 0 1 3.27 20.875L5.999 12Zm0 0h7.5" /></svg></button>
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
