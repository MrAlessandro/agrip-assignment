<template>
  <div class="container">
    <div
      v-if="loading"
      class="w-full min-h-56 flex justify-center items-center">
      <spinner></spinner>
    </div>
    <template v-else>
      <h1 class="uppercase text-4xl font-bold">{{ pack?.name }}</h1>

      <div class="bg-gray-100 p-4 my-4 rounded-lg">
        <h2 class="text-xl font-bold"></h2>
        <p class="line-clamp-1">Package Description</p>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";

const loading = ref(true);
const pack = ref<any>(null);

const fetchPackage = async () => {
  const response = await fetch("http://localhost:8000/api/packages/");
  const data = await response.json();
  pack.value = data.results;
};

onMounted(() => {
  fetchPackage().then(() => {
    //loading.value = false;
  });
});
</script>
