<template>
  <section class="app-main" :style="{ minHeight: minHeight }">
    <router-view>
      <template #default="{ task_name }">
        <!-- <transition
          enter-active-class="animate__animated animate__fadeIn"
          mode="out-in"
        >
        </transition> -->
        <p>{{ task_name }}</p>
      </template>
    </router-view>
  </section>
</template>
