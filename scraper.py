import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re
import time
import random
from datetime import datetime, timedelta
from fake_useragent import UserAgent

# === KONFIGURASI SELENIUM ===
ua = UserAgent()

def get_driver():
    options = uc.ChromeOptions()
    options.add_argument(f"user-agent={ua.random}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.headless = False  # Ubah ke True jika ingin lebih stealth

    driver = uc.Chrome(options=options, use_subprocess=True)
    return driver

# === FUNGSI PENGECEKAN CAPTCHA ===
def check_captcha(driver):
    if "sorry/index" in driver.current_url or "consent.google.com" in driver.current_url:
        print("⚠ CAPTCHA terdeteksi! Ganti IP atau gunakan akun Google.")
        return True
    return False

# === SCRAPING GOOGLE ===
def scrape_google(query, max_results=1000):
    driver = get_driver()
    data = []
    current_time = datetime.now()

    driver.get("https://www.google.com/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))

    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(random.uniform(2, 5))  # Delay acak agar tidak dicurigai

    page = 1
    while len(data) < max_results:
        if check_captcha(driver):
            break  # Keluar jika kena CAPTCHA

        try:
            # Gunakan alternatif selector jika "div.tF2Cxc" tidak ditemukan
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.tF2Cxc, div.g"))
            )
            results = driver.find_elements(By.CSS_SELECTOR, "div.tF2Cxc, div.g")

            for result in results:
                try:
                    title = result.find_element(By.TAG_NAME, "h3").text
                    link = result.find_element(By.TAG_NAME, "a").get_attribute("href")
                    description = result.find_element(By.CLASS_NAME, "VwiC3b").text

                    release_date = current_time.strftime("%d/%m/%Y")  # Default: hari ini

                    data.append({
                        "Judul": title,
                        "Deskripsi": description,
                        "Tanggal Rilis": release_date,
                        "Link": link
                    })

                    if len(data) >= max_results:
                        break
                except:
                    continue

            if len(data) >= max_results:
                break

            # Scroll halaman agar terlihat natural
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(2, 5))

            # Pindah ke halaman berikutnya
            try:
                next_button = driver.find_element(By.LINK_TEXT, "Berikutnya")
                next_button.click()
                time.sleep(random.uniform(2, 5))
                page += 1
            except:
                print("🚫 Tidak ada halaman berikutnya.")
                break

        except Exception as e:
            print(f"⚠ Kesalahan pada halaman {page}: {e}")
            break

    driver.quit()
    return data

# === JALANKAN SCRAPING ===
query = "Berita politik Indonesia 2025"
data = scrape_google(query, max_results=1000)

# Simpan ke CSV
df = pd.DataFrame(data)
df.to_csv("hasil_scraping_fix.csv", index=False)
print(f"✅ Scraping selesai! Data yang dikumpulkan: {len(df)}")
