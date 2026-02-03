<script setup>
import { useRoute, useRouter } from 'vue-router';
import { onMounted, ref } from 'vue';
import PageLayout from './layouts/PageLayout.vue';
import LoginLayout from './layouts/LoginLayout.vue';
import { useUserStore } from './stores/user';
import { usePostStore } from './stores/post';

defineOptions({
    name: "App"
})

onMounted(() => {
    userStore.checkAuth()
})

const router = useRouter()
const route = useRoute()
const isAdmin = ref(false)

const userStore = useUserStore()
const postStore = usePostStore()

</script>

<template>
    <div>
        <div>
            <LoginLayout v-if="route.name === 'login.index' || route.name === 'register.index'">
                <router-view :key="$route.fullPath"></router-view>
            </LoginLayout>
            <PageLayout v-else>
                <router-view :key="$route.fullPath"></router-view>
            </PageLayout>
        </div>
    </div>
</template>


<style>


</style>
