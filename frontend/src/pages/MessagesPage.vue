<script setup>
import { useChatStore } from '@/stores/chat';
import { useUserStore } from '@/stores/user';
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';


onMounted(async () => {
    chatStore.$reset()
    await chatStore.getChats()
})


const userStore = useUserStore()
const chatStore = useChatStore()

const router = useRouter()

const goToUser = (chat) => {
    const other = getOtherMember(chat)
    if (!other) return

    router.push({
        name: 'users.index',
        params: { id: other.user_id }
    })
}

const goToChat = (chat) => {
    if (!chat) return

    router.push({
        name: 'messages.chat.index',
        params: { id: chat.id }
    })
}

const getOtherMember = (chat) => {
    return chat.members?.find(m => m.user_id !== userStore.payload?.id)
}

const deleteChat = async (chat) => {
    await chatStore.deleteChat(chat.id)
}

</script>

<template>
    <div class="messages mt-4 bg-white rounded-lg max-w-2xl w-full pt-5 pb-1 px-5 text-lg mb-2">
        <div class="btns flex pb-2 border-b border-gray-300 text-gray-700">
            <span>Chats </span>
        </div>
        <div class="messages">
            <div @click="goToChat(chat)" v-for="chat in chatStore.chats" :key="chat.id" class="flex-1 px-3 py-2 my-3 rounded-xl bg-gray-200 hover:bg-gray-300">
                <div v-if="(other = getOtherMember(chat))" class="flex">
                    <div class="w-15 h-15">
                        <button @click.stop="goToUser(chat)" class="image">
                            <img :src="`http://localhost:8000/api/users/${other.user_id}/avatar?v=${userStore.avatarVersion}`" class="cursor-pointer border border-white w-15 h-15 rounded-full object-cover">
                        </button>
                    </div>
                    <div class="ml-3 my-auto w-[60%] flex-shrink min-w-0">
                        <div>
                            <button @click.stop="goToUser(chat)" class="cursor-pointer">
                                {{ other.user.login }}
                            </button>
                        </div>
                        <div class="last message text-base text-gray-500 truncate">
                            <span>{{ chat.last_message }}</span>
                        </div>
                    </div>
                    <div class="btns ml-auto my-auto">
                        <button @click.stop="deleteChat(chat)" class="ml-3 bg-red-800 hover:bg-red-900 cursor-pointer py-2 px-4 text-base rounded-lg text-white">Delete chat</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>

</style>