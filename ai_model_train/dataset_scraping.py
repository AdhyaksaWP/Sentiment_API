import re
import time
import csv
import os
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

# --- CONFIGS ---
GOOGLE_MAPS_URL = "https://www.google.com/maps/place/BPJS+Kesehatan+Cabang+Yogyakarta/@-8.059319,109.7918364,9z/data=!4m12!1m2!2m1!1sBPJS+Kesehatan!3m8!1s0x2e7a5769d6777f39:0x8de328c5e008e038!8m2!3d-7.8151233!4d110.4017147!9m1!1b1!15sCg5CUEpTIEtlc2VoYXRhbiIDiAEBkgEWc29jaWFsX3NlY3VyaXR5X29mZmljZaoBaAoNL2cvMTFieWwzZjN2awoML2cvMTJtYjN2NXh2EAEqEiIOYnBqcyBrZXNlaGF0YW4oJjIfEAEiGzsOED_XnZWgIAzYvQGFUyn_T3pnbyb1oxVhCTISEAIiDmJwanMga2VzZWhhdGFu4AEA!16s%2Fg%2F1hc24_t2d?entry=ttu&g_ep=EgoyMDI1MDYwMy4wIKXMDSoASAFQAw%3D%3D"
CHROMEDRIVER_PATH = "D:\\chromedriver-win64\\chromedriver.exe"
CSV_PATH = "./dataset/bpjs_review.csv"
SCROLL_PAUSE_TIME = 2
SCROLL_AMOUNT = -5000
SCROLL_INTERVAL = 2
TOTAL_DURATION = 10 * 60  # 10 minutes

# --- FUNCTIONS ---
def extract_reviews(driver, seen_reviews, csv_writer):
    try:
        review_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "jftiEf fontBodyMedium")]'))
        )

        for review in review_elements:
            try:
                review_text_elem = review.find_element(By.XPATH, './/span[@class="wiI7pd"]')
                review_text = review_text_elem.text.strip()
            except:
                review_text = "N/A"

            if not review_text or review_text in seen_reviews:
                continue

            seen_reviews.add(review_text)

            try:
                rating_elem = review.find_element(By.XPATH, './/span[contains(@aria-label, "bintang")]')
                rating_label = rating_elem.get_attribute("aria-label")
                match = re.search(r"(\d+)", rating_label)
                rating = match.group(1) if match else "N/A"
            except:
                rating = "N/A"

            print(f"Rating: {rating}")
            print(f"Review: {review_text}")
            print("-" * 30)

            # Write to CSV
            csv_writer.writerow([rating, review_text])

    except Exception as e:
        print(f"[!] Error extracting reviews: {e}")


def scroll_reviews_panel(driver):
    try:
        scrollable_div = driver.find_element(By.XPATH, '//div[@class="m6QErb DxyBCb kA9KIf dS8AEf ecceSd"]')
        driver.execute_script("arguments[0].scrollBy(0, 1000);", scrollable_div)
    except Exception as e:
        print(f"[!] Could not scroll review panel: {e}")


def main():
    options = Options()
    options.add_argument("--start-maximized")

    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(GOOGLE_MAPS_URL)

    seen_reviews = set()

    # Prepare output folder
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)

    with open(CSV_PATH, mode='w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Rating", "Review"])  # header

        try:
            reviews_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'reviews')]"))
            )
            reviews_button.click()
            time.sleep(3)
        except Exception:
            print("[!] Could not click reviews button — maybe already visible.")

        print("[*] Starting scroll and scrape loop...")
        start_time = time.time()

        while (time.time() - start_time) < TOTAL_DURATION:
            pyautogui.scroll(SCROLL_AMOUNT)
            time.sleep(5)
            extract_reviews(driver, seen_reviews, csv_writer)
            time.sleep(SCROLL_INTERVAL - 1)

    driver.quit()
    print(f"[✓] Done. Reviews saved to: {CSV_PATH}")

if __name__ == "__main__":
    main()
