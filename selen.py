import time
import random

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# отключаем голову браузера
opt = Options()
opt.add_argument('-headless')

# random user agent
r_user_agent = ["Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36", 
                "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36", 
                "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36", 
                "Mozilla/5.0 (Windows NT 6.1; rv:83.0) Gecko/20100101 Firefox/83.0",
                "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 OPR/72.0.3815.320"]
r_user_agent = random.choice(r_user_agent)


# передача user agent
profile = webdriver.FirefoxProfile()
profile.set_preference("general.useragent.override", r_user_agent)

driver = webdriver.Firefox(profile, options=opt)

# настройки для Chrome

# from selenium.webdriver.chrome.options import Options

# opts = Options()
# opts.add_argument('user-agent=r_user_agent)

# browser = webdriver.Chrome(chrome_options=opts)

link = 'https://hh.ru/search/vacancy?st=searchVacancy&text=&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=2&no_magic=true&L_save_area=true'

try:
    r = driver.get(link)

    # получаем список ссылок на объявления
    list_links = driver.find_elements_by_css_selector('a[data-qa=vacancy-serp__vacancy-title]')
    list_for_save = []
    print('Получено ссылок:', len(list_links))

    n = 0
    # извлекаем ссылки из списка и переходим по ним
    for link in list_links: 
        link.click()
        time.sleep(5)

        # переключаемся между окнами
        n += 1
        new_tab = driver.window_handles[n]
        driver.switch_to.window(new_tab)
        print('-*-*-*-*-*-*-*-')
        # получаем поля вакансии
        try:
            title = driver.find_element_by_css_selector('h1[data-qa=vacancy-title]')
            print(title.text)
            experience = driver.find_element_by_css_selector('span[data-qa=vacancy-experience')
            print('Опыт', experience.text)
            description = driver.find_element_by_css_selector('div[data-qa=vacancy-description')
            print(description.text)

            try:
                city = driver.find_element_by_css_selector('p[data-qa=vacancy-view-location]')
            except:
                city = driver.find_element_by_css_selector('span[data-qa=vacancy-view-raw-address]')

            print(city.text)
            money = driver.find_element_by_css_selector('span[data-qa=bloko-header-2]')
            print(money.text)
        except:
            # при исключении сохраняем страницу на которой возникла ошибка
            f = open('source_page_hh_ru.html', 'w')
            f.write(driver.page_source)
            f.close()


        # переключаемся на главное окно
        main_window = driver.window_handles[0]
        driver.switch_to.window(main_window)        

    

finally:
    # выполнится в любом случае
    time.sleep(1)
    driver.quit()