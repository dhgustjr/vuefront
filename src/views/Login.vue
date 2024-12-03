<template>
  <div class="login">
    <h2>로그인</h2>
    <form class="login-form" @submit.prevent="handleLogin">
      <div class="input-group">
        <label for="username">아이디:</label>
        <input type="text" id="username" v-model="username" placeholder="아이디를 입력하세요" />
      </div>
      <div class="input-group">
        <label for="password">비밀번호:</label>
        <input type="password" id="password" v-model="password" placeholder="비밀번호를 입력하세요" />
      </div>
      <button type="submit" class="login-button">로그인</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'LoginPage',
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    handleLogin() {
      // 간단한 로그인 검증 로직
      if (this.username === 'admin' && this.password === '1234') {
        this.$router.push('/home'); // Home 화면으로 이동
      } else {
        alert('아이디 또는 비밀번호가 올바르지 않습니다.');
      }
    },
  },
};
</script>
