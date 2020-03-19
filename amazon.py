from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import json

url = "https://www.amazon.com/s?k=laptops&i=computers&rh=n%3A172282%2Cn%3A541966%2Cn%3A565108&dc&qid=1584523271&rnid=493964&ref=sr_nr_n_1"


def getSpec(url, driver):
    spec = {
        'brand': None,
        'model': None,
        'processor': None,
        'RAM': None,
        'storage': None,
        'graphic': None
    }

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    try:
        driver.get(url)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.ID, 'productDetails_techSpec_section_1')))

        soup = BS(driver.page_source, 'lxml')

        product_table = soup.find('table', attrs={
            'id': 'productDetails_techSpec_section_1'})
        # print(product_table)
        if product_table != None:
            for elements in product_table.find_all('tr'):
                label = elements.find('th')
                content = elements.find('td')

                # print("Label\t\t: " + str(label.text))
                if label == None:
                    continue
                elif label.text.strip() == "Processor":
                    spec['processor'] = content.text.strip()
                elif label.text.strip() == "RAM":
                    spec['RAM'] = content.text.strip()
                elif label.text.strip() == "Hard Drive":
                    spec['storage'] = content.text.strip()
                elif label.text.strip() == "Graphics Coprocessor":
                    spec['graphic'] = content.text.strip()
                else:
                    continue

        product_table = soup.find('table', attrs={
            'id': 'productDetails_techSpec_section_2'})
        # print(product_table)
        if product_table != None:
            for elements in product_table.find_all('tr'):
                label = elements.find('th')
                content = elements.find('td')

                # print("Label\t\t: " + str(label.text))
                if label == None:
                    continue
                elif label.text.strip() == "Brand Name":
                    spec['brand'] = content.text.strip()
                elif label.text.strip() == "Series":
                    spec['model'] = content.text.strip()
                else:
                    continue

        driver.close()

    except TimeoutException as TM:
        print("Error Timeout: " + str(TM))
        return spec

    except NoSuchWindowException as NW:
        print("Error No Windows: " + str(NW))

    driver.switch_to.window(driver.window_handles[0])

    return spec


driver_options = Options()
driver_options.add_argument("headless")
driver_options.add_argument("incognito")
driver_options.add_argument("no-default-browser-check")
driver_options.add_argument("no-first-run")
driver_options.add_argument("no-sandbox")
driver_options.add_argument("disable-extensions")

driver = webdriver.Chrome(
    executable_path="/home/fauh45/Code/chrome-driver/chromedriver", options=driver_options)
driver.get(url)
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, 'sg-col-inner')))

output = []

try:
    while True:
        soup = BS(driver.page_source, 'html.parser')

        for wrap in soup.find_all('div', attrs={'class': 's-include-content-margin s-border-bottom s-latency-cf-section'}):
            img_wrapper = wrap.find('div', attrs={
                                    'class': 'sg-col-4-of-24 sg-col-4-of-12 sg-col-4-of-36 sg-col-4-of-28 sg-col-4-of-16 sg-col sg-col-4-of-20 sg-col-4-of-32'})

            img_url = img_wrapper.find('img', attrs={'s-image'})
            img_url = (None if img_url == None else img_url['src'])

            wrapper = wrap.find('div', attrs={
                                'class': 'sg-col-4-of-12 sg-col-8-of-16 sg-col-16-of-24 sg-col-12-of-20 sg-col-24-of-32 sg-col sg-col-28-of-36 sg-col-20-of-28'})
            product_url = wrapper.find(
                'a', attrs={'class': 'a-link-normal a-text-normal'})
            product_url = product_url['href']

            name = wrapper.find(
                'span', attrs={'class': 'a-size-medium a-color-base a-text-normal'})
            name = name.text

            price = wrapper.find('span', attrs={'class': 'a-offscreen'})
            price = (None if price == None else price.text)

            more_price = wrapper.find(
                'div', attrs={'class': 'a-section a-spacing-none a-spacing-top-mini'})
            if more_price != None:
                more_price = more_price.find(
                    'span', attrs={'class': 'a-color-base', 'dir': 'auto'})

            more_price = (None if more_price == None else more_price.text)

            rating_wrapper = wrapper.find(
                'div', attrs={'class': 'a-section a-spacing-none a-spacing-top-micro'})
            if rating_wrapper != None:
                rating = rating_wrapper.find(
                    'span', attrs={'class': 'a-icon-alt'})
                num_of_rating = rating_wrapper.find(
                    'span', attrs={'class': 'a-size-base', 'dir': 'auto'})

                rating = (None if rating ==
                          None else rating.text.split(" ")[0])
                num_of_rating = (0 if num_of_rating ==
                                 None else num_of_rating.text)
            else:
                rating = None
                num_of_rating = 0

            print("Name\t\t: " + str(name))
            print("URL\t\t: " + 'https://www.amazon.com' + str(product_url))
            print("Image URL\t: " + str(img_url))
            print("Price\t\t: " + str(price))
            print("More Options\t: " + str(more_price))
            print("Rating\t\t: " + str(rating))
            print("Num Of Rating\t: " + str(num_of_rating))

            spec = getSpec(
                ('https://www.amazon.com' + str(product_url)), driver)
            print(spec)
            print()

            output.append(
                {
                    'name': str(name),
                    'url': 'https://www.amazon.com' + str(product_url),
                    'img-url': str(img_url),
                    'price': str(price),
                    'more-options-price': str(more_price),
                    'rating': str(rating),
                    'num-of-rating': str(num_of_rating),
                    'spec': spec
                }
            )

        try:
            # button = driver.find_element_by_class_name('a-pagination')
            button = driver.find_element_by_class_name('a-last')

            if button.is_enabled() and button.is_displayed():
                button.click()

                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, 'sg-col-inner')))
                print("\n\nCLICK!\n\n")
            else:
                break

        except NoSuchElementException as NE:
            print("No Elements :" + str(NE))
            break

# except TimeoutException as TE:
#     print("Timeout Error" + str(TE))
#     pass

except KeyboardInterrupt:
    print("Exception Ctrl+C!")

    print("Dumping...")
    with open('amazon.json', 'w') as file:
        json.dump(output, file, indent=4)

    print("Done...")

print("Done!\nDumping...")
with open('amazon.json', 'w') as file:
    json.dump(output, file, indent=4)

print("Done...")

driver.quit()
