<template>
    <div class="task-component-operation">
        <p v-if="error !== ''" class="error">{{error}}</p>
        <button @click="$emit('editbutton', 0)" class="close-button">Закрити</button>
        <form @submit.prevent="editTask">
            <div>
                <label for="title">Назва завдання</label>
                <input type="text" id="title" maxlength="256" v-model="title" required />
            </div>
            <div>
                <label for="description">Опис завдання</label>
                <textarea id="description" v-model="description" required></textarea>
            </div>
            <div>
                <label for="date">Дата виконання</label>
                <input type="date" id="date" v-model="date" :min="todayDate" required/>
            </div>
            <button type="submit">Зберегти зміни</button>
        </form>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'EditTask',
    props: {
        task: Object
    },
    data() {
        return {
            title: this.task.title || '',
            description: this.task.description || '',
            completed: this.task.completed,
            date: this.task.date || '',
            error: ''
        };
    },
    methods: {
        async editTask() {
            try {
                this.error = '';
                if (this.title === '' || this.description === '' || this.date === '') {
                    this.error = 'Будь ласка, заповніть всі поля.';
                    return;
                }
                await axios.put(`https://mytodolist-pcw4.onrender.com/tasks/${this.task.id}/`, {
                    title: this.title,
                    description: this.description,
                    completed: this.completed,
                    date: this.date,
                    user_id: this.task.user_id 
                });
                this.$emit('fetchTasks');
                this.$emit('editbutton', 0); 
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