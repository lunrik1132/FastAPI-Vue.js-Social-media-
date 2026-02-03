<script setup>
import MyButton from '@/components/UI/MyButton.vue';
import { vClickOutside } from '@/directives/VClickOutside';
import { useUserStore } from '@/stores/user';
import { onMounted, ref } from 'vue';


onMounted(async () => {
    await userStore.getUser(userStore.payload.id)

    login.value = userStore.user.login
    description.value = userStore.user.description
    gender.value = userStore.user.gender===1?'Male':'Female'
    birthday.value = userStore.user.birthday.split('-').map(Number)
    selectedDay.value = birthday.value[2]
    selectedMonth.value = months[birthday.value[1]-1]
    selectedYear.value = birthday.value[0]
    country.value = userStore.user.country
})

const userStore = useUserStore()

const isLoginError = ref(false)
const isPasswordError = ref(false)

const login = ref(null)
const description = ref(null)
const gender = ref(null)
const country = ref(null)

const birthday = ref(null)
const selectedDay = ref(null)
const selectedMonth = ref(null)
const selectedYear = ref(null)

const oldPassword = ref(null)
const newPassword = ref(null)

const isOpenGender = ref(false)
const isOpenDay = ref(false)
const isOpenMonth = ref(false)
const isOpenYear = ref(false)

const currentYear = new Date().getFullYear()
const years = Array.from({ length: 80 }, (_, i) => currentYear - i)
const days = Array.from({length: 31}, (_, i) => i+1)
const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
const genders = ['Male', 'Female']

function selectGender(genderName) {
    gender.value = genderName
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

const confirmChanges = async () => {
    if (login.value != userStore.user.login){
        try {
            await userStore.updateLogin(login.value)
            isLoginError.value = false
        } catch (e) {
            isLoginError.value = e.response.status
        }
    }

    if (oldPassword.value && newPassword.value){
        try {
            await userStore.updatePassword(oldPassword.value, newPassword.value)
            isPasswordError.value = false
        } catch(e) {
            console.log(e.response.status)
            isPasswordError.value = e.response.status
        }
    }

    if (description.value != userStore.user.description){
        await userStore.updateDescription(description.value)
    }

    if (!((gender.value=='Male'?1:0) === userStore.user.gender)){
        await userStore.updateGender(gender.value==='Male'?1:0)
    }

    if (selectedDay.value != birthday.value[2] || selectedMonth.value != months[birthday.value[1]-1] || selectedYear.value != birthday.value[0]){
        const dayStr = selectedDay.value < 10 ? `0${selectedDay.value}` : selectedDay.value
        const monthMap = {
            January: "01", February: "02", March: "03", April: "04",
            May: "05", June: "06", July: "07", August: "08",
            September: "09", October: "10", November: "11", December: "12"
        }
        const monthStr = monthMap[selectedMonth.value]
        const birthday_full = `${selectedYear.value}-${monthStr}-${dayStr}`

        await userStore.updateBirthday(birthday_full)
        birthday.value = userStore.user.birthday.split('-').map(Number)
    }

    if (country.value != userStore.user.country){
        await userStore.updateCountry(country.value)
    }
}

</script>

<template>
    <div class="settings max-w-2xl w-full my-4 bg-white rounded-lg py-3 px-7">
        <div class="text-lg border-b border-gray-300 text-gray-700">
            <span>Settings</span>
        </div>
        <div class="login flex mt-3 text-lg">
            <span class="pt-2 mr-3">Login:</span>
            <input v-model="login" type="text" name="login" minlength="5" maxlength="15" class="w-50 mb-3 px-3 py-2 border border-gray-300 rounded-lg bg-gray-50 focus:border-gray-500 focus:outline-none text-base">
            <span v-if="isLoginError===422" class="text-base text-red-800 ml-3 mt-2">Username should be from 5 to 15 characters</span>
            <span v-else-if="isLoginError===400" class="text-base text-red-800 ml-3 mt-2">This username is already taken</span>
        </div>
        <div class="password flex flex-col text-lg border-b border-gray-300 mb-3 pb-3">
            <div class="flex">
                <span class="pt-2 mr-3">Password:</span>
                <input v-model="oldPassword" placeholder="Old password" type="text" name="password" minlength="5" maxlength="15" class="w-50 px-3 py-2 border border-gray-300 rounded-lg bg-gray-50 focus:border-gray-500 focus:outline-none text-base">
                <input v-model="newPassword" placeholder="New password" type="text" name="password" minlength="5" maxlength="15" class="w-50 ml-3 px-3 py-2 border border-gray-300 rounded-lg bg-gray-50 focus:border-gray-500 focus:outline-none text-base">
            </div>
            <div v-if="isPasswordError" class="mx-auto">
                <span v-if="isPasswordError===422" class="text-base text-red-800">Password should be from 5 to 15 characters</span>
                <span v-else-if="isPasswordError===400" class="text-base text-red-800">Old password is wrong</span>
            </div>
        </div>
        <div class="description flex mt-3 text-lg">
            <span class="pt-2 mr-3">Description:</span>
            <textarea v-model="description" maxlength="100" class="w-full h-25 p-3 border border-gray-300 rounded-lg bg-gray-100 resize-none focus:outline-none" placeholder="Description"></textarea>
        </div>
        <div class="gender flex mt-3 text-lg">
            <span class="pt-2 mr-3">Gender:</span>
            <div class="gender relative w-64" v-click-outside="() => isOpenGender=false">
                <button type="button" @click="isOpenGender = !isOpenGender" :class="isOpenGender ? 'focus:border-gray-500' : ''" class="w-full px-3 py-2 text-left border border-gray-300 rounded-lg bg-gray-50 text-black text-base">
                    {{ gender }}
                </button>
                <ul v-if="isOpenGender" class="absolute z-10 mt-1 w-full bg-white border rounded max-h-48 overflow-y-auto shadow-lg">
                    <li v-for="gender in genders" :key="gender" @click="selectGender(gender)" class="px-3 py-2 cursor-pointer hover:bg-gray-200">
                        {{ gender }}
                    </li>
                </ul>
            </div>
        </div>
        <div class="birthday flex mt-3 text-lg">
            <span class="pt-2 mr-3">Birthday:</span>
            <div class="day relative w-64 mr-3" v-click-outside="() => isOpenDay=false">
                <button type="button" @click="isOpenDay = !isOpenDay" :class="[selectedDay ? 'text-black' : 'text-gray-500', isOpenDay ? 'focus:border-gray-500' : '']" class="w-full px-3 py-2 text-left border border-gray-300 rounded-lg bg-gray-50 text-base">
                    {{ selectedDay }}
                </button>
                <ul v-if="isOpenDay" class="absolute z-10 mt-1 w-full bg-white border rounded max-h-48 overflow-y-auto shadow-lg">
                    <li v-for="day in days" :key="day" @click="selectDay(day)" class="px-3 py-2 cursor-pointer hover:bg-gray-200">
                        {{ day }}
                    </li>
                </ul>
            </div>
            <div class="month relative w-64 mr-3" v-click-outside="() => isOpenMonth=false">
                <button type="button" @click="isOpenMonth = !isOpenMonth" :class="[selectedMonth ? 'text-black' : 'text-gray-500', isOpenMonth ? 'focus:border-gray-500' : '']" class="w-full px-3 py-2 text-left border border-gray-300 rounded-lg bg-gray-50 text-base">
                    {{ selectedMonth }}
                </button>
                <ul v-if="isOpenMonth" class="absolute z-10 mt-1 w-full bg-white border rounded max-h-48 overflow-y-auto shadow-lg">
                    <li v-for="month in months" :key="month" @click="selectMonth(month)" class="px-3 py-2 cursor-pointer hover:bg-gray-200">
                        {{ month }}
                    </li>
                </ul>
            </div>
            <div class="year relative w-64" v-click-outside="() => isOpenYear=false">
                <button type="button" @click="isOpenYear = !isOpenYear" :class="[selectedYear ? 'text-black' : 'text-gray-500', isOpenYear ? 'focus:border-gray-500' : '']" class="w-full px-3 py-2 text-left border border-gray-300 rounded-lg bg-gray-50 text-base">
                    {{ selectedYear }}
                </button>
                <ul v-if="isOpenYear" class="absolute z-10 mt-1 w-full bg-white border rounded max-h-48 overflow-y-auto shadow-lg">
                    <li v-for="year in years" :key="year" @click="selectYear(year)" class="px-3 py-2 cursor-pointer hover:bg-gray-200">
                        {{ year }}
                    </li>
                </ul>
            </div>
        </div>
        <div class="country flex mt-3 text-lg">
            <span class="pt-2 mr-3">Country:</span>
            <input v-model="country" type="text" name="country" placeholder="Country" minlength="1" maxlength="20" class="px-3 py-2 border border-gray-300 rounded-lg bg-gray-50 focus:border-gray-500 focus:outline-none text-base">
        </div>
        <div class="mt-3">
            <MyButton @click="confirmChanges" class="w-full bg-green-700 text-white hover:bg-green-800">Confirm changes</MyButton>
        </div>
    </div>
</template>

<style scoped>

</style>