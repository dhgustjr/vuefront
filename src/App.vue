#npm run serve 실행 

<template>
  <div>
    <!-- 메뉴 -->
    <div class="menu">
      <a @click="navigateTo('/')">HOME</a>
      <a @click="navigateTo('/login')">로그인</a>
      <a @click="navigateTo('/signup')">회원가입</a>
    </div>

    <!-- 라우터 뷰 -->
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'App',
  methods: {
    navigateTo(route) {
      this.$router.push(route); // 라우터 경로 이동
    },
  },
};
</script>

<style>
/* 기존 스타일 유지 */
.menu {
  background: darkslateblue;
  padding: 15px;
  text-align: center;
}

.menu a {
  color: white;
  margin: 0 10px;
  cursor: pointer;
  text-decoration: none;
}

.menu a:hover {
  text-decoration: underline;
}
</style>
