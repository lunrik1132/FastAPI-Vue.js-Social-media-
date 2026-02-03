<script setup>
import Postlist from '@/components/post/Postlist.vue';
import { usePostStore } from '@/stores/post';
import { useUserStore } from '@/stores/user';
import { onMounted, ref } from 'vue';



const userStore = useUserStore()
const postStore = usePostStore()
const loadMoreRef = ref(null)

onMounted(async () => {
    const preserved = userStore.avatarVersion
    postStore.$reset()
    userStore.$reset()
    userStore.avatarVersion = preserved

    const observer = new IntersectionObserver(
        ([entry]) => {
            if (entry.isIntersecting) {
                postStore.getAllPosts()
            }
        },
        { threshold: 1 }
    )

    observer.observe(loadMoreRef.value)
})

</script>

<template>
    <div class="feed mt-4">
        <div class="posts">
            <Postlist></Postlist>
        </div>
        <div ref="loadMoreRef" class="h-10"></div>
        <div v-if="postStore.loading" class="text-center py-4 text-gray-500">
            <span>Loading...</span>
        </div>
        <div v-if="!postStore.hasMore" class="text-center py-4 text-gray-400">
            <span>There are no posts left</span>
        </div>
    </div>
</template>

<style>

</style>