<template>
  <div class="container pt-14">
    <h1 class="uppercase text-4xl font-bold">DPKG Status</h1>
    <div v-if="loading"></div>
    <div v-else>
      <div v-for="pakage in pakages" :key="pakage.id">
        <div class="bg-gray-100 p-4 my-4 rounded-lg flex items-center">
          <div class="grow">
            <h2 class="text-xl font-bold">{{ pakage.name }}</h2>
            <p class="line-clamp-1">{{ pakage.description }}</p>
          </div>
          <div class="flex items-center">
            <router-link
              :to="`/packages/${pakage.id}`"
              class="bg-blue-500 text-white px-4 py-2 rounded-lg">
              Details
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
const loading = ref(true);
const pakages = ref([]);
const page = ref(1);
const totalPages = ref(0);

const fetchPackages = async () => {
  const response = await fetch("http://localhost:8000/api/packages/");
  const data = await response.json();
  pakages.value = data.results;
  loading.value = false;
};

onMounted(() => {
  fetchPackages().then(() => {
    loading.value = false;
  });
});
</script>
