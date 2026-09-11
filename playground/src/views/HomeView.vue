<script setup lang="ts">
import { useRouter } from 'vue-router'
import { logout } from '../services/auth'

const router = useRouter()

async function handleLogout(): Promise<void> {
  logout()
  await router.replace({ name: 'login' })
}
</script>

<template>
  <main class="dashboard-page">
    <header class="dashboard-header">
      <a class="compact-brand" href="/" aria-label="航标工作台首页">
        <span class="compact-brand-mark" aria-hidden="true"></span>
        航标工作台
      </a>
      <button class="logout-button" type="button" @click="handleLogout">
        退出登录
      </button>
    </header>

    <section class="dashboard-content" aria-labelledby="dashboard-title">
      <p class="eyebrow dark-eyebrow">ROUTE / ARRIVED</p>
      <h1 id="dashboard-title">登录成功，<br />航向已确认。</h1>
      <p class="dashboard-summary">
        你已通过前端模拟认证，并由 Vue Router 跳转到受保护页面。
      </p>

      <div class="status-grid">
        <article class="status-card">
          <span class="status-index">01</span>
          <h2>认证状态</h2>
          <p><span class="status-dot"></span>已登录</p>
        </article>
        <article class="status-card">
          <span class="status-index">02</span>
          <h2>当前路由</h2>
          <p><code>/</code></p>
        </article>
        <article class="status-card">
          <span class="status-index">03</span>
          <h2>技术栈</h2>
          <p>Vue 3 + Vite</p>
        </article>
      </div>
    </section>
  </main>
</template>
