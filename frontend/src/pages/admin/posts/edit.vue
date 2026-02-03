<template>
    <div class="mb-4">
        <div class="bg-white border border-gray-200 p-4">
            <div class="mb-4">
                <p class="inline-block border border-gray-400 p-4">{{ postStore.post.user.login }}</p>
            </div>
            <div class="mb-4">
                <textarea v-model="postStore.post.text" class="border border-gray-200 p-4 w-full" placeholder="text"></textarea>
            </div>
            <div>
                <a @click.prevent="postStore.updatePost" href="#" class="inline-block px-3 py-2 bg-sky-600 border border-sky-700 text-white">UPDATE POST</a>
            </div>
        </div>
    </div>
</template>

<script setup>
import { usePostStore } from '@/stores/post';
import { onMounted } from 'vue';

defineOptions({
    name: 'Edit'
})

onMounted(() => {
    postStore.getPost()
})

const postStore = usePostStore()


</script>

<style scoped>

</style>