import { defineStore } from 'pinia'
import axios from 'axios';
import { api } from '@/api';
import { apiUrl } from '@/main';
const getPayload = () => {
    const token = localStorage.getItem('access_token');
    if (!token) return {};
    try {
        return JSON.parse(atob(token.split('.')[1]));
    } catch (e) {
        return {};
    }
};

export const useUserStore = defineStore('users', {
    state: () => ({
        payload: getPayload(),
        user: {},
        friend_accepted_offset: 0,
        friend_pending_offset: 0,
        friend_hasMore_accepted: true,
        friend_hasMore_pending: true,
        loading: false,
        friends_accepted: {
            total: 0,
            friends: []
        },
        friends_pending: {
            total: 0,
            friends: []
        },
        isAuth: !!localStorage.getItem('access_token'),
        // bgImage_default: '${apiUrl}/static/images/default_bgimage.jpg',
        // avatar_default: '${apiUrl}/static/images/default_image.jpg',
        avatarVersion: 0,
        bgVersion: 0,
    }),

    getters: {
        gender: (state) => state.user.gender===1?"Male":"Female",
        avatar: (state) => {
            if (!state.user?.id) {
                return ''
            }
            return `${apiUrl}/api/users/${state.user.id}/avatar?v=${state.avatarVersion}`
        },
        bgImage: (state) => {
            if (!state.user?.id) {
                return ''
            }
            return `${apiUrl}/api/users/${state.user.id}/bgimage?v=${state.bgVersion}`
        },
    },

    actions: {
        async getUser(userId){
            const res = await axios.get(`${apiUrl}/api/users/id/${userId}`)
            
            this.user = res.data

        },
        async getUsersByLogin(login){
            const res = await axios.get(`${apiUrl}/api/users/search`, {
                params: {
                    query: login
                }
            })
            return res
        },
        async checkFriendship(userId){
            const res = await api.get(`/api/users/friends/status/${userId}`)
            return res.data
        },
        async getFriends(userId, limit){
            if (this.loading || !this.friend_hasMore_accepted) return

            this.loading = true

            try {
                const res = await axios.get(`${apiUrl}/api/users/friends/accepted/${userId}`, {
                    params: {
                        limit: limit,
                        offset: this.friend_accepted_offset
                    }
                })
                if (!res.data.friends.length) {
                    this.friend_hasMore_accepted = false
                } else {
                    this.friends_accepted.friends.push(...res.data.friends)
                    this.friends_accepted.total = res.data.total
                    this.friend_accepted_offset += res.data.friends.length
                }
            } catch (e) {
                console.error("Loading accepted friends error: ", e)
            } finally {
                this.loading = false
            }
        },
        async getFriendsRequests(limit){
            if (this.loading || !this.friend_hasMore_pending) return

            this.loading = true

            try {
                const res = await api.get(`/api/users/friends/pending`, {
                    params: {
                        limit: limit,
                        offset: this.friend_pending_offset
                    }
                })
                if (!res.data.friends.length) {
                    this.friend_hasMore_pending = false
                } else {
                    this.friends_pending.friends.push(...res.data.friends)
                    this.friends_pending.total = res.data.total
                    this.friend_pending_offset += res.data.friends.length
                }
            } catch (e) {
                console.error("Loading pending friends error: ", e)
            } finally {
                this.loading = false
            }
        },
        async sendFriendRequest(userId){
            try {
                const res = await api.post(`/api/users/friends/requests/send`, {
                    addressee_id: userId
                })
            } catch(e) {
                console.error("Send friend request error: ", e)
            }
        },
        async rejectFriendRequest(requesterId){
            try {
                const res = await api.delete(`/api/users/friends/requests/reject/${requesterId}`)
            } catch(e) {
                console.error("Reject friend request error: ", e)
            }
        },
        async deleteFriend(friendshipId){
            try {
                const res = await api.delete(`/api/users/friends/accepted/${friendshipId}`)
            } catch(e) {
                console.error("Delete friendship error: ", e)
            }
        },
        async storeUser(login, password, gender, birthday, country){
            try{
                const res = await axios.post(`${apiUrl}/api/users`, {
                    login: login,
                    password: password,
                    gender: gender,
                    birthday: birthday,
                    country: country
                })

                await this.loginUser(login, password)
            } catch(e) {
                console.error("Register user error: ", e)
            }


        },
        async loginUser(login, password){
            try {
                const res = await axios.post('${apiUrl}/api/jwt/login',
                {
                    login: login,
                    password: password
                })

                const { access_token, refresh_token } = res.data

                localStorage.setItem('access_token', access_token)
                localStorage.setItem('refresh_token', refresh_token)

                this.payload = JSON.parse(atob(access_token.split('.')[1]))
                this.isAuth = true

            } catch (e) {
                this.isAuth = false
                alert("Wrong login or password")
                throw e
            }
        },
        checkAuth() {
            const token = localStorage.getItem('access_token')
            this.isAuth = !!token
        },

        logoutUser() {
            localStorage.clear()
            this.isAuth = false
            this.payload = {}

        },

        async updateLogin(login){
            try {
                const res = await api.patch(`/api/users/login`, {
                    new_login: login
                })

                this.user.login = login
            } catch (e) {
                console.error("Update login error: ", e)
                throw e
            }
        },
        async updatePassword(oldPassword, newPassword){
            try {
                const res = await api.patch(`/api/users/password`, {
                    old_password: oldPassword,
                    new_password: newPassword
                })

            } catch (e) {
                console.error("Update password error: ", e)
                throw e
            }
        },
        async updateDescription(text){
            try {
                const res = await api.patch(`/api/users/description`, {
                    new_description: text
                })

                this.user.desctiption = text

                this.getUser(this.user.id)

            } catch (e) {
                console.error("Update description error: ", e)
            }
        },
        async updateGender(gender){
            try {
                const res = await api.patch(`/api/users/gender`, {
                    new_gender: gender
                })

                this.user.gender = gender
            } catch (e) {
                console.error("Update gender error: ", e)
            }
        },
        async updateBirthday(birthday){
            try {
                const res = await api.patch(`/api/users/birthday`, {
                    new_birthday: birthday
                })
                
                this.user.birthday = birthday

            } catch (e) {
                console.error("Update birthday error: ", e)
            }
        },
        async updateCountry(country){
            try {
                const res = await api.patch(`/api/users/country`, {
                    new_country: country
                })

                this.user.country = country

            } catch (e) {
                console.error("Update country error: ", e)
            }
        },
        async uploadAvatar(file) {
            try {
                const formData = new FormData()
                formData.append('file', file)

                await api.post('/api/users/avatar', formData, {
                    headers: {
                    'Content-Type': 'multipart/form-data',
                    },
                })
                this.avatarVersion++

            } catch (e) {
                console.error('Upload avatar error:', e)
                throw e
            }
        },
        async uploadBackground(file) {
            try {
                const formData = new FormData()
                formData.append('file', file)

                await api.post('/api/users/bgimage', formData, {
                    headers: {
                    'Content-Type': 'multipart/form-data',
                    },
                })
                this.bgVersion++

            } catch (e) {
                console.error('Upload background error:', e)
                throw e
            }
        },
    },
})