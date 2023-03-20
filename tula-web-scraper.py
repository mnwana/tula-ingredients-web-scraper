from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

driver = webdriver.Chrome()
ingredientList = {}

# gather product list pages
urls = []
homepage = 'https://www.tula.com/collections/all'
driver.get(homepage)
productBlocks = driver.find_elements(By.CLASS_NAME, "imageContainer")
for i in range(len(productBlocks)):
    driver.implicitly_wait(2)
    urls.append(productBlocks[i].get_attribute("href"))

# for each page, get html / text from ingredients tab and clean it up. will collect page location and product name and cutesey name
for url in urls:
    driver.implicitly_wait(2)
    if "product" in url and "card" not in url and "rennovation" not in url:
        print(url)
        driver.get(url)
        try:
            ingredientsP = driver.find_elements(
                By.ID, "tabSection-ingredients")[0]
            children = ingredientsP.find_elements(By.TAG_NAME, "div")
            for child in children:
                classname = child.get_attribute("className")
                if "panel_body" in classname:
                    try:
                        cleanHtml = child.get_attribute(
                            "innerHTML").split("<br>")[2].strip()
                    except:
                        cleanHtml = child.get_attribute(
                            "innerHTML").strip()
                    ingredientList[url] = cleanHtml
        except:
            print("no ingredients tab")


driver.close()

(pd.DataFrame.from_dict(data=ingredientList, orient='index').to_csv(
    'tulaIngredientList.csv', header=True))
