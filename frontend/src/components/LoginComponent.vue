<template>
    <div class="login-component">
        <h2>Вітаємо! Радий бачити тебе знову 👋</h2>
        <p v-if="error !== ''" class="error">{{error}}</p>
        <form @submit.prevent="authorization">
            <div>
                <label for="email">Email</label>
                <input type="email" id="email" v-model="email" required>
            </div>
            <div>
                <label for="password">Пароль</label>
                <input type="password" id="password" v-model="password" required>
            </div>
            <button type="submit">Увійти</button>
        </form>
        <p>Забули пароль? Натисніть тут</p>
        <p @click="$emit('registration')" class="allocated">Немає аккаунта? Зареєструватися</p>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'LoginComponent',
    data() {
        return {
            email: '',
            password: '',
            error:''
        }
    },
    methods: {
        async authorization() {
            this.error = '';
            try {
                const response = await axios.get(`https://mytodolist-pcw4.onrender.com/users/${this.email}`);
                const userData = response.data;

                if (userData.password !== this.password) {
                    this.error = 'Невірний пароль';
                    return;
                }
                this.$emit('authorization', userData);
            } catch (err) {
                if (err.response) {
                    if (err.response.status === 400 && err.response.data && err.response.data.detail === "Incorrect username") {
                        this.error = 'Користувача з таким email не знайдено';
                    } else {
                        this.error = `Помилка: ${err.response.data.detail || 'Не вдалося увійти. Спробуйте пізніше.'}`;
                    }
                } else if (err.request) {
                    this.error = 'Не вдалося підключитися до сервера. Перевірте ваше інтернет-з\'єднання.';
                } else {
                    this.error = 'Сталася помилка під час відправки запиту.';
                }
            }
        }
    }
}
</script>

<style scoped>
.login-component{
    background-color: #111;
    color: #fff;
    padding: 30px 10px;
    border-radius: 10px;
    margin: auto;
    width: clamp(100px, 80%, 700px);
    margin-top: 100px;
    text-align: center;
}

label{
    margin: 5px;
}

form div {
    text-align: left;
    margin: 20px 0 20px 10%;
}
</style>