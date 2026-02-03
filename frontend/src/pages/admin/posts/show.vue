<template>
        <div>
            <div class="mb-4">
                <h3>SHOW</h3>
            </div>
            <div>
                <div>
                    <div class="bg-white border border-gray-200 p-4">
                        <h3 class="mb-4 text-lg">{{ postStore.post.user.login }}</h3>
                        <p class="text-sm">{{ postStore.post.text }}</p>
                    </div>
                </div>
            </div>
        </div>
</template>

<script setup>
import { usePostStore } from '@/stores/post';
import { onMounted } from 'vue';


defineOptions({
    name: 'Show'
})

onMounted(() => {
    postStore.getPost()
})

const postStore = usePostStore()

</script>



<style scoped>

</style>