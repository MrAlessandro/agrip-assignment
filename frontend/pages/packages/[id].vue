<template>
  <div class="container py-4 lg:py-14">
    <div class="mb-4">
      <router-link
        to="/"
        class="flex items-center text-blue-500 hover:underline w-fit">
        <ChevronLeftIcon class="w-6 h-6 mr-1"></ChevronLeftIcon>
        Packages list
      </router-link>
    </div>
    <div
      v-if="loading"
      class="w-full min-h-56 flex justify-center items-center">
      <spinner></spinner>
    </div>
    <template v-else>
      <h1 class="uppercase text-4xl font-bold">
        {{ pack?.name }}
      </h1>

      <div
        class="bg-gray-100 p-4 my-4 rounded-lg grid grid-cols-1 gap-y-2 mb-4">
        <div class="">
          <h2 class="text-xl font-bold">Version</h2>
          <p class="">{{ pack.version }}</p>
        </div>
        <div v-if="pack.installed_size" class="">
          <h2 class="text-xl font-bold">Size</h2>
          <p class="">{{ pack.installed_size }}</p>
        </div>
        <div v-if="pack.architecture">
          <h2 class="text-xl font-bold">Architecture</h2>
          <p class="">{{ pack.architecture }}</p>
        </div>
        <div v-if="pack.priority">
          <h2 class="text-xl font-bold">Priority</h2>
          <p class="">{{ pack.priority }}</p>
        </div>
        <div v-if="pack.section">
          <h2 class="text-xl font-bold">Section</h2>
          <p class="">{{ pack.section }}</p>
        </div>
        <div class="">
          <h2 class="text-xl font-bold">Description</h2>
          <p class="">{{ pack.description }}</p>
        </div>
        <div v-if="pack.maintainer" class="">
          <h2 class="text-xl font-bold">Maintainer</h2>
          <p class="">{{ pack.maintainer }}</p>
        </div>
        <div v-if="pack.original_maintainer" class="">
          <h2 class="text-xl font-bold">Original maintainer</h2>
          <p class="">{{ pack.original_maintainer }}</p>
        </div>
        <div v-if="pack.homepage" class="">
          <h2 class="text-xl font-bold">Homepage</h2>
          <a
            :href="pack.homepage"
            class="block text-blue-500 hover:underline"
            >{{ pack.homepage }}</a
          >
        </div>
      </div>
      <div
        v-if="pack.dependencies.length > 0"
        class="bg-gray-100 p-4 my-4 rounded-lg grid grid-cols-1 gap-y-2">
        <h2 class="text-xl font-bold">Dependencies</h2>
        <div v-if="pack.dependencies?.length > 0" class="">
          <div v-for="dep in pack.dependencies" :key="dep.id">
            <router-link
              :to="`/packages/${dep.id}`"
              class="text-blue-500 hover:underline"
              >{{ dep.name }}</router-link
            >
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { HomeIcon, ChevronLeftIcon, PlusIcon } from "@heroicons/vue/24/solid";

const route = useRoute();
const loading = ref(true);
const pack = ref<any>();

const fetchPackage = async () => {
  const response = await fetch(
    `http://localhost:8000/api/packages/${route.params.id}/`
  );
  const data = await response.json();
  pack.value = data;
};

onMounted(() => {
  fetchPackage().then(() => {
    loading.value = false;
  });
});
</script>
