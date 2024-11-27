<template>
  <div class="home-container">
    <div class="home-header">
      <h1>추천 여행지</h1>
      <p>인스타그램 api를 이용한 여행지 추천 시스템</p>
    </div>

    <div class="home-grid">
      <div class="home-item-wrapper" v-for="(product, index) in products" :key="index">
        <!-- 여행지명 (카드 위쪽) -->
        <h4 class="destination-name">{{ product }}</h4>
        <!-- 박스 -->
        <div class="home-item">
          <div class="image-wrapper">
            <img :src="images[index]" alt="여행지 이미지" class="room-img" />
          </div>
          <button @click="report[index]++" class="recommend-button">추천</button>
          <span class="recommend-count">추천수: {{ report[index] }}</span>
        </div>
        <!-- 추천여행지 (카드 아래쪽) -->
        <p class="destination-description">{{ prices[index] }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  data() {
    return {
      products: ['여행지명1', '여행지명2'],
      prices: ['추천여행지1', '추천여행지2'],
      images: [
        require('@/assets/room0.jpg'), // 이미지 경로 수정
        require('@/assets/room1.jpg'), // 이미지 경로 수정
      ],
      report: [0, 0],
    };
  },
};
</script>

<style>
/* 홈 화면 컨테이너 */
.home-container {
  display: flex;
  flex-direction: column;
  align-items: center; /* 중앙 정렬 */
  margin: 20px auto;
  text-align: center;
  max-width: 1200px; /* 전체 너비 제한 */
}

/* 홈 화면 헤더 */
.home-header h1 {
  font-size: 2rem;
  margin-bottom: 10px;
  color: #333;
}

.home-header p {
  font-size: 1rem;
  color: #666;
  margin-bottom: 20px;
}

/* 그리드 레이아웃 */
.home-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr); /* 한 줄에 2개의 칸 배치 */
  gap: 20px; /* 칸 사이의 간격 */
  justify-content: center; /* 중앙 정렬 */
  width: 100%; /* 전체 너비를 화면에 맞춤 */
  max-width: 900px; /* 그리드의 최대 너비 */
}

/* 박스 스타일 */
.home-item-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center; /* 자식 요소 중앙 정렬 */
  text-align: center; /* 텍스트 중앙 정렬 */
}

.home-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 300px; /* 박스 크기 */
  height: 350px; /* 박스 높이 */
  overflow: hidden;
  transition: transform 0.3s, box-shadow 0.3s;
}

.home-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

/* 이미지 스타일 */
.image-wrapper {
  width: 100%;
  height: 80%; /* 이미지가 박스 내에서 차지할 비율 */
  overflow: hidden;
}

.room-img {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 이미지 비율 유지하며 박스를 채움 */
}

/* 추천여행지 (카드 아래쪽) */
.destination-description {
  text-align: center;
  margin-top: 10px;
  font-size: 1rem;
  color: #666;
}

/* 버튼과 추천수 */
.recommend-button {
  background-color: rgba(0, 0, 0, 0.6);
  color: white;
  border: none;
  border-radius: 5px;
  padding: 8px 20px;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 10px;
  transition: background-color 0.3s;
}

.recommend-button:hover {
  background-color: rgba(0, 0, 0, 0.8);
}

.recommend-count {
  margin-top: 8px;
  font-size: 0.9rem;
  color: #666;
}

.destination-name {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 10px;
}
</style>
