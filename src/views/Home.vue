<template>
  <div class="home-container">
    <div class="home-header">
      <h1>✈️ 추천 여행지</h1>
      <p>인스타그램 API를 활용한<br /> 맞춤형 여행지 추천 서비스</p>
    </div>

    <!-- 수평 정렬을 위한 그리드 -->
    <div class="home-grid">
      <!-- 스와이프 여행지 추천 -->
      <div class="home-item-wrapper">
        <h4 class="destination-name">{{ products[currentIndex] }}</h4>
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
        <div class="action-container">
          <button @click="saveDestination" class="save-button">💾 저장</button>
          <button @click.stop.prevent="report[currentIndex]++" class="recommend-button">👍 좋아요</button>
          <span class="recommend-count">좋아요: {{ report[currentIndex] }}</span>
        </div>
        <p class="destination-description">{{ prices[currentIndex] }}</p>
      </div>

      <!-- 랜덤 여행지 추천 -->
      <div class="random-item-wrapper">
        <h4 class="destination-name">🎲 랜덤 추천 여행지</h4>
        <div class="random-item">
          <div class="image-wrapper">
            <img
              v-if="randomImage"
              :src="randomImage"
              alt="랜덤 여행지 이미지"
              class="room-img"
            />
          </div>
        </div>
        <div class="action-container">
          <button @click="getRandomImage" class="reload-button">🔄 새로고침</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomePage",
  data() {
    return {
      products: [], // 여행지명 배열
      prices: [], // 추천 여행지 배열
      images: [], // 이미지 배열
      report: [], // 추천수 배열
      currentIndex: 0, // 현재 표시 중인 이미지의 인덱스
      randomImage: null, // 랜덤 추천 이미지
      startX: 0, // 마우스 시작 위치
      isDragging: false, // 드래그 상태
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
      this.getRandomImage();
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
      this.currentIndex =
        (this.currentIndex - 1 + this.images.length) % this.images.length;
    },
    getRandomImage() {
      if (this.images.length > 0) {
        const randomIndex = Math.floor(Math.random() * this.images.length);
        this.randomImage = this.images[randomIndex];
      }
    },
    saveDestination() {
      alert(`${this.products[this.currentIndex]}이(가) 저장되었습니다!`);
    },
  },
};
</script>

<style>
/* 전체 컨테이너 */
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
}

/* 수평 배치를 위한 그리드 */
.home-grid {
  display: flex;
  gap: 20px;
  justify-content: center;
  align-items: flex-start;
  width: 100%;
  max-width: 1200px;
}

/* 공통 이미지 스타일 */
.image-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 스와이프 섹션 */
.home-item-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 45%;
}

.home-item {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 400px;
  border: 2px solid #007bff;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  background: white;
}

.recommend-button {
  margin-top: 10px;
}

.save-button {
  margin-top: 10px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  cursor: pointer;
  font-size: 1rem;
  margin-left: 10px;
}

.save-button:hover {
  background-color: #218838;
}

/* 랜덤 추천 섹션 */
.random-item-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 45%;
}

.random-item {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 400px;
  border: 2px solid #28a745;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  background: white;
}

.reload-button {
  margin-top: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  cursor: pointer;
  font-size: 1rem;
}

.reload-button:hover {
  background-color: #0056b3;
}
</style>
