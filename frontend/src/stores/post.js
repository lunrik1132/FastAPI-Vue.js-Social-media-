import { defineStore } from 'pinia'
import axios from 'axios';
import { useUserStore } from './user';
import { api } from '@/api';
import { apiUrl } from '@/main';
export const usePostStore = defineStore('posts', {
    state: () => ({
        posts: [],
        // post: {author: {},
        //        destination: {}},
        limit: 3,
        offset: 0,
        loading: false,
        hasMore: true,
    }),

    getters: {
        //postText: (state) => state.post.text,
    },

    actions: {
        reset() {
            this.posts = []
            this.offset = 0
            this.hasMore = true
            this.loading = false
        },
        async getPosts(userId) {
            if (this.loading || !this.hasMore) return

            this.loading = true

            try {
                const res = await axios.get(`${apiUrl}/api/posts/user/destination/${userId}`, {
                    params: {
                        limit: this.limit,
                        offset: this.offset
                    }
                })
               
                if (!res.data.posts.length) {
                    this.hasMore = false
                } else {
                    this.posts.push(...res.data.posts)
                    this.offset += res.data.posts.length
                }

                for (const post of res.data.posts) {
                    post.comments = []
                    post.commentsOffset = 0
                    post.newComments = []
                    this.getComments(post.id, 1)
                }

            } catch (e) {
                console.error("Loading posts error: ", e)
            } finally {
                this.loading = false
            }
        },
        async getAllPosts() {
            if (this.loading || !this.hasMore) return

            this.loading = true

            try {
                const res = await axios.get(`${apiUrl}/api/posts`, {
                    params: {
                        limit: 10,
                        offset: this.offset
                    }
                })
               
                if (!res.data.posts.length) {
                    this.hasMore = false
                } else {
                    this.posts.push(...res.data.posts)
                    this.offset += res.data.posts.length
                }

                for (const post of res.data.posts) {
                    post.comments = []
                    post.commentsOffset = 0
                    post.newComments = []
                    this.getComments(post.id, 1)
                }

            } catch (e) {
                console.error("Loading posts error: ", e)
            } finally {
                this.loading = false
            }
        },
        async storePost(destinationId, text){
            try {
                const res = await api.post(`/api/posts`, {
                    destination_id: destinationId,
                    text: text,
                })
                
                const newPost = {
                    ...res.data.new_post,
                    comments: [],         
                    commentsOffset: 0,   
                    newComments: [],
                }

                this.posts.unshift(newPost)
                this.offset += 1

            } catch (e) {
                console.error("Create post error: ", e)
            }
        },
        async deletePost(postId){
            try{
                const res = await api.delete(`/api/posts/${postId}`)
                this.posts = this.posts.filter(post => post.id != postId)
                this.offset -= 1

            } catch(e) {
                console.error("Delete post error: ", e)
            }
        },
        likePost(postId){
            const userStore = useUserStore()
            if (!userStore.isAuth){
                return
            }
            try {
                const res = api.post(`/api/posts/${postId}/likes`, null)

                const post = this.posts.find(p => p.id === postId)
                post.likes.push({ user_id: userStore.payload.id })
                
            } catch(e) {
                console.error("Like post error: ", e)
            }
        },

        unlikePost(postId){
            const userStore = useUserStore()
            try {
                const res = api.delete(`/api/posts/${postId}/likes`, null)

                const post = this.posts.find(p => p.id === postId)
                post.likes = post.likes.filter(like => like.user_id !== userStore.payload.id)
            
            } catch(e) {
                console.error("unLike post error: ", e)
            }
        },
        async getComments(postId, limit) {
            try {
                const post = this.posts.find(p => p.id === postId)

                const res = await axios.get(`${apiUrl}/api/posts/${postId}/comments`, {
                    params: {
                        limit: limit,
                        offset: post.commentsOffset
                    }
                })
            
                post.comments.push(...res.data.comments)
                post.commentsOffset += res.data.comments.length
                
                if (post.newComments){
                    if (post.comments.length > (post.comments_count - post.newComments.length)) {
                        for (let i = 0; i < post.comments_count - post.newComments.length; i++) {
                            post.newComments.shift()
                        }
                    }
                }
                

            } catch (e) {
                console.error("Loading comments error: ", e)
            }
        },

        async storeComment(postId, text){
            const userStore = useUserStore()
            try {
                const res = await api.post(`/api/posts/${postId}/comments`, {
                    text: text
                })
                
                const post = this.posts.find(p => p.id === postId)

                post.newComments = post.newComments || []
                post.newComments.push({
                    id: res.data.new_comment.id,
                    author_id: userStore.payload.id,
                    text: text,
                    author: { login: res.data.new_comment.author.login }
                })
                post.comments_count += 1
                
            } catch (e) {
                console.error("Comment store error: ", e)
            }
        },
        async deleteComment(postId, commentId){
            try{
                const res = await api.delete(`/api/posts/${postId}/comments/${commentId}`)

                const post = this.posts.find(p => p.id === postId)
                post.comments = post.comments.filter(comment => comment.id != commentId)
                post.newComments = post.newComments.filter(comment => comment.id != commentId)
                post.comments_count -= 1
                post.commentsOffset -= 1
            } catch(e) {
                console.error("Delete comment error: ", e)
            }
        },
    },
})