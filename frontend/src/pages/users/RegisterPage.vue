<script setup>
import MyButton from '@/components/UI/MyButton.vue';
import { vClickOutside } from '@/directives/VClickOutside';
import router from '@/router/router';
import { useUserStore } from '@/stores/user';
import { ref } from 'vue';

const userStore = useUserStore()

const login = ref(null)
const password = ref(null)
const gender = ref(null)
const country = ref(null)

const isOpenGender = ref(false)
const isOpenDay = ref(false)
const isOpenMonth = ref(false)
const isOpenYear = ref(false)

const selectedGender = ref(null)
const selectedDay = ref(null)
const selectedMonth = ref(null)
const selectedYear = ref(null)

const currentYear = new Date().getFullYear()
const years = Array.from({ length: 80 }, (_, i) => currentYear - i)
const days = Array.from({length: 31}, (_, i) => i+1)
const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
const genders = ['Male', 'Female']

function selectGender(gender) {
    selectedGender.value = gender
    isOpenGender.value = false
}

function selectDay(day) {
    selectedDay.value = day
    isOpenDay.value = false
}

function selectMonth(month) {
    selectedMonth.value = month
    isOpenMonth.value = false
}


function selectYear(year) {
    selectedYear.value = year
    isOpenYear.value = false
}



const registerUser = async () => {
    if (!login.value || !password.value || !selectedGender.value || !selectedDay.value || !selectedMonth.value || !selectedYear.value || !country.value) {
        alert("Please fill in all required fields")
        return
    }

    const dayStr = selectedDay.value < 10 ? `0${selectedDay.value}` : selectedDay.value
    const monthMap = {
        January: "01", February: "02", March: "03", April: "04",
        May: "05", June: "06", July: "07", August: "08",
        September: "09", October: "10", November: "11", December: "12"
    }
    const monthStr = monthMap[selectedMonth.value]
    const birthday = `${dayStr}-${monthStr}-${selectedYear.value}`

    await userStore.storeUser(login.value, password.value, selectedGender.value === "Male" ? 1 : 0, birthday, country.value)

    if (userStore.payload.id){
            router.push(`/user/${userStore.payload.id}`)
        }
}

</script>

<template>
    <div class="register-field max-w-xl mx-auto">
        <div class="register mt-10 bg-white rounded-lg pt-5 pb-1 px-5">
            <div class="register-span w-full border-b border-gray-300 text-gray-700 text-xl pb-3 flex">
                <span class="mx-auto">Register</span>
            </div>
            <div class="register-form mt-3" @submit.prevent="registerUser">
                <form @submit.prevent="loginUser" action="/login" method="post" class="flex flex-col w-full p-3">
                    <div class="flex flex-col mb-4">
                        <span>Username*</span>
                        <input v-model="login" type="text" name="login" placeholder="Username" minlength="5" maxlength="15" class="px-3 py-2 border border-gray-300 rounded-lg bg-gray-50 focus:border-gray-500 focus:outline-none text-base">
                        <span class="mt-1 text-sm text-gray-500">Username should be at least 5 characters</span>
                    </div>
                    <div class="flex flex-col mb-4">
                        <span>Password*</span>
                        <input v-model="password" type="password" name="password" placeholder="Password" minlength="5" maxlength="15" class="px-3 py-2 border border-gray-300 rounded-lg bg-gray-50 focus:border-gray-500 focus:outline-none text-base">
                        <span class="mt-1 text-sm text-gray-500">Password should be at least 5 characters</span>
                    </div>
                    <div class="flex flex-col mb-4">
                        <span>Gender*</span>
                        <div class="gender relative w-64" v-click-outside="() => isOpenGender=false">
                            <button type="button" @click="isOpenGender = !isOpenGender" :class="[selectedGender ? 'text-black' : 'text-gray-500', isOpenGender ? 'focus:border-gray-500' : '']" class="w-full px-3 py-2 text-left border border-gray-300 rounded-lg bg-gray-50 text-base">
                                {{ selectedGender ?? 'Gender' }}
                            </button>
                            <ul v-if="isOpenGender" class="absolute z-10 mt-1 w-full bg-white border rounded max-h-48 overflow-y-auto shadow-lg">
                                <li v-for="gender in genders" :key="gender" @click="selectGender(gender)" class="px-3 py-2 cursor-pointer hover:bg-gray-200">
                                    {{ gender }}
                                </li>
                            </ul>
                        </div>
                    </div>
                    <div class="flex flex-col mb-4">
                        <span>Birthday*</span>
                        <div class="flex gap-2">
                            <div class="day relative w-64" v-click-outside="() => isOpenDay=false">
                                <button type="button" @click="isOpenDay = !isOpenDay" :class="[selectedDay ? 'text-black' : 'text-gray-500', isOpenDay ? 'focus:border-gray-500' : '']" class="w-full px-3 py-2 text-left border border-gray-300 rounded-lg bg-gray-50 text-base">
                                    {{ selectedDay ?? 'Day' }}
                                </button>
                                <ul v-if="isOpenDay" class="absolute z-10 mt-1 w-full bg-white border rounded max-h-48 overflow-y-auto shadow-lg">
                                    <li v-for="day in days" :key="day" @click="selectDay(day)" class="px-3 py-2 cursor-pointer hover:bg-gray-200">
                                        {{ day }}
                                    </li>
                                </ul>
                            </div>
                            <div class="month relative w-64" v-click-outside="() => isOpenMonth=false">
                                <button type="button" @click="isOpenMonth = !isOpenMonth" :class="[selectedMonth ? 'text-black' : 'text-gray-500', isOpenMonth ? 'focus:border-gray-500' : '']" class="w-full px-3 py-2 text-left border border-gray-300 rounded-lg bg-gray-50 text-base">
                                    {{ selectedMonth ?? 'Month' }}
                                </button>
                                <ul v-if="isOpenMonth" class="absolute z-10 mt-1 w-full bg-white border rounded max-h-48 overflow-y-auto shadow-lg">
                                    <li v-for="month in months" :key="month" @click="selectMonth(month)" class="px-3 py-2 cursor-pointer hover:bg-gray-200">
                                        {{ month }}
                                    </li>
                                </ul>
                            </div>
                            <div class="year relative w-64" v-click-outside="() => isOpenYear=false">
                                <button type="button" @click="isOpenYear = !isOpenYear" :class="[selectedYear ? 'text-black' : 'text-gray-500', isOpenYear ? 'focus:border-gray-500' : '']" class="w-full px-3 py-2 text-left border border-gray-300 rounded-lg bg-gray-50 text-base">
                                    {{ selectedYear ?? 'Year' }}
                                </button>
                                <ul v-if="isOpenYear" class="absolute z-10 mt-1 w-full bg-white border rounded max-h-48 overflow-y-auto shadow-lg">
                                    <li v-for="year in years" :key="year" @click="selectYear(year)" class="px-3 py-2 cursor-pointer hover:bg-gray-200">
                                        {{ year }}
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    <div class="flex flex-col mb-4">
                        <span>Country*</span>
                        <input v-model="country" type="text" name="country" placeholder="Country" minlength="1" maxlength="20" class="px-3 py-2 border border-gray-300 rounded-lg bg-gray-50 focus:border-gray-500 focus:outline-none text-base">
                    </div>
                    <MyButton class="bg-green-700 text-white hover:bg-green-800">Register</MyButton>
                </form>
            </div>
            <div class="login-link text-gray-500 flex mb-3">
                <router-link :to="{name: 'login.index'}" class="mx-auto">
                    <span>Already have an account? Log in</span>
                </router-link>  
            </div>
            
        </div>
    </div>
</template>

<style scoped>

</style>
