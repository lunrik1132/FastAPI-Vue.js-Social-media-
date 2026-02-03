<script setup>
import router from '@/router/router';
import { useChatStore } from '@/stores/chat';
import { useUserStore } from '@/stores/user';
import { onMounted, ref, watch } from 'vue';

onMounted(async () => {
    const preserved = userStore.avatarVersion
    userStore.$reset()
    userStore.avatarVersion = preserved

    await userStore.getFriends(userStore.payload.id, 12)
    await userStore.getFriendsRequests(12)

    const observer = new IntersectionObserver(
        ([entry]) => {
            if (entry.isIntersecting) {
                active.value === 'friends'? userStore.getFriends(userStore.payload.id, 12) : userStore.getFriendsRequests(12)
            }
        },
        { threshold: 1 }
    )

    observer.observe(loadMoreRef.value)
})

const userStore = useUserStore()
const chatStore = useChatStore()
const active = ref('friends')

const loadMoreRef = ref(null)


const acceptRequest = async(friend) => {
    userStore.friends_pending.friends = userStore.friends_pending.friends.filter(user => user != friend)
    userStore.friends_pending.total--
    userStore.friends_accepted.total++
    userStore.friends_accepted.friends.push(friend)
    await userStore.sendFriendRequest(friend.requester_id)
}

const rejectRequest = async(friend) => {
    userStore.friends_pending.friends = userStore.friends_pending.friends.filter(user => user != friend)
    userStore.friends_pending.total--
    await userStore.rejectFriendRequest(friend.requester_id)
}

const sendMessage = async(friend) => {
    if (userStore.payload.id == friend.requester_id){
        const chat_id = await chatStore.storeChat(friend.addressee_id)
        router.push(`/messages/${chat_id}`)
    } else {
        const chat_id = await chatStore.storeChat(friend.requester_id)
        router.push(`/messages/${chat_id}`)
    }
}

const deleteFriend = async(friend) => {
    userStore.friends_accepted.friends = userStore.friends_accepted.friends.filter(user => user != friend)
    userStore.friends_accepted.total--
    await userStore.deleteFriend(friend.id)
}

</script>

<template>
    <div class="friends mt-4 bg-white rounded-lg max-w-2xl w-full pt-5 pb-1 px-5 text-lg mb-2">
        <div class="btns flex pb-2 border-b border-gray-300 text-gray-800">
            <button @click="active='friends'" :class="active==='friends'?'bg-gray-200':'hover:bg-gray-100'" class="text-base px-2 py-1 border border-gray-200 rounded-lg cursor-pointer">Friends</button>
            <button @click="active='pending'" :class="active==='pending'?'bg-gray-200':'hover:bg-gray-100'" class="ml-4 text-base border border-gray-200 px-2 py-1 rounded-lg cursor-pointer">Pending</button>
        </div>
        <div v-if="active==='friends'">
            <div class="friends-list mt-3 text-gray-700">
                <span>Total friends: {{ userStore.friends_accepted.total }}</span>
            </div>
            <div v-for="friend in userStore.friends_accepted.friends" :key="friend.id">
                <div class="friend flex px-3 py-2 my-3 rounded-xl bg-gray-200">
                    <div v-if="friend.addressee_id === userStore.payload.id" class="flex">
                        <router-link :to="{name: 'users.index', params: { id: friend.requester_id } }" class="image">
                            <img :src="`http://localhost:8000/api/users/${friend.requester_id}/avatar?v=${userStore.avatarVersion}`" class="border border-white w-15 h-15 rounded-full object-cover">
                        </router-link>
                        <router-link :to="{name: 'users.index', params: { id: friend.requester_id } }" class="name ml-3 my-auto">
                            {{ friend.requester.login }}
                        </router-link>
                    </div>
                    <div v-else class="flex">
                        <router-link :to="{name: 'users.index', params: { id: friend.addressee_id } }" class="image">
                            <img :src="`http://localhost:8000/api/users/${friend.addressee_id}/avatar?v=${userStore.avatarVersion}`" class="border border-white w-15 h-15 rounded-full object-cover">
                        </router-link>
                        <router-link :to="{name: 'users.index', params: { id: friend.addressee_id } }" class="name ml-3 my-auto">
                            {{ friend.addressee.login }}
                        </router-link>
                    </div>
                    <div class="btns ml-auto my-auto">
                        <button @click="sendMessage(friend)" class="bg-gray-400 border border-gray-400 hover:bg-gray-500 cursor-pointer py-2 px-4 text-base rounded-lg text-white">Send message</button>
                        <button @click="deleteFriend(friend)" class="ml-3 bg-red-800 hover:bg-red-900 cursor-pointer py-2 px-4 text-base rounded-lg text-white">Delete friend</button>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="active==='pending'">
            <div class="pending-list mt-3 text-gray-700">
                <span>Total friend requests: {{ userStore.friends_pending.total }}</span>
            </div>
            <div v-for="friend in userStore.friends_pending.friends" :key="friend.id">
                <div class="pending flex px-3 py-2 my-3 rounded-xl bg-gray-200">
                    <router-link :to="{name: 'users.index', params: { id: friend.requester_id } }" class="image">
                        <img :src="`http://localhost:8000/api/users/${friend.requester_id}/avatar?v=${userStore.avatarVersion}`" class="border border-white w-15 h-15 rounded-full object-cover">
                    </router-link>
                    <router-link :to="{name: 'users.index', params: { id: friend.requester_id } }" class="name ml-3 my-auto">
                        {{ friend.requester.login }}
                    </router-link>
                    <div class="btns ml-auto my-auto">
                        <button @click="acceptRequest(friend)" class="bg-sky-600 hover:bg-sky-700 cursor-pointer py-2 px-2 text-base rounded-lg text-white">Accept</button>
                        <button @click="rejectRequest(friend)" class="ml-3 bg-sky-600 hover:bg-sky-700 cursor-pointer py-2 px-2 text-base rounded-lg text-white">Reject</button>
                    </div>
                </div>
            </div>
        </div>
        <div ref="loadMoreRef" class="h-10"></div>       
    </div>
</template>

<style scoped>

</style>