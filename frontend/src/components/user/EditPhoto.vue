<script setup>
import { useUserStore } from '@/stores/user'
import { ref } from 'vue'

const emit = defineEmits(['close', 'changeAvatar', 'changeBackground'])

const userStore = useUserStore()

const active = ref('avatar')

const avatarInput = ref(null)
const bgInput = ref(null)

const avatarImage = ref(null)
const bgImage = ref(null)
const avatarFile = ref(null)
const bgFile = ref(null)

const selectAvatar = () => {
    avatarInput.value.click()
}

const selectBackground = () => {
    bgInput.value.click()
}

const onAvatarChange = (e) => {
    avatarFile.value = e.target.files[0]
    if (avatarFile) {
        avatarImage.value = URL.createObjectURL(avatarFile.value)
    }
}

const onBgChange = (e) => {
    bgFile.value = e.target.files[0]
    if (bgFile) {
        bgImage.value = URL.createObjectURL(bgFile.value)
    }
}

const confirmChanges = () => {
    if (active.value === 'avatar' && avatarFile.value) {
        emit('changeAvatar', avatarFile.value)
    } 
    else if (active.value === 'bgimage' && bgFile.value) {
        emit('changeBackground', bgFile.value)
    }
}


</script>

<template>
    <div class="fixed inset-0 bg-black/40 flex items-center justify-center z-50" @click="$emit('close')">
        <div class="bg-white rounded-xl p-6 max-w-3xl w-full relative" @click.stop>
            <span class="flex text-lg border-b border-gray-300 text-gray-700">
                Edit profile
            </span>
            
            <div class="btns flex mt-2">
                <button @click="active='avatar'" class="flex-1 mx-2 py-1 text-lg border border-gray-400 cursor-pointer hover:bg-gray-300" :class="active === 'avatar'?'bg-gray-200':''">Avatar</button>
                <button @click="active='bgimage'" class="flex-1 mx-2 py-1 text-lg border border-gray-400 cursor-pointer hover:bg-gray-300" :class="active === 'bgimage'?'bg-gray-200':''">Background image</button>
            </div>

            <div class="images my-8">
                <div v-if="active==='avatar'">
                    <img v-if="avatarImage" :src="avatarImage" alt="Avatar" class="mx-auto w-55 h-55 rounded-full object-cover">
                    <img v-else :src="userStore.avatar" class="mx-auto w-55 h-55 rounded-full object-cover">
                </div>
                <div v-else>
                    <img v-if="bgImage" :src="bgImage" alt="BgImage" class="mx-auto w-full h-55 object-cover">
                    <img v-else :src="userStore.bgImage" class="mx-auto w-full h-55 object-cover">
                </div>
            </div>

            <div class="btns mx-2">
                <button v-if="active==='avatar'" class="w-full mb-3 py-2 rounded-lg bg-gray-100 hover:bg-gray-200 cursor-pointer" @click="selectAvatar">
                    Change avatar
                </button>
    
                <button v-else class="w-full mb-3 py-2 rounded-lg bg-gray-100 hover:bg-gray-200 cursor-pointer" @click="selectBackground">
                    Change background image
                </button>

                <button class="w-full py-2 rounded-lg text-white bg-green-600 hover:bg-green-700 cursor-pointer" @click="confirmChanges">
                    Confirm
                </button>
            </div>


            <button class="absolute top-3 right-3 text-gray-400 hover:text-gray-600 cursor-pointer" @click="$emit('close')">
                ✕
            </button>

            <input
                ref="avatarInput"
                type="file"
                accept="image/*"
                class="hidden"
                @change="onAvatarChange"
            />

            <input
                ref="bgInput"
                type="file"
                accept="image/*"
                class="hidden"
                @change="onBgChange"
            />
        </div>
    </div>
</template>

<style scoped>

</style>