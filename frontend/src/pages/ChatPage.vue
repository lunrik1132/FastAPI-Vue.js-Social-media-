<script setup>
import { useChatStore } from '@/stores/chat'
import { useUserStore } from '@/stores/user'
import { useWebsocketStore } from '@/stores/websocket'
import { nextTick, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import { apiUrl } from '@/main';

onMounted(async() => {
    websocketStore.$reset()
    chatStore.$reset()
    chat.value = await chatStore.getChat(chatId)
    other_user.value = chat.value.members?.find(m => m.user_id !== userStore.payload?.id)
    await chatStore.getMessages(chatId)
    scrollToBottom()

    websocketStore.connect(chatId)


    const observer = new IntersectionObserver(
        async ([entry]) => {
            if (entry.isIntersecting) {
                const el = messagesContainer.value
                const current_scroll = el.scrollHeight
                await chatStore.getMessages(chatId)
                messagesContainer.value.scrollTop = el.scrollHeight - current_scroll
            }
        },
        { threshold: 1 }
    )

    observer.observe(loadMoreRef.value)
})

const chatStore = useChatStore()
const userStore = useUserStore()
const websocketStore = useWebsocketStore()

const chat = ref()
const other_user = ref()

const newMessageText = ref()
const messagesContainer = ref(null)
const loadMoreRef = ref(null)

const route = useRoute()
const chatId = route.params.id

const scrollToBottom = async () => {
    await nextTick()
    const el = messagesContainer.value
    if (el) {
        el.scrollTop = el.scrollHeight
    }
}

const CreateMessage = async () => {
    if (!newMessageText.value) return 
    websocketStore.sendMessage(newMessageText.value)
    newMessageText.value = ""
}

const autoResize = (event) => {
    const textarea = event.target;
    if (textarea.style.height !== "90px"){
        textarea.style.height = (textarea.scrollHeight + 2) + "px";
    }
}

watch(
    () => chatStore.messages.length,
    async (newLen, oldLen) => {
        if (newLen > oldLen && !chatStore.isLoadingHistory) {
            await nextTick()
            scrollToBottom()
        }
    }
)

</script>

<template>
    <div class="chat mt-4 bg-white rounded-lg max-w-2xl w-full h-[85vh] flex flex-col pb-1 text-lg">
        <div v-if="other_user" class="user-info flex shadow py-3 pl-10">
            <router-link :to="{name: 'users.index', params: { id: other_user.user_id } }" class="image">
                <img :src="`${apiUrl}/api/users/${other_user.user_id}/avatar?v=${userStore.avatarVersion}`" class="border border-white w-15 h-15 rounded-full object-cover">
            </router-link>
            <router-link :to="{name: 'users.index', params: { id: other_user.user_id } }" class="name ml-3 my-auto">
                {{ other_user.user.login }}
            </router-link>
        </div>
        <div ref="messagesContainer" class="messages mx-6 flex-1 overflow-y-auto flex flex-col px-5">
            <div ref="loadMoreRef" class="h-10"></div>
            <div v-for="message in chatStore.messages" :key="message.id" class="mb-3">
                <div v-if="message.sender_id === userStore.payload.id" class="bg-blue-300 max-w-[75%] w-fit px-3 rounded-lg ml-auto">
                    <p class="whitespace-pre-wrap break-words">{{ message.text }}</p>
                </div>
                <div v-else class="bg-gray-300 max-w-[75%] w-fit px-3 rounded-lg mr-auto">
                    <p class="whitespace-pre-wrap break-words">{{ message.text }}</p>
                </div>
            </div>
        </div>
        <div class="btns flex mx-auto mt-3">
            <div class="textarea ml-2">
                <textarea @input="autoResize" v-model="newMessageText" maxlength="1000" rows="1" cols="60" class="w-full flex-1 p-2 border border-gray-300 rounded-lg bg-gray-100 resize-none focus:outline-none text-base" placeholder="Send message"></textarea>
            </div>
            <div class="btn-send mt-2 ml-3" @click="CreateMessage(chatId)" :disabled="!newMessageText">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6 cursor-pointer mx-auto my-auto">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M6 12 3.269 3.125A59.769 59.769 0 0 1 21.485 12 59.768 59.768 0 0 1 3.27 20.875L5.999 12Zm0 0h7.5" />
                </svg>
            </div>
        </div>
    </div>
</template>

<style scoped>

</style>