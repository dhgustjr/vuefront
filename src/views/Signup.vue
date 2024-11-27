<template>
    <div class="signup">
      <h2>회원가입</h2>
      <form class="signup-form">
        <div class="input-group">
          <label for="username">아이디:</label>
          <input type="text" id="username" placeholder="아이디를 입력하세요" />
        </div>
        <div class="input-group">
          <label for="password">비밀번호:</label>
          <input type="password" id="password" placeholder="비밀번호를 입력하세요" />
        </div>
        <div class="input-group">
          <label for="nickname">닉네임:</label>
          <input type="text" id="nickname" placeholder="닉네임을 입력하세요" />
        </div>
        <div class="input-group">
          <label for="email">이메일:</label>
          <input type="email" id="email" placeholder="이메일을 입력하세요" />
        </div>
        <button type="submit" class="signup-button">회원가입</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    name: 'SignupPage', // 다중 단어 이름 사용
  };
  </script>
  
  <style>
  .signup {
    margin: 20px auto;
    text-align: center;
    max-width: 400px;
  }
  
  .signup-form {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .input-group {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
    width: 100%;
  }
  
  .input-group label {
    width: 120px;
    text-align: right;
    margin-right: 10px;
  }
  
  .input-group input {
    flex: 1;
    padding: 5px;
    font-size: 14px;
  }
  
  .signup-button {
    margin-top: 10px;
    padding: 10px 20px;
    font-size: 16px;
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .signup-button:hover {
    background-color: #45a049;
  }
  </style>
  