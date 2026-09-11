<script setup lang="ts">
import { reactive, shallowRef } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { login } from '../services/auth'

const route = useRoute()
const router = useRouter()
const credentials = reactive({
  username: '',
  password: '',
})
const errorMessage = shallowRef('')
const isSubmitting = shallowRef(false)

async function handleLogin(): Promise<void> {
  errorMessage.value = ''
  isSubmitting.value = true

  await new Promise((resolve) =>
    window.setTimeout(resolve, 360),
  )

  if (!login(credentials)) {
    errorMessage.value = '账号或密码不正确，请使用演示账号重试。'
    isSubmitting.value = false
    return
  }

  const redirect = typeof route.query.redirect === 'string'
    ? route.query.redirect
    : '/'

  await router.replace(redirect)
}
</script>

<template>
  <main class="login-page">
    <section class="brand-panel" aria-labelledby="product-title">
      <div class="brand-mark" aria-hidden="true">
        <span class="brand-mark-core"></span>
      </div>
      <p class="eyebrow">NAV / ACCESS POINT 01</p>
      <h1 id="product-title">
        航标<br />工作台
      </h1>
      <p class="brand-summary">
        清晰辨认方向，安全进入工作空间。
      </p>
      <div class="route-line" aria-hidden="true">
        <span class="route-point route-point-start"></span>
        <span class="route-label">身份验证</span>
        <span class="route-point route-point-end"></span>
        <span class="route-label route-label-end">工作台</span>
      </div>
    </section>

    <section class="login-panel" aria-labelledby="login-title">
      <div class="login-card">
        <p class="step-label">安全入口 · 01</p>
        <h2 id="login-title">欢迎回来</h2>
        <p class="login-intro">输入演示账号，查看登录跳转和路由守卫效果。</p>

        <form class="login-form" @submit.prevent="handleLogin">
          <label for="username">账号</label>
          <input
            id="username"
            v-model.trim="credentials.username"
            name="username"
            type="text"
            autocomplete="username"
            placeholder="请输入账号"
            required
          />

          <label for="password">密码</label>
          <input
            id="password"
            v-model="credentials.password"
            name="password"
            type="password"
            autocomplete="current-password"
            placeholder="请输入密码"
            required
          />

          <p v-if="errorMessage" class="error-message" role="alert">
            {{ errorMessage }}
          </p>

          <button class="login-button" type="submit" :disabled="isSubmitting">
            {{ isSubmitting ? '正在确认航向…' : '进入工作台' }}
            <span aria-hidden="true">→</span>
          </button>
        </form>

        <div class="demo-account">
          <span>演示账号</span>
          <code>admin / vue3</code>
        </div>
      </div>
    </section>
  </main>
</template>
