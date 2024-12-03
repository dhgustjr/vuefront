<template>
  <div class="home-container">
    <div class="home-grid" v-if="images.length > 0">
      <div class="home-item-wrapper">
        <!-- 여행지명 -->
        <h4 class="destination-name">{{ products[currentIndex] }}</h4>

        <!-- 이미지 영역 -->
        <div
          class="home-item"
          @mousedown="onMouseDown"
          @mousemove="onMouseMove"
          @mouseup="onMouseUp"
          @mouseleave="onMouseLeave"
        >
          <div class="image-wrapper">
            <img
              v-if="images[currentIndex]"
              :src="images[currentIndex]"
              alt="여행지 이미지"
              class="room-img"
            />
          </div>
        </div>

        <!-- 추천 버튼 및 추천 수 -->
        <div class="action-container">
          <button @click.stop.prevent="report[currentIndex]++" class="recommend-button">👍 추천</button>
          <span class="recommend-count">추천수: {{ report[currentIndex] }}</span>
        </div>

        <!-- 추천 여행지 설명 -->
        <p class="destination-description">{{ prices[currentIndex] }}</p>
      </div>
    </div>
    <p v-else>이미지를 불러오는 중입니다...</p>

    <!-- 메뉴 -->
    <div class="menu">
      <router-link to="/">HOME</router-link>
      <router-link to="/login">로그인</router-link>
      <router-link to="/signup">회원가입</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomePage",
  data() {
    return {
      products: [],
      prices: [],
      images: [],
      report: [],
      currentIndex: 0,
      startX: 0,
      isDragging: false,
    };
  },
  async created() {
    try {
      const imageCount = await this.getImageCount();
      for (let i = 0; i < imageCount; i++) {
        this.images.push(require(`@/assets/room${i}.jpg`));
        this.products.push(`🗻 여행지명${i + 1}`);
        this.prices.push(`🌟 추천여행지${i + 1}`);
        this.report.push(0);
      }
    } catch (error) {
      console.error("이미지를 로드하는 중 오류 발생:", error);
    }
  },
  methods: {
    async getImageCount() {
      const context = require.context("@/assets", false, /room\d+\.jpg$/);
      return context.keys().length;
    },
    onMouseDown(event) {
      this.startX = event.clientX;
      this.isDragging = true;
    },
    onMouseMove(event) {
      if (this.isDragging) {
        const deltaX = event.clientX - this.startX;
        if (deltaX > 50) {
          this.prevSlide();
          this.isDragging = false;
        } else if (deltaX < -50) {
          this.nextSlide();
          this.isDragging = false;
        }
      }
    },
    onMouseUp() {
      this.isDragging = false;
    },
    onMouseLeave() {
      this.isDragging = false;
    },
    nextSlide() {
      this.currentIndex = (this.currentIndex + 1) % this.images.length;
    },
    prevSlide() {
      this.currentIndex = (this.currentIndex - 1 + this.images.length) % this.images.length;
    },
  },
};
</script>

<style>
/* 기존 CSS 유지 */
.home-container {
  font-family: "Arial", sans-serif;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 20px auto;
  text-align: center;
  max-width: 1200px;
  padding: 20px;
  background: linear-gradient(to bottom, #f8f9fa, #e9ecef);
  border-radius: 15px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  position: relative;
  min-height: 100vh;
}

/* 이미지 영역 */
.home-item {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  width: 350px;
  height: 400px;
  border: 2px solid #007bff;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  margin: 20px 0;
  background: white;
  cursor: grab;
}

.home-item:active {
  cursor: grabbing;
}

/* 하단 메뉴 */
.menu {
  background: darkslateblue;
  padding: 15px;
  text-align: center;
  width: 100%;
  position: fixed;
  bottom: 0;
}

.menu a {
  color: white;
  margin: 0 10px;
  text-decoration: none;
}

.menu a:hover {
  text-decoration: underline;
}
</style>

