<template>
  <div>
    <LoginComponent v-if="!Auth && !Regist" @authorization="authorization" @registration="registration"/>
    <SignUpComponent v-if="!Auth && Regist" @authorization="authorization" @unregistration="unregistration" />
    <TaskComponent v-if="Auth && User" :user="User" @logout="logout"/> 
  </div>
</template>

<script>
import LoginComponent from './components/LoginComponent.vue'
import SignUpComponent from './components/SignUpComponent.vue'
import TaskComponent from './components/TaskComponent.vue'

export default {
  name: 'App',
  components: {
    LoginComponent,
    SignUpComponent,
    TaskComponent
  },
  data() {
    return{
      Auth: false,
      Regist: false,
      User: null
    }
  },
  methods: {
    authorization(user) {
      this.Auth = true
      this.User = user
    },
    registration() {
      this.Regist = true
    },
    unregistration() {
      this.Regist = false
    },
    logout() {
      this.Auth = false
      this.Regist = false
      this.User = null
    },
  }
}
</script>

<style scoped>
</style>
