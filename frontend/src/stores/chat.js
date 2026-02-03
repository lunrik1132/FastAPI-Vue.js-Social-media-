import { defineStore } from 'pinia'
import axios from 'axios';
import { useUserStore } from './user';
import { api } from '@/api';

export const useChatStore = defineStore('chats', {
    state: () => ({
        chats: [],
        messages: [],
        total_messages: 0,
        limit: 12,
        message_limit: 24,
        offset: 0,
        loading: false,
        hasMore: true,
        ws: null
    }),
    getters: {
    },

    actions: {
        async getChats() {
            if (this.loading || !this.hasMore) return

            this.loading = true

            try {
                const res = await api.get(`/api/chats`, {
                    params: {
                        limit: this.limit,
                        offset: this.offset
                    }
                })
                if (!res.data.chats.length) {
                    this.hasMore = false
                } else {
                    this.chats.push(...res.data.chats)
                    this.offset += res.data.chats.length
                }
            } catch (e) {
                console.error("Loading chats error: ", e)
            } finally {
                this.loading = false
            }
        },
        async getChat(chatId) {
            try {
                const res = await api.get(`/api/chats/${chatId}`)
                return res.data
            } catch (e) {
                console.error("Loading chat error: ", e)
            }
        },
        async storeChat(userId){
            try {
                const res = await api.post(`/api/chats`, {
                    user_ids: [userId]
                })
                return res.data.id
            } catch (e) {
                console.error("Create chat error: ", e)
            }
        },
        async deleteChat(chatId){
            try{
                const res = await api.delete(`/api/chats/${chatId}`)
                this.chats = this.chats.filter(chat => chat.id != chatId)
                this.offset -= 1

            } catch(e) {
                console.error("Delete chat error: ", e)
            }
        },
        async getMessages(chatId){
            if (this.loading || !this.hasMore) return

            this.loading = true

            try {
                const res = await api.get(`/api/chats/messages/${chatId}`, {
                    params: {
                        limit: this.message_limit,
                        offset: this.offset
                    }
                })

                if (!res.data.messages.length) {
                    this.hasMore = false
                } else {
                    this.messages.unshift(...res.data.messages)
                    this.total_messages = res.data.total
                    this.offset += res.data.messages.length
                }
            } catch (e) {
                console.error("Loading messages error: ", e)
            } finally {
                this.loading = false
            }
        },
        async storeMessage(chatId, text){
            try {
                const res = await api.post(`/api/chats/messages/${chatId}`, {
                    text: text
                })
                
            } catch (e) {
                console.error("Create message error: ", e)
            }
        },
    },
})