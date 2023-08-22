from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient

# MongoDB connection details
MONGODB_URI = "mongodb://localhost:27017/"
DB_NAME = "insiderbiz"
COLLECTION_NAME = "companies"

# Configure Selenium web driver
#chrome_options = Options()
#chrome_options.add_argument("--headless")  # Run in headless mode
service = Service(r"C:\Users\AJAO SEYI\Desktop\ML\chromedriver_win32\chromedriver.exe")  # Replace with path to chromedriver executable
driver = webdriver.Chrome(service=service)

# Connect to MongoDB
client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Scrape data from InsiderBiz
base_url = "https://www.insiderbiz.in/company-list/?page="
page_limit = 10

for page in range(1, page_limit + 1):
    url = base_url + str(page)
    driver.get(url)

    wait = WebDriverWait(driver, 10)
    table =wait.until(EC.presence_of_element_located((By.ID, "datatable")))
    rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # Skip header row

    for row in rows:
        columns = row.find_elements(By.TAG_NAME, "td")
        cin = columns[0].text
        company_name = columns[1].text
        roc = columns[2].text
        address = columns[3].text

        # Create a document and insert into MongoDB
        document = {
            "CIN": cin,
            "COMPANY NAME": company_name,
            "ROC": roc,
            "ADDRESS": address
        }
        collection.insert_one(document)

# Close the web driver and MongoDB connection
driver.quit()
client.close()
