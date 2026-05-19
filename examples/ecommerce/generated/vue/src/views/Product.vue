<template>
  <section class="mx-auto max-w-md min-h-screen">
    <div class="flex flex-col gap-2 bg-background">
      <img src="https://picsum.photos/seed/linen/1200/800" alt="Linen shirt" class="" />
      <p class="text-2xl font-bold">Linen shirt</p>
      <p class="text-primary text-lg">$48</p>
      <p class="text-[#64748B] text-sm">Soft, breathable linen with a relaxed cut. Ethically sourced.</p>
      <button type="button" class="bg-on_surface text-background">Add to cart</button>
    </div>
  </section>
</template>

<script setup>
import { useRouter } from 'vue-router';
const router = useRouter();
const routes = {"prod_0":"product_detail","prod_1":"product_detail","prod_2":"product_detail","prod_3":"product_detail"};
function onTap(id) {
  if (routes[id]) router.push('/' + routes[id]);
}
</script>
