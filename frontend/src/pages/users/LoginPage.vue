<script setup>
import MyButton from '@/components/UI/MyButton.vue';
import router from '@/router/router';
import { useUserStore } from '@/stores/user';
import { ref } from 'vue';

const userStore = useUserStore()

const login = ref('')
const password = ref('')

const loginUser = async () => {
    try {
        if (!login.value || !password.value) {
            alert("Please fill in all required fields")
            return
        }
        await userStore.loginUser(login.value, password.value)

        if (userStore.payload.id){
            router.push(`/user/${userStore.payload.id}`)
        }
    } catch (e) {
        console.error("Login error: ", e)
    }
}

</script>

<template>
    <div class="login-field max-w-xl mx-auto">
        <div class="login mt-10 bg-white rounded-lg pt-5 pb-1 px-5">
            <div class="login-span w-full border-b border-gray-300 text-gray-700 text-xl pb-3 flex">
                <span class="mx-auto">Log in</span>
            </div>
            <div class="login-form mt-3">
                <form @submit.prevent="loginUser" class="flex flex-col w-full p-3">
                    <div class="flex flex-col mb-1">
                        <span>Username:</span>
                        <input v-model="login" type="text" name="login" minlength="5" maxlength="15" class="mb-3 px-3 py-2 border border-gray-300 rounded-lg bg-gray-50 focus:border-gray-500 focus:outline-none text-base">
                    </div>
                    <div class="flex flex-col mb-1">
                        <span>Password:</span>
                        <input v-model="password" type="password" name="password" minlength="5" maxlength="15" class="mb-3 px-3 py-2 border border-gray-300 rounded-lg bg-gray-50 focus:border-gray-500 focus:outline-none text-base">
                    </div>
                    <MyButton class="bg-green-700 text-white hover:bg-green-800">Log in</MyButton>
                </form>
            </div>
            <div class="register-link text-gray-500 flex mb-3">
                <router-link :to="{name: 'register.index'}" class="mx-auto">
                    <span>Do not have an account? Register</span>
                </router-link>
            </div>
            
        </div>
    </div>
</template>

<style scoped>

</style>