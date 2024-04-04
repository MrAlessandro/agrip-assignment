<template>
  <div class="container py-4 lg:py-14">
    <h1 class="uppercase text-4xl font-bold">DPKG Status</h1>
    <div
      class="w-full overflow-hidden border border-gray-300 rounded-lg mt-4 flex items-center">
      <input
        type="text"
        v-model="search"
        class="grow p-2 focus:ring-none focus:outline-none"
        placeholder="Search packages..." />
      <MagnifyingGlassIcon
        v-if="search.length == 0"
        class="w-8 h-8 pr-2"></MagnifyingGlassIcon>
      <XCircleIcon
        v-if="search.length > 0"
        @click="search = ''"
        class="w-8 h-8 pr-2 cursor-pointer"></XCircleIcon>
    </div>
    <div
      v-if="loading"
      class="w-full min-h-56 flex justify-center items-center">
      <spinner></spinner>
    </div>
    <div v-else>
      <div v-for="pack in packs" :key="pack.id">
        <div class="bg-gray-100 p-4 my-4 rounded-lg md:flex md:items-center">
          <div class="grow">
            <h2 class="text-xl font-bold">
              {{ pack.name }}
              <small class="font-normal">{{ pack.version }}</small>
            </h2>
            <p class="line-clamp-1 mb-1">{{ pack.description }}</p>
            <p v-if="(pack.dependencies?.length || 0) > 0" class="line-clamp-1">
              <strong>Dependencies: </strong>
              <span v-for="(dep, index) in pack.dependencies">
                <RouterLink
                  :to="`/packages/${dep.id}`"
                  class="text-blue-500 hover:underline">
                  {{ dep.name }} </RouterLink
                >{{ index == pack.dependencies.length - 1 ? "" : ", " }}
              </span>
            </p>
          </div>
          <div class="flex items-center mt-3 md:mt-0 md:ml-2 w-full md:w-fit">
            <router-link
              :to="`/packages/${pack.id}`"
              class="bg-blue-500 text-white px-4 py-2 rounded-lg flex items-center w-full md:w-fit justify-center">
              Details
              <ChevronRightIcon class="w-6 h-6 ml-1"></ChevronRightIcon>
            </router-link>
          </div>
        </div>
      </div>
      <div
        v-if="nextPageLoading"
        class="w-full min-h-56 flex justify-center items-center">
        <spinner></spinner>
      </div>
      <div v-if="packs.length > 0 && nextPage == undefined" class="py-14">
        <p class="text-center text-gray-500">No more packages</p>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import {
  ChevronRightIcon,
  MagnifyingGlassIcon,
  XCircleIcon,
} from "@heroicons/vue/24/solid";

const loading = ref(true);
const packs = ref<any[]>([]);
const nextPage = ref<string | undefined>();
const nextPageLoading = ref(false);
const search = ref("");

let debounceTimer: ReturnType<typeof setTimeout> | null = null;

watch(search, () => {
  if (debounceTimer) {
    clearTimeout(debounceTimer);
  }

  debounceTimer = setTimeout(() => {
    loading.value = true;
    packs.value = [];
    fetchPackages("http://localhost:8000/api/packages/").then(() => {
      loading.value = false;
    });
  }, 500); // Adjust the debounce delay as needed (in milliseconds)
});

const fetchPackages = async (url: string) => {
  let pUrl = new URL(url);
  if (search.value) {
    pUrl.searchParams.set("search", search.value);
  }
  const response = await fetch(pUrl);
  const data = await response.json();
  packs.value.push(...data.results);
  if (data.next) {
    nextPage.value = data.next;
  } else {
    nextPage.value = undefined;
  }
  loading.value = false;
};

onMounted(() => {
  window.addEventListener("scroll", handleScroll);
  fetchPackages("http://localhost:8000/api/packages/").then(() => {
    loading.value = false;
  });
});

onUnmounted(() => {
  window.removeEventListener("scroll", handleScroll);
});

const handleScroll = (e: Event) => {
  const reachBottom =
    document.documentElement.scrollTop + window.innerHeight >=
    document.documentElement.offsetHeight;
  if (reachBottom && nextPage.value && !nextPageLoading.value) {
    nextPageLoading.value = true;
    fetchPackages(nextPage.value).then(() => {
      nextPageLoading.value = false;
    });
  }
};
</script>
