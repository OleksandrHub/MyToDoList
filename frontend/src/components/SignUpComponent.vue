<template>
    <div class="signup-component">
        <h2>Приєднуйтесь до нашого TODO-додатку! 🚀</h2>
        <p v-if="error !== ''" class="error">{{error}}</p>
        <form @submit.prevent="registration">
            <div>
                <label for="name">Ім'я</label>
                <input type="text" id="name" v-model="name" minlength="4" maxlength="20" required>
            </div>
            <div>
                <label for="email">Email</label>
                <input type="email" id="email" v-model="email" required>
            </div>
            <div>
                <label for="password">Пароль</label>
                <input type="password" id="password" v-model="password" minlength="6" required>
            </div>
            <button type="submit">Зареєструватися</button>
        </form>
        <p @click="$emit('unregistration')" class="allocated">Вже є аккаунт? Увійти</p>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'SignUpComponent',
    data() {
        return {
            name: '',
            email: '',
            password: '',
            error:''
        }
    },
    methods: {
        async registration() {
            this.error = '';
            try {
                const response = await axios.post(`https://mytodolist-pcw4.onrender.com/users/sign_up`, {
                    name: this.name,
                    username: this.email,
                    password: this.password
                });
                const userData = response.data;
                
                this.$emit('authorization', userData);
            } catch (err){ 
                if (err.response) {
                    if (err.response.status === 400 && err.response.data && err.response.data.detail === "Username already registered") {
                        this.error = 'Користувач з таким email вже існує';
                    } else {
                        this.error = `Помилка: ${err.response.data.detail || 'Не вдалося зареєструватися. Спробуйте пізніше.'}`;
                    }
                } else if (err.request) {
                    this.error = 'Не вдалося підключитися до сервера. Перевірте ваше інтернет-з\'єднання.';
                } else {
                    this.error = 'Сталася помилка під час відправки запиту.';
                }
            }
        },
        unregistration() {
            this.$emit('unregistration');
        }
    }
}
</script>

<style scoped>
.signup-component{
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