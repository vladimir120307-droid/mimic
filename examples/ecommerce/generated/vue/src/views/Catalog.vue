<template>
  <section class="mx-auto max-w-md min-h-screen">
    <div class="flex flex-col gap-2 bg-[#F8FAFC]">
      <div class="w-full px-4 py-3 flex items-center justify-between bg-background text-on_surface">
        <span>Shop</span>
      </div>
      <input type="text" placeholder="Search products" class=" w-full px-3 py-2 rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-violet-500" />
      <div class="relative">
        <div class="rounded-2xl bg-white shadow-sm p-4 bg-background rounded-lg shadow-md p-3" @click='onTap("prod_0")'>
          <img src="https://picsum.photos/seed/linen/400/400" alt="Linen shirt" class="rounded" />
          <p class="text-sm font-semibold">Linen shirt</p>
          <p class="text-primary text-base font-bold">$48</p>
        </div>
        <div class="rounded-2xl bg-white shadow-sm p-4 bg-background rounded-lg shadow-md p-3" @click='onTap("prod_1")'>
          <img src="https://picsum.photos/seed/sweater/400/400" alt="Knit sweater" class="rounded" />
          <p class="text-sm font-semibold">Knit sweater</p>
          <p class="text-primary text-base font-bold">$72</p>
        </div>
        <div class="rounded-2xl bg-white shadow-sm p-4 bg-background rounded-lg shadow-md p-3" @click='onTap("prod_2")'>
          <img src="https://picsum.photos/seed/coat/400/400" alt="Wool coat" class="rounded" />
          <p class="text-sm font-semibold">Wool coat</p>
          <p class="text-primary text-base font-bold">$195</p>
        </div>
        <div class="rounded-2xl bg-white shadow-sm p-4 bg-background rounded-lg shadow-md p-3" @click='onTap("prod_3")'>
          <img src="https://picsum.photos/seed/trousers/400/400" alt="Cotton trousers" class="rounded" />
          <p class="text-sm font-semibold">Cotton trousers</p>
          <p class="text-primary text-base font-bold">$56</p>
        </div>
      </div>
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
