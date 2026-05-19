<script setup>
import Postlist from '@/components/post/Postlist.vue';
import MyButton from '@/components/UI/MyButton.vue';
import EditPhoto from '@/components/user/EditPhoto.vue';
import router from '@/router/router';
import { useChatStore } from '@/stores/chat';
import { usePostStore } from '@/stores/post';
import { useUserStore } from '@/stores/user';
import { useWebsocketStore } from '@/stores/websocket';
import { formatDate } from '@/utils/formatDate';
import { formatTimeAgo } from '@/utils/formatTimeAgo';
import { computed, onMounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { inject } from 'vue'
const apiUrl = inject('apiUrl')
defineOptions({
    name: "UserProfile"
})

onMounted(async () => {
    postStore.$reset()
    const preserved = userStore.avatarVersion
    userStore.$reset()
    userStore.avatarVersion = preserved
    await userStore.getUser(userId)
    await userStore.getFriends(userId, 6)
    await checkFriendship()
    isMyProfile.value = userStore.payload.id === userStore.user.id
    const observer = new IntersectionObserver(
        ([entry]) => {
            if (entry.isIntersecting) {
                postStore.getPosts(userId)
            }
        },
        { threshold: 1 }
    )

    observer.observe(loadMoreRef.value)
})

const userStore = useUserStore()
const postStore = usePostStore()
const chatStore = useChatStore()
const websocketStore = useWebsocketStore()

const friendship = ref(null)
const friendship_status = ref(null)
const friendship_id = ref(null)
const friendship_requesterId = ref(null)

const loadMoreRef = ref(null)
const newDescriptionText = ref('')
const newPostText = ref('')

const isEditPhotoOpen = ref(false)
const isMyProfile = ref(true)

const route = useRoute()
const userId = route.params.id

const visibleFriends = computed(() =>
    userStore.friends_accepted.friends.slice(0, 6)
)

const checkFriendship = async() =>{
    if (userStore.user.id != userStore.payload.id && userStore.isAuth) {
        friendship.value = await userStore.checkFriendship(userId)
        friendship_status.value = friendship.value.status
        friendship_id.value = friendship.value.id
        friendship_requesterId.value = friendship.value.requester_id
    }
}

const sendMessage = async(userId) => {
    const chat_id = await chatStore.storeChat(userId)
    router.push(`/messages/${chat_id}`)
}

const addFriend = async() => {
    await userStore.sendFriendRequest(userStore.user.id)
    await checkFriendship()
}

const deleteFriend = async() => {
    await userStore.deleteFriend(friendship_id.value)
    await checkFriendship()
}

const CreatePost = async () => {
    if (!newPostText.value) return

    await postStore.storePost(userId, newPostText.value)
    newPostText.value = ""
}

const CreateDescription = async () => {
    if (!newDescriptionText.value) return

    await userStore.updateDescription(newDescriptionText.value)
    newDescriptionText.value = ""
}

const changeAvatar = async (file) => {
    await userStore.uploadAvatar(file)
    isEditPhotoOpen.value = false
}

const changeBackground = async (file) => {
    await userStore.uploadBackground(file)
    isEditPhotoOpen.value = false
}

watch(() => route.params.id, (newUserId, oldUserId) => {
    if (newUserId !== oldUserId) {
        postStore.$reset()
        postStore.getPosts(newUserId)
    }
})

watch(isEditPhotoOpen, (isOpen) => {
    if (isOpen) {
        const scrollBarWidth = window.innerWidth - document.documentElement.clientWidth

        document.body.style.overflow = 'hidden'
        document.body.style.paddingRight = `${scrollBarWidth}px`
    } else {
        document.body.style.overflow = ''
        document.body.style.paddingRight = ''
    }
})

</script>

<template>
    <div class="profile-info max-w-5xl mx-auto py-4">
        <div class="profilebg-header flex flex-col">
            <div
            class="h-55 bg-cover bg-center rounded-lg flex group"
            :style="{ backgroundImage: `url(${userStore.bgImage})` }"
            >
                <div v-if="userStore.user.id === userStore.payload.id" class="btn-edit ml-auto mt-3 mr-3 opacity-0 group-hover:opacity-100 transition-opacity">
                    <svg @click.stop="isEditPhotoOpen = true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6 text-gray-500 cursor-pointer">
                        <path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
                    </svg>
                </div>
                <div v-if="isEditPhotoOpen">
                    <EditPhoto
                    @close="isEditPhotoOpen = false"
                    @changeAvatar="changeAvatar"
                    @changeBackground="changeBackground"/>
                </div>
            </div>
            <div class="profile-header -mt-3 flex bg-white rounded-lg pb-4">
                <div class="photo">
                    <img :src="userStore.avatar" class="translate-x-10 -mt-20 border border-white shadow-xl w-40 h-40 rounded-full object-cover">
                </div>
                <div class="profile-name py-6 translate-x-15 text-2xl">
                    <span>{{ userStore.user.login }}</span>
                </div>
                <div class="flex ml-auto px-4 my-auto">
                    <div v-if="!isMyProfile && userStore.isAuth">
                        <button @click="sendMessage(userStore.user.id)" class="bg-gray-400 border border-gray-400 hover:bg-gray-500 cursor-pointer py-2 px-4 text-base rounded-lg text-white">Send message</button>
                    </div>
                    <div class="ml-3">
                        <div v-if="friendship_status==='rejected'" class="btn-friend text-lg">
                            <button @click="addFriend" class="bg-sky-600 hover:bg-sky-700 cursor-pointer py-2 px-2 text-base rounded-lg text-white">Send friend request</button>
                        </div>
                        <div v-if="friendship_status==='accepted'" class="btn-friend text-lg">
                            <button @click="deleteFriend" class="bg-gray-400 hover:bg-gray-500 cursor-pointer py-2 px-2 text-base rounded-lg text-white">Delete friend</button>
                        </div>
                        <div v-if="friendship_status==='pending' && friendship_requesterId === userStore.payload.id" class="btn-friend text-lg">
                            <button @click="deleteFriend" class="bg-gray-400 hover:bg-gray-500 cursor-pointer py-2 px-2 text-base rounded-lg text-white">Pending</button>
                        </div>
                        <div v-if="friendship_status==='pending' && friendship_requesterId != userStore.payload.id" class="btn-friend text-lg">
                            <button @click="addFriend" class="bg-sky-600 hover:bg-sky-700 cursor-pointer py-2 px-2 text-base rounded-lg text-white">Accept friend request</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="content flex h-screen">
            <div class="left-section max-w-2xl w-full">
                <div class="full-info flex mt-4">
                    <div class="description bg-white rounded-lg max-w-2xl w-full py-5 px-5 text-lg">
                        <div v-if="!userStore.user.description && userStore.user.id === userStore.payload.id" class="create-desctiption border-b border-gray-300 pb-3 mb-3">
                            <div class="border-b border-gray-300 text-gray-700">
                                <span>Create description</span>
                            </div>
                            <div class="max-w-2xl w-full text-black mt-3">
                                <textarea v-model="newDescriptionText" maxlength="100" class="w-full h-35 p-3 border border-gray-300 rounded-lg bg-gray-100 resize-none focus:outline-none" placeholder="Description"></textarea>
                            </div>
                            <div class="btn-create flex">
                                <MyButton @click="CreateDescription" :disabled="!newDescriptionText" class="border-blue-500">Create</MyButton>
                                <MyButton @click="newDescriptionText=''" class="ml-auto">Clear</MyButton>
                            </div>
                        </div>
                        <div v-if="userStore.user.description" class="border-b border-gray-300 text-gray-700">
                            <span>Description</span>
                        </div>
                        <div v-if="userStore.user.description" class="w-full whitespace-pre-wrap break-words py-3 mb-3 text-md border-b border-gray-300">
                            <p>{{ userStore.user.description }}</p>
                        </div>
                        <div class="w-full text-md">
                            <p class="text-gray-700">Gender: {{ userStore.gender }}</p>
                        </div>
                        <div class="w-full text-md">
                            <p class="text-gray-700">Birthday: {{ formatDate(userStore.user.birthday) }}</p>
                        </div>
                        <div class="w-full text-md">
                            <p class="text-gray-700">Country: {{ userStore.user.country }}</p>
                        </div>
                        <div class="w-full text-md">
                            <p class="text-gray-700">Account created: {{ formatDate(userStore.user.date_created) }}</p>
                        </div>
                    </div>
                </div>
                <div v-if="userStore.isAuth" class="create-post mt-4 bg-white rounded-lg max-w-2xl w-full py-5 px-5 text-lg mb-2">
                    <div class="header border-b border-gray-300 text-gray-700">
                        Create post
                    </div>
                    <div class="max-w-2xl w-full text-black mt-3">
                        <textarea v-model="newPostText" maxlength="200" class="w-full h-35 p-3 border border-gray-300 rounded-lg bg-gray-100 resize-none focus:outline-none" placeholder="Say something..."></textarea>
                    </div>
                    <div class="btn-create flex">
                        <MyButton @click="CreatePost" :disabled="!newPostText" class="border-blue-500">Create</MyButton>
                        <MyButton @click="newPostText=''" class="ml-auto">Clear</MyButton>
                    </div>
                </div>
                <div class="posts mt-2">
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
            <div class="right-section flex flex-col flex-1">
                <div class="friends max-h-65 h-full mt-4 ml-3 bg-white rounded-lg pt-5 px-5 text-lg overflow-y-auto">
                    <div class="border-b border-gray-300 text-gray-700 mb-3">
                        <router-link v-if="userStore.user.id === userStore.payload.id" :to="{name: 'friends.index'}">Friends: {{ userStore.friends_accepted.total }}</router-link>
                        <router-link v-else :to="{name: 'users.friends.index', params: { id: userStore.user.id } }">Friends: {{ userStore.friends_accepted.total }}</router-link>
                    </div>
                    <div class="flex flex-wrap justify-between gap-4">
                        <div v-for="friend in visibleFriends" :key="friend.id" class="flex flex-col items-center flex-grow-0 flex-shrink-0" style="min-width: 60px; width: calc(33.333% - 1rem);">
                            <router-link v-if="friend.addressee_id === userStore.user.id" class="friend" :to="{name: 'users.index', params: { id: friend.requester_id } }">
                                <div>
                                    <img :src="`${apiUrl}/api/users/${friend.requester_id}/avatar?v=${userStore.avatarVersion}`" class="border border-white w-15 h-15 rounded-full object-cover shrink-0">
                                    <span class="text-sm truncate max-w-[60px] block text-center">{{ friend.requester.login }}</span>
                                </div>
                            </router-link>
                            <router-link v-else class="friend" :to="{name: 'users.index', params: { id: friend.addressee_id  } }">
                                <div>
                                    <img :src="`${apiUrl}/api/users/${friend.addressee_id}/avatar?v=${userStore.avatarVersion}`" class="border border-white w-15 h-15 rounded-full object-cover shrink-0">
                                    <span class="text-sm truncate max-w-[60px] block text-center">{{ friend.addressee.login }}</span>
                                </div>
                            </router-link>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>

</style>