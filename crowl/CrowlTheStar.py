import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from urllib.request import urlretrieve
from dotenv import load_dotenv
import os
import time
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)

# 1. 해시태그 검색 URL 생성
def insta_searching(word: str) -> str:
    url = f'https://www.instagram.com/explore/tags/{word}'
    logging.info(f"{word} 해시태그 검색 URL: {url}")
    return url

# 2. Instagram 로그인
def login_instagram(driver, username: str, password: str):
    driver.get('https://www.instagram.com/accounts/login/')
    logging.info("로그인 페이지로 이동했습니다.")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "password").submit()
    time.sleep(2)
    
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[text()="나중에 하기"]'))
        ).click()
        logging.info("로그인 정보 저장 팝업 클릭 완료.")
    except Exception:
        logging.info("팝업이 없거나 이미 처리됨.")

# 3. 이미지 URL 추출 (게시글 내 마지막 이미지만 추출)
def extract_last_image_url(driver):
    try:
        # 게시글 내 이미지 추출
        images = driver.find_elements(By.CSS_SELECTOR, "img.x5yr21d.xu96u03.x10l6tqk.x13vifvy.x87ps6o.xh8yej3")
        img_urls = []
        if images:
            # 페이지에서 마지막 이미지를 추출
            for image in images:
                img_url = image.get_attribute("src")
                if not img_url:
                    # src가 없는 경우 srcset에서 가져오기
                    img_url = image.get_attribute("srcset")
                    if img_url:
                        # srcset에서 가장 큰 이미지 URL 선택
                        img_url = img_url.split(',')[-1].split(' ')[0]  # 가장 큰 이미지 URL 선택

                # 실제 이미지 URL만 필터링 (섬네일 제외)
                if img_url and "thumbnail" not in img_url and img_url not in img_urls:
                    img_urls.append(img_url)

            # 마지막 이미지만 리턴
            if img_urls:
                last_image_url = img_urls[-1]
                logging.info(f"게시글 내 마지막 이미지 URL 추출 완료: {last_image_url}")
                return [last_image_url]
            else:
                logging.warning("게시글 내 유효한 이미지가 없습니다.")
                return []
        else:
            logging.warning("이미지 요소를 찾을 수 없습니다.")
            return []
    except Exception as e:
        logging.error(f"이미지 URL 추출 실패: {e}")
        return []

# 4. 이미지 다운로드
def download_image(image_url, save_path):
    try:
        if image_url:  # image_url이 None이 아닌지 확인
            urlretrieve(image_url, save_path)
            logging.info(f"이미지 저장 완료: {save_path}")
        else:
            logging.warning(f"이미지 URL이 없어서 다운로드하지 않았습니다: {save_path}")
    except Exception as e:
        logging.error(f"이미지 다운로드 실패: {e}")

    # 태그 가져오기 함수
def get_tag(driver):
    try:
        # 페이지 로드 대기
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, '_ap3a')))

        # 페이지 소스 가져오기
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # 해시태그 포함된 게시글 내용 추출
        try:
            tags_text_element = driver.find_element(By.CSS_SELECTOR, 'h1._ap3a._aaco._aacu._aacx._aad7._aade')
            tags_text = tags_text_element.text if tags_text_element else ''
        except Exception:
            print("태그 텍스트를 찾을 수 없습니다.")
            tags_text = ''

        # 유효성 검사
        if not tags_text:
            print("게시글이 비어 있음: 추출된 데이터 없음")
        else:
            print("태그 텍스트 추출 완료.")

        hashtags = re.findall(r'#\S+', tags_text) # 정규 표현식
        return hashtags  # 태그만 반환

    except Exception as e:
        print("태그 텍스트 추출 실패:", e)
        return ''  # 빈 값을 반환

# 5. 게시글 내 다중 이미지 넘기기
def move_to_next_image_in_post(driver):
    try:
        # 'div._9zm2'는 다음 이미지 버튼으로 확인되었으므로 해당 요소 클릭
        next_image_button = driver.find_elements(By.CSS_SELECTOR, "div._9zm2")
        if next_image_button:
            next_image_button[0].click()  # 첫 번째 다음 이미지 버튼 클릭
            logging.info("다음 이미지로 이동.")
            time.sleep(2)  # 크롤링 속도 조절
            return True
        else:
            logging.info("더 이상 이동 가능한 이미지가 없습니다.")
            return False
    except Exception as e:
        logging.error(f"이미지 이동 중 오류 발생: {e}")
        return False

#5.5  URL에서 파일명을 추출하고, 파일명에 포함될 수 없는 특수문자들을 안전한 문자로 대체합니다.
def clean_filename(url):
    # URL에서 파일명만 추출
    filename = url.split("/")[-1].split("?")[0]
    
    # 파일명에 포함될 수 없는 특수문자들을 '_'로 치환
    filename = re.sub(r'[\\/:*?"<>|]', '_', filename)
    
    return filename

# 6. 게시글 이동 (다음 버튼)
def move_to_next_post(driver):
    try:
        # 여러 개의 ._abl- 요소를 찾고, 두 번째 요소를 클릭
        next_post_buttons = driver.find_elements(By.CSS_SELECTOR, "button._abl-")
        if len(next_post_buttons) > 1:  # 두 번째 버튼이 존재하는 경우
            next_post_buttons[1].click()  # 두 번째 요소 (다음 게시글 버튼 클릭)
            logging.info("다음 게시글로 이동 성공.")
            time.sleep(2)
            return True
        else:
            logging.warning("다음 버튼이 존재하지 않습니다.")
            return False
    except Exception as e:
        logging.error(f"다음 게시글로 이동 실패 (더 이상 게시글 없음): {e}")
        return False

# 7. 이미지 크롤링
def crawl_the_star(driver, target, download_folder, word):
    results = []  # 최종 크롤링된 이미지 URL 저장
    all_tags = []  # 각 게시글의 태그를 저장하는 리스트

    downloaded_urls = set()  # 이미 다운로드된 이미지 URL 추적

    # 검색 페이지 이동
    driver.get(insta_searching(word))
    logging.info(f"{word} 해시태그 페이지로 이동.")
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div._aagw")))

    # 첫 번째 게시글 대기 및 클릭
    try:
        first_post = driver.find_element(By.CSS_SELECTOR, "div._aagw")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_post)
        driver.execute_script("arguments[0].click();", first_post)
        logging.info("첫 번째 게시글 클릭 성공.")
    except Exception as e:
        logging.error(f"첫 번째 게시글 클릭 실패: {e}")
        return results

    # 게시글 크롤링 루프
    p=0  # 몇번째 이미지인지 카운트
    for i in range(target):
        try:
            # 이미지 요소 대기
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "img")))
            
            # 태그 추출
            tags = get_tag(driver)
            all_tags.append(tags)  # 각 게시글마다 태그 저장

            # 이미지 URL 추출
            img_urls = extract_last_image_url(driver)
            new_urls = [url for url in img_urls if url not in downloaded_urls]  # 새로운 URL만 필터링

            if new_urls:
                for j, img_url in enumerate(new_urls):
                    # 파일명 생성 (clean_filename 호출)
                    filename = clean_filename(img_url)
                    save_path = os.path.join(download_folder, filename)  # 안전한 파일명으로 저장
                    
                    # 카운트 증가 및 다운로드
                    p += 1
                    download_image(img_url, save_path)
                    downloaded_urls.add(img_url)  # 다운로드된 URL 기록
                results.extend(new_urls)
                logging.info(f"{i+1}번째 게시글: 새로운 이미지 {len(new_urls)}개 다운로드 완료.")
            else:
                logging.info(f"{i+1}번째 게시글: 새로운 이미지 URL 없음.")

            # 게시글 내 다중 이미지 넘기기
            if not move_to_next_image_in_post(driver):
                logging.info("더 이상 게시글 내 이미지가 없습니다. 게시글 이동.")
                if not move_to_next_post(driver):
                    logging.info("더 이상 게시글이 없습니다. 크롤링 종료.")
                    break

        except Exception as e:
            logging.error(f"{i+1}번째 게시글 처리 중 오류 발생: {e}")
            continue

    # 엑셀로 저장하기 전에 길이가 맞는지 확인
    logging.info(f"이미지 개수: {len(results)}")
    logging.info(f"태그 개수: {len(all_tags)}")

    # 길이가 맞지 않으면 맞추기
    if len(results) != len(all_tags):
        if len(results) > len(all_tags):
            all_tags.extend([""] * (len(results) - len(all_tags)))  # 빈 문자열로 채우기
        else:
            results.extend([None] * (len(all_tags) - len(results)))  # None으로 채우기

    save_to_excel(results, all_tags)

    return results

# 엑셀로 저장
def save_to_excel(image_urls, tags):
    import pandas as pd

    # 결과를 pandas DataFrame으로 변환
    data = {
        'Image URLs': image_urls,
        'Tags': tags
    }
    
    # 길이가 맞지 않으면 수정 (이미 위에서 수정하였으므로 필요하지 않지만 안전장치)
    if len(image_urls) != len(tags):
        min_len = min(len(image_urls), len(tags))
        image_urls = image_urls[:min_len]
        tags = tags[:min_len]

    df = pd.DataFrame(data)

    # 엑셀 파일로 저장
    df.to_excel('instagram_images_and_tags3.xlsx', index=False)
    logging.info("엑셀 파일로 저장 완료.")

# 8. 실행부
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

load_dotenv()
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
download_folder = "C:/Users/Administrator/Desktop/플젝/test_1"

os.makedirs(download_folder, exist_ok=True)
login_instagram(driver, username, password)
word = "성수동"
target_posts = 25
results = crawl_the_star(driver, target_posts, download_folder, word)
driver.quit()
logging.info("크롤링 완료 및 드라이버 종료.")