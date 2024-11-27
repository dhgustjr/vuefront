<template>
  <div class="login">
    <h2>로그인</h2>
    <form class="login-form">
      <div class="input-group">
        <label for="username">아이디:</label>
        <input type="text" id="username" placeholder="아이디를 입력하세요" />
      </div>
      <div class="input-group">
        <label for="password">비밀번호:</label>
        <input type="password" id="password" placeholder="비밀번호를 입력하세요" />
      </div>
      <button type="submit" class="login-button">로그인</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'LoginPage',
};
</script>

<style>
.login {
  margin: 20px auto;
  text-align: center;
  max-width: 400px;
}

.login-form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.input-group {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
  width: 100%;
}

.input-group label {
  width: 100px;
  text-align: right;
  margin-right: 10px;
}

.input-group input {
  flex: 1;
  padding: 8px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.login-button {
  margin-top: 10px;
  padding: 10px 20px;
  font-size: 16px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.login-button:hover {
  background-color: #45a049;
}
</style>
