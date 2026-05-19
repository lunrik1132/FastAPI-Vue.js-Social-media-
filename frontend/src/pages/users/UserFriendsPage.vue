<script setup>
import { useUserStore } from '@/stores/user';
import { onMounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';

import { apiUrl } from '@/main';

onMounted(async () => {
    const preserved = userStore.avatarVersion
    userStore.$reset()
    userStore.avatarVersion = preserved

    await userStore.getFriends(userId, 12)
    console.log(userStore.friends_accepted)
    const observer = new IntersectionObserver(
        ([entry]) => {
            if (entry.isIntersecting) {
                userStore.getFriends(userId, 12)
            }
        },
        { threshold: 1 }
    )

    observer.observe(loadMoreRef.value)
})

const userStore = useUserStore()
const route = useRoute()
const userId = route.params.id

const active = ref('friends')

const loadMoreRef = ref(null)


</script>

<template>
    <div class="friends mt-4 bg-white rounded-lg max-w-2xl w-full pt-5 pb-1 px-5 text-lg mb-2">
        <div class="btns flex pb-2 border-b border-gray-300 text-gray-800">
            <button @click="active='friends'" :class="active==='friends'?'bg-gray-200':'hover:bg-gray-100'" class="text-base px-2 py-1 border border-gray-200 rounded-lg cursor-pointer">Friends</button>
        </div>
        <div class="friends">
            <div class="friends-list mt-3 text-gray-700">
                <span>Total friends: {{ userStore.friends_accepted.total }}</span>
            </div>
            <div v-for="friend in userStore.friends_accepted.friends" :key="friend.id">
                <div class="friend flex px-3 py-2 my-3 rounded-xl bg-gray-200">
                    <div v-if="friend.addressee_id == userId" class="flex">
                        <router-link :to="{name: 'users.index', params: { id: friend.requester_id } }" class="image">
                            <img :src="`${apiUrl}/api/users/${friend.requester_id}/avatar?v=${userStore.avatarVersion}`" class="border border-white w-15 h-15 rounded-full object-cover">
                        </router-link>
                        <router-link :to="{name: 'users.index', params: { id: friend.requester_id } }" class="name ml-3 my-auto">
                            {{ friend.requester.login }}
                        </router-link>
                    </div>
                    <div v-else class="flex">
                        <router-link :to="{name: 'users.index', params: { id: friend.addressee_id } }" class="image">
                            <img :src="`${apiUrl}/api/users/${friend.addressee_id}/avatar?v=${userStore.avatarVersion}`" class="border border-white w-15 h-15 rounded-full object-cover">
                        </router-link>
                        <router-link :to="{name: 'users.index', params: { id: friend.addressee_id } }" class="name ml-3 my-auto">
                            {{ friend.addressee.login }}
                        </router-link>
                    </div>
                    <!-- <div class="btns ml-auto my-auto">
                        <button class="bg-gray-400 border border-gray-400 hover:bg-gray-500 cursor-pointer py-2 px-4 text-base rounded-lg text-white">Send message</button>
                        <button @click="deleteFriend(friend)" class="ml-3 bg-red-800 hover:bg-red-900 cursor-pointer py-2 px-4 text-base rounded-lg text-white">Delete friend</button>
                    </div> -->
                </div>
            </div>
        </div>
        <div ref="loadMoreRef" class="h-10"></div>       
    </div>
</template>

<style scoped>

</style>