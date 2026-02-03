import { defineStore } from 'pinia'
import axios from 'axios';
import { useUserStore } from './user';
import { useChatStore } from './chat';
import { api } from '@/api';

export const useWebsocketStore = defineStore('websockets', {
    state: () => ({
        ws: null,
    }),
    getters: {
    },

    actions: {
        connect(chatId){

            const chatStore = useChatStore()
            this.disconnect()
            

            const token = localStorage.getItem("access_token")
            const url = `ws://localhost:8000/api/ws/chat/${chatId}?token=${token}`

            this.ws = new WebSocket(url)

           this.ws.onopen = () => {
                console.log('WS connected to chat', chatId)
            }

           this.ws.onmessage = (e) => {
                const data = JSON.parse(e.data)
                chatStore.messages.push(data)
            }

            this.ws.onclose = () => {
                console.log('WS closed')
            }

            this.ws.onerror = (e) => {
                console.error('WS error', e)
            }
        },
        disconnect() {
            if (this.ws) {
                this.ws.close()
            }
        },
        sendMessage(text){
        if (!this.ws) {
            console.log('WS is null')
            return
        }

        console.log('WS readyState:', this.ws.readyState)
        if (!this.ws || this.ws.readyState !== WebSocket.OPEN) return

        this.ws.send(text)
        },
    },
})