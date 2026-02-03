<script setup>
import { usePostStore } from '@/stores/post';
import { useUserStore } from '@/stores/user';
import { formatDate } from '@/utils/formatDate';
import { formatTimeAgo } from '@/utils/formatTimeAgo';
import { ref, watch } from 'vue';

const postStore = usePostStore()
const userStore = useUserStore()

const newCommentText = ref({})
const commentArea = ref(null);
const limit = 3

const isLikedByUser = (post) => {
    if (!userStore.payload) return false

    return post.likes.some(
        like => like.user_id === userStore.payload.id
    )
}

const CreateComment = async (postId) => {
    if (!newCommentText.value[postId]) return 

    await postStore.storeComment(postId, newCommentText.value[postId])
    newCommentText.value[postId] = ""
}

const autoResize = (event) => {
  const textarea = event.target;
  textarea.style.height = "auto";
  textarea.style.height = (textarea.scrollHeight + 2) + "px";
}

</script>

<template>
<div v-for="post in postStore.posts" :key="post.id">
    <div class="post bg-white rounded-lg max-w-2xl w-full pt-5 pb-1 px-5 text-lg mb-2">
        <div class="post-header flex pb-3">
            <router-link :to="{name: 'users.index', params: { id: post.author_id } }" class="photo">
                <img :src="`http://localhost:8000/api/users/${post.author_id}/avatar?v=${userStore.avatarVersion}`" class="border border-white w-13 h-13 rounded-full object-cover">
            </router-link>
            <div class="author pt-3 pl-3 text-lg">
                <router-link :to="{name: 'users.index', params: { id: post.author_id } }" >{{ post.author.login }}</router-link>
            </div>
            <div v-if="userStore.isAuth && (userStore.user.id === userStore.payload.id || post.author_id === userStore.payload.id)" @click="postStore.deletePost(post.id)" class="btn-delete pt-3 ml-auto">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-5 text-red-700 cursor-pointer">
                    <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                </svg>
            </div>
        </div>
        <div class="post-content pb-5 whitespace-pre-wrap break-words">
            <p>{{ post.text }}</p>
        </div>
        <div class="post-bottom flex text-gray-700 text-base">
            <div class="btn-like flex" @click="isLikedByUser(post)?postStore.unlikePost(post.id) : postStore.likePost(post.id)">
                <svg xmlns="http://www.w3.org/2000/svg" :fill="isLikedByUser(post)?'black' : 'none'" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6 cursor-pointer">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12Z" />
                </svg>
                <span class="ml-1">{{ post.likes.length }}</span>
            </div>
            <div class="btn-comment ml-10 flex">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6 cursor-pointer">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M8.625 12a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H8.25m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H12m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 0 1-2.555-.337A5.972 5.972 0 0 1 5.41 20.97a5.969 5.969 0 0 1-.474-.065 4.48 4.48 0 0 0 .978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25Z" />
                </svg>
                <span class="ml-1">{{ post.comments_count }}</span>  
            </div>
            <div class="time ml-auto">
                <span>{{ formatTimeAgo(post.date_created) }}</span>
            </div>
        </div>
        <div :class="[post.comments.length>0?'border-t border-gray-300':'', post.newComments.length>0?'border-t border-gray-300':'', userStore.isAuth?'border-t border-gray-300':'']" class="comments-box pt-4 mt-2 px-6">
            <div v-for="comment in [...(post.comments || []), ...(post.newComments || [])]" class="post-comments mb-3">
                <div class="comment flex">
                    <div class="comment-image min-w-10">
                        <img :src="`http://localhost:8000/api/users/${comment.author_id}/avatar?v=${userStore.avatarVersion}`" class="border border-white w-10 h-10 rounded-full object-cover">
                    </div>
                    <div class="comment-body flex-1 pl-2 text-base">
                        <div class="comment-author pt-1">
                            <span>{{ comment.author.login }}</span>
                        </div>
                        <div class="comment-content flex">
                            <div class="comment-text pt-1 wrap-anywhere">
                                <span>{{ comment.text }}</span>
                            </div>
                            <div class="ml-auto my-auto" v-if="comment.author_id === userStore.payload.id" @click="postStore.deleteComment(post.id, comment.id)">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-5 text-red-700 cursor-pointer">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                                </svg>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="btn-see-more text-base text-gray-700 mb-3" v-if="(post.comments.length + post.newComments.length) != post.comments_count">
                <span @click="postStore.getComments(post.id, limit)" class="cursor-pointer">See more comments</span>
            </div>
            <div v-if="userStore.isAuth" class="comment-create flex">
                <div class="image shrink-0 ">
                    <img :src="`http://localhost:8000/api/users/${userStore.payload.id}/avatar?v=${userStore.avatarVersion}`" class="border border-white w-10 h-10 rounded-full object-cover">
                </div>
                <div class="textarea mx-2">
                    <textarea @input="autoResize" v-model="newCommentText[post.id]" maxlength="150" rows="1" cols="60" class="w-full flex-1 p-2 border border-gray-300 rounded-lg bg-gray-100 resize-none focus:outline-none text-base" placeholder="Add comment"></textarea>
                </div>
                <div class="btn-send ml-auto mt-2" @click="CreateComment(post.id)">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6 cursor-pointer">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M6 12 3.269 3.125A59.769 59.769 0 0 1 21.485 12 59.768 59.768 0 0 1 3.27 20.875L5.999 12Zm0 0h7.5" />
                    </svg>
                </div>
            </div>
        </div>
    </div>
</div>

</template>

<style>
    
</style>