<template>
    <div class="task-component">
        <p v-if="user">Привіт, {{ user.name }}! Ось твій список справ ✨</p>
        <button @click="$emit('logout')">Вийти</button>
        <div>
            <label for="search">Знайти задачу </label>
            <input type="text" id="search" v-model="searchQuery" placeholder="Введіть назву або опис..." />
        </div>
        <p v-if="error !== ''" class="error">{{error}}</p>
        <nav>
            <span class="allocated" @click="setFilter('all')">Усі завдання |</span>
            <span class="allocated" @click="setFilter('completed')">Виконані завдання |</span>
            <span class="allocated" @click="setFilter('incomplete')">Не виконані завдання</span>
        </nav>
        <section v-if="filteredTasks.length > 0">
            <div v-for="task in filteredTasks" :key="task.id">
                <div v-if="task.id !== editbutton_id" class="task">
                    <div>
                        <h3 :class="task.completed ? 'completed' : ''">{{ task.title }}</h3>
                        <p>{{ task.description }}</p>
                        <input type="checkbox" :checked="task.completed" @change="completedTask(task, !task.completed)" />
                        <p :class="task.date < todayDate ? 'redDate' : ''">Дата виконання: {{ task.date }}</p>
                    </div>
                    <div class="buttons">
                        <button @click="deleteTask(task.id)">Видалити</button>
                        <button @click="editbutton_id = task.id">Редагувати</button>
                    </div>
                </div>
                <EditTask v-if="task.id === editbutton_id" :task="task" @fetchTasks="fetchTasks" @editbutton="editbutton_id = $event" @handleAuthError="this.$emit('handleAuthError')" @todayDate="todayDate"/>
            </div>
        </section>
        <p v-if="tasks.length > 0 && filteredTasks.length === 0 && searchQuery != ''">Завдання не знайдено за вашим запитом та фільтром.</p>
        <p v-if="tasks.length === 0 && searchQuery === ''">У вас ще немає задач. Додайте першу!</p>
        <button v-if="!addbutton" @click="addbutton = !addbutton">Додати задачу</button>
        <AddTask v-if="addbutton" :user_id="user.id" @fetchTasks="fetchTasks" @addbutton="addbutton = $event" @handleAuthError="this.$emit('handleAuthError')" @todayDate="todayDate" />

    </div>
</template>

<script>
import axios from 'axios';
import AddTask from './AddTask.vue';
import EditTask from './EditTask.vue';

export default {
    name: 'TaskComponent',
    components: {
        AddTask,
        EditTask
    },
    props: {
        user: Object
    },
    data() {
        return {
            tasks: [],
            error: '',
            addbutton: false,
            editbutton_id: 0,
            searchQuery: '',
            filterStatus: 'all' // 'all', 'completed', 'incomplete'
        }
    },
    computed: {
        filteredTasks() {
            let tasksToFilter = this.tasks;

            if (this.filterStatus === 'completed') {
                tasksToFilter = this.tasks.filter(task => task.completed);
            } else if (this.filterStatus === 'incomplete') {
                tasksToFilter = this.tasks.filter(task => !task.completed);
            }

            if (!this.searchQuery) {
                return tasksToFilter;
            }

            const lowerCaseQuery = this.searchQuery.toLowerCase();
            return tasksToFilter.filter(task =>
                task.title.toLowerCase().includes(lowerCaseQuery) ||
                task.description.toLowerCase().includes(lowerCaseQuery)
            );
        },
        todayDate() {
            const today = new Date();
            const yyyy = today.getFullYear();
            const mm = String(today.getMonth() + 1).padStart(2, '0');
            const dd = String(today.getDate()).padStart(2, '0');
            return `${yyyy}-${mm}-${dd}`;
        }
    },
    methods: {
        async fetchTasks() {
            this.error = '';
            try {
                const response = await axios.get(`https://mytodolist-pcw4.onrender.com/tasks/${this.user.id}`);
                this.tasks = response.data;
            } catch (err) {
                this.$emit('handleAuthError', err);
            }
        },
        async deleteTask(id) {
            try {
                await axios.delete(`https://mytodolist-pcw4.onrender.com/tasks/${id}`);
                this.fetchTasks();
            } catch (err) {
                this.$emit('handleAuthError', err);
            }
        },
        async completedTask(task, completed) {
            try {
                await axios.put(`https://mytodolist-pcw4.onrender.com/tasks/${task.id}/`, {
                    title: task.title,
                    description: task.description,
                    completed: completed,
                    date: task.date,
                    user_id: task.user_id
                });
                this.fetchTasks();
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
        },
        setFilter(status) {
            this.filterStatus = status;
        }
    },
    watch: {
        user: {
            handler(newUser) {
                if (newUser && newUser.id) {
                    this.fetchTasks();
                } else {
                    this.tasks = [];
                    this.error = '';
                }
            },
            immediate: true
        }
    }
}
</script>

<style scoped>
.task-component{
    color: #fff;
    padding: 30px 10px;
    border-radius: 10px;
    margin: auto;
    width: clamp(100px, 80%, 700px);
    text-align: center;
}

section > div{
    background-color: #111;
    border-radius: 10px;
    margin:10px 0;
    padding: 10px;
}
section div input[type="checkbox"]{
    accent-color: #6e2d7d;
}

.completed{
    text-decoration: line-through;
}
.task{
    display: flex;
    justify-content: space-around;
    align-items: center;
    flex-wrap: wrap;
    text-align: left;
}
.task > div{
    width: 50%;
}
.buttons{
    text-align: right;
}
.redDate{
    color: rgb(255, 77, 77);
}

nav{
    margin:20px 0;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
}

@media screen and (max-width: 768px) {
    .task > div{
        width: 100%;
    }
}

</style>