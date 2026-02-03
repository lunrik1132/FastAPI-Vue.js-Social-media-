<template>
    <div class="mb-4">
        <div class="bg-white border border-gray-200 p-4">
            <div class="mb-4">
                <input v-model="postStore.post.user_id" class="border border-gray-200 p-4 w-full" type="text" placeholder="author">
            </div>
            <div class="mb-4">
                <textarea v-model="postStore.post.text" class="border border-gray-200 p-4 w-full" placeholder="text"></textarea>
            </div>
            <div>
                <a @click.prevent="postStore.storePost" href="#" class="inline-block px-3 py-2 bg-sky-600 border border-sky-700 text-white">STORE POST</a>
            </div>
        </div>
    </div>
</template>

<script setup>
import { usePostStore } from '@/stores/post';
import { onMounted } from 'vue';

defineOptions({
    name: 'Create'
})

onMounted(() => {
    postStore.post = {user: {}}
})

const postStore = usePostStore()


</script>

<style scoped>

</style>