<template>
    <div class="task-component-operation">
        <p v-if="error !== ''" class="error">{{error}}</p>
        <button @click="$emit('addbutton', false)" class="close-button">Закрити</button>
        <form @submit.prevent="addtask">
            <div>
                <label for="title">Назва завдання</label>
                <input type="text" id="title" maxlength="256" v-model="title" required />
            </div>
            <div>
                <label for="description">Опис завдання</label>
                <textarea type="text" id="description" v-model="description" required></textarea>
            </div>
            <div>
                <label for="date">Дата виконання</label>
                <input type="date" id="date" v-model="date" :min="todayDate" required/>
            </div>
            <button type="submit">Додати задачу</button>
        </form>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'AddTask',
    props: {
        user_id: Number
    },
    data() {
        return {
            title: '',
            description: '',
            completed: false,
            date: '',
            error: ''
        }
    },
    computed: {
        todayDate() {
            const today = new Date();
            const yyyy = today.getFullYear();
            const mm = String(today.getMonth() + 1).padStart(2, '0');
            const dd = String(today.getDate()).padStart(2, '0');
            return `${yyyy}-${mm}-${dd}`;
        }
    },
    methods: {
        async addtask() {
            try {
                this.error = '';
                if (this.title === '' || this.description === '' || this.date === '') {
                    this.error = 'Будь ласка, заповніть всі поля.';
                    return;
                }
                await axios.post('https://mytodolist-pcw4.onrender.com/tasks', {
                    title: this.title,
                    description: this.description,
                    completed: this.completed,
                    date: this.date,
                    user_id: this.user_id
                });
                this.$emit('fetchTasks');
                this.$emit('addbutton', false);
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

form > div {
    display: flex;
    align-items: center; 
    margin-bottom: 15px; 
    text-align: left;
}
label{
    margin-bottom: 0;
    margin-right: 10px;
    min-width: 120px; 
}


</style>