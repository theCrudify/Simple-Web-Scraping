import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# Konfigurasi User-Agent agar tidak terdeteksi sebagai bot
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/110.0.0.0 Safari/537.36"

options = uc.ChromeOptions()
options.add_argument(f"user-agent={user_agent}")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")

# Hapus headless agar bisa melihat hasil secara langsung
# options.headless = True  # Jika ingin tetap headless, aktifkan ini

# Jalankan driver Chrome
driver = uc.Chrome(options=options)

# Buka Google Search
driver.get("https://www.google.com/")
time.sleep(2)  # Tunggu halaman termuat

# Masukkan kata kunci ke dalam kotak pencarian
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("Presiden Prabowo Subianto")
search_box.send_keys(Keys.RETURN)

# Tunggu hasil pencarian muncul
time.sleep(5)

# Coba ambil data dari hasil pencarian
products = []
results = driver.find_elements(By.CSS_SELECTOR, "div.tF2Cxc")

if not results:
    print("⚠ Tidak ada hasil yang ditemukan! Coba periksa struktur HTML.")

for result in results:
    try:
        title = result.find_element(By.TAG_NAME, "h3").text
        link = result.find_element(By.TAG_NAME, "a").get_attribute("href")
        description = result.find_element(By.CLASS_NAME, "VwiC3b").text
        products.append({"Judul": title, "Deskripsi": description, "Link": link})
    except:
        continue

# Simpan ke CSV
df = pd.DataFrame(products)
df.to_csv("hasil_scraping.csv", index=False)
print(df)

# Tutup browser
driver.quit()
