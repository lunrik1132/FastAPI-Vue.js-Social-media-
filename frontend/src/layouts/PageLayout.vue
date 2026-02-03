<script setup>
import router from '@/router/router';
import { useUserStore } from '@/stores/user';
import { ref, watch } from 'vue';


const userStore = useUserStore()

const searchQuery = ref('')
const users = ref([])
const cache = {}

const logout = () => {
    userStore.logoutUser()
    router.push('/login')
}


const debounce = (fn, delay = 300) => {
    let timeout
    return (...args) => {
        clearTimeout(timeout)
        timeout = setTimeout(() => {
        fn(...args)
        }, delay)
    }
}

const fetchUsers = async (query) => {
    if (!query) {
        users.value = []
        return
    }

    if (cache[query]) {
        users.value = cache[query]
        return
    }

    const response = await userStore.getUsersByLogin(query)
    users.value = response.data.users
    cache[query] = response.data.users
}

const gotoUser = (userId) => {
    router.push(`/user/${userId}`)
    searchQuery.value = ""
    users.value = []
}

const debouncedFetchUsers = debounce(fetchUsers, 500)

watch(searchQuery, (newQuery) => {
    debouncedFetchUsers(newQuery)
})

</script>

<template>
    <div class='max-w-screen mx-auto w-full'> 
        <div class='header bg-white shadow-lg sticky top-0 z-50'>
            <div class='header-body max-w-6xl mx-auto px-4 py-2 flex items-center'> 
                <div class="text-lg font-semibold md:w-40">
                    <span>BLOG</span>
                </div>
                <div class="relative">
                    <input v-model="searchQuery" type="text" placeholder="Search..." class="px-3 py-1 bg-white border border-gray-300 rounded-lg bg-gray-50 focus:border-gray-500 focus:outline-none text-base"/>
                    <ul v-if="users.length>0" class="absolute z-10 mt-1 w-full bg-white border rounded max-h-48 overflow-y-auto shadow-lg">
                        <li v-for="user in users" :key="user.id" @click="gotoUser(user.id)" class="px-3 py-2 cursor-pointer hover:bg-gray-200">
                            {{ user.login }}
                        </li>
                    </ul>
                </div>
                <div class="ml-auto text-lg">
                    <span v-if="userStore.isAuth" @click="logout" class="mr-6 cursor-pointer">Log Out</span>
                    <router-link v-if="userStore.isAuth" :to="{name: 'settings.index'}" class="mr-6">Settings</router-link>
                    <router-link v-if="userStore.isAuth" :to="{name: 'users.index', params: { id: userStore.payload.id } }" >MY PROFILE</router-link>
                    <router-link :to="{name: 'login.index'}" v-else>Log in</router-link>
                </div>
            </div>
        </div>
        <div class="page-layout max-w-6xl mx-auto h-[calc(100vh-4rem)] flex">
            <div class="side-bar hidden md:flex md:w-40 flex-col pt-3 sticky top-13 h-[calc(100vh-4rem)]">
                <div class="flex flex-col">
                    <router-link v-if="userStore.isAuth" :to="{name: 'users.index', params: { id: userStore.payload.id } }" class="flex items-center px-4 py-2 hover:bg-gray-200 cursor-pointer">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-5.5 text-blue-500">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                        </svg>
                        <span class="pl-2">Profile</span>
                    </router-link>
                    <router-link v-else :to="{name: 'login.index'}" class="flex items-center px-4 py-2 hover:bg-gray-200 cursor-pointer">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-5.5 text-blue-500">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                        </svg>
                        <span class="pl-2">Profile</span>
                    </router-link>
                    <router-link :to="{name: 'feed.index'}" class="flex items-center px-4 py-2 hover:bg-gray-200 cursor-pointer">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20" stroke-width="0.1" stroke="currentColor" class="size-5 text-blue-500">
                            <path clip-rule="evenodd" d="M11.84 2H8.16c-.93 0-1.67 0-2.26.05-.62.05-1.15.15-1.63.4a4.15 4.15 0 0 0-1.82 1.82 4.26 4.26 0 0 0-.4 1.63C2 6.5 2 7.23 2 8.16v3.68c0 .93 0 1.67.05 2.26.05.62.15 1.15.4 1.63.4.78 1.04 1.42 1.82 1.82.48.25 1.01.35 1.63.4.6.05 1.33.05 2.26.05h3.68c.93 0 1.67 0 2.26-.05a4.26 4.26 0 0 0 1.63-.4 4.15 4.15 0 0 0 1.82-1.82c.25-.48.35-1.01.4-1.63.05-.6.05-1.33.05-2.26V8.16c0-.93 0-1.67-.05-2.26a4.26 4.26 0 0 0-.4-1.63 4.15 4.15 0 0 0-1.82-1.82 4.26 4.26 0 0 0-1.63-.4C13.5 2 12.77 2 11.84 2zm-6.9 1.79c.25-.12.56-.2 1.08-.25.53-.04 1.2-.04 2.17-.04h3.62c.96 0 1.64 0 2.17.04.52.05.83.13 1.07.25.5.25.9.66 1.16 1.16.12.24.2.55.25 1.07l.02.48H3.52l.02-.48c.05-.52.13-.83.25-1.07.25-.5.66-.9 1.16-1.16zM3.5 8v3.81c0 .96 0 1.64.04 2.17.05.52.13.83.25 1.07.25.5.66.9 1.16 1.16.24.12.55.2 1.07.25.53.04 1.2.04 2.17.04h3.62c.96 0 1.64 0 2.17-.04a2.8 2.8 0 0 0 1.07-.25c.5-.25.9-.66 1.16-1.16.12-.24.2-.55.25-1.07.04-.53.04-1.2.04-2.17V8z" fill="currentColor" fill-rule="evenodd"></path>
                        </svg>
                        <span class="pl-2">Feed</span>
                    </router-link>
                    <router-link :to="{name: 'friends.index'}" class="flex items-center px-4 py-2 hover:bg-gray-200 cursor-pointer">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-5 text-blue-500">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M15 19.128a9.38 9.38 0 0 0 2.625.372 9.337 9.337 0 0 0 4.121-.952 4.125 4.125 0 0 0-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 0 1 8.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0 1 11.964-3.07M12 6.375a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0Zm8.25 2.25a2.625 2.625 0 1 1-5.25 0 2.625 2.625 0 0 1 5.25 0Z" />
                        </svg>
                        <span class="pl-2">Friends</span>
                    </router-link>
                    <router-link :to="{name: 'messages.index'}" class="flex items-center px-4 py-2 hover:bg-gray-200 cursor-pointer">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-5 text-blue-500">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 0 1-.923 1.785A5.969 5.969 0 0 0 6 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337Z" />
                        </svg>
                        <span class="pl-2">Messages</span>
                    </router-link>
                </div>
            </div>
            <div class="page-body flex-1">
                <slot></slot>
            </div>
        </div>
    </div>
</template>

<style scoped>

</style>