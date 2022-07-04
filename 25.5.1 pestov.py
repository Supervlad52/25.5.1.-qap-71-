import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('D:\programs\chromedriver.exe')
    pytest.driver.set_window_size(1024, 600)
    pytest.driver.maximize_window()
    # Переходим на страницу авторизации
    pytest.driver.get('https://petfriends.skillfactory.ru/login')
    # Вводим email
    pytest.driver.find_element_by_id('email').send_keys('vlad-pestov@mail.ru')
    # Вводим пароль
    pytest.driver.find_element_by_id('pass').send_keys('123123')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    # Нажимаем на ссылку "Мои питомцы"
    WebDriverWait(pytest.driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a.nav-link[href="/my_pets"]'))
        )
    pytest.driver.find_element_by_css_selector('a.nav-link[href="/my_pets"]').click()
    # Проверяем, что мы оказались на страницы "Мои питомцы"
    assert pytest.driver.current_url == 'https://petfriends.skillfactory.ru/my_pets'
    yield
    pytest.driver.quit()


# Проверка карточек "Мои питомцы"
def test_my_pets():
    pytest.driver.implicitly_wait(10)
    images = pytest.driver.find_elements_by_css_selector('.card-deck .card-img-top')
    names = pytest.driver.find_elements_by_css_selector('.card-deck .card-tittle')
    descriptions = pytest.driver.find_elements_by_css_selector('.card-deck .card-text')
    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0


# проверяем присутствие всех питомцев
def test_count_of_pets():
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".\\.col-sm-4.left")))
    # элементы статистики
    statistic = pytest.driver.find_elements_by_css_selector(".\\.col-sm-4.left")
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))
    # элементы карточек
    pets = pytest.driver.find_elements_by_css_selector('.table.table-hover tbody tr')
    # количество из статистики
    count_stats = statistic[0].text.split('\n')
    count_stats = count_stats[1].split(' ')
    count_stats = int(count_stats[1])
    # количество карточек
    count_cards = len(pets)
    assert count_stats == count_cards


# проверяем присутствие не менее половины фото
def test_count_of_foto():
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".\\.col-sm-4.left")))
    # элементы статистики
    statistic = pytest.driver.find_elements_by_css_selector(".\\.col-sm-4.left")
    # элементы с фото
    images = pytest.driver.find_elements_by_css_selector('.table.table-hover img')
    # количество из статистики
    count_stats = statistic[0].text.split('\n')
    count_stats = count_stats[1].split(' ')
    count_stats = int(count_stats[1])
    # количество фото
    count_cards_with_foto = 0
    for i in range(len(images)):
        if images[i].get_attribute('src') != '':
            count_cards_with_foto += 1
    assert count_cards_with_foto >= count_stats/2


# проверяем разноименность
def test_any_names():
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))
    data = pytest.driver.find_elements_by_css_selector('.table.table-hover tbody tr')
    pets_name = []
    for i in range(len(data)):
        pets_name.append(data[i].text.replace('\n', '').split(' ')[0])
    pets_name_set = set(pets_name)
    assert len(pets_name) == len(pets_name_set)


# проверяем наличие имени, возраста и породы
def test_having_full_description():
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))
    data = pytest.driver.find_elements_by_css_selector('.table.table-hover tbody tr')
    for i in range(len(data)):
        assert len(data[i].text.replace('\n', '').split(' ')) == 3


# проверяем отсутствие повторяющихся питомцев
def test_any_pets():
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))
    data = pytest.driver.find_elements_by_css_selector('.table.table-hover tbody tr')
    data_list = []
    for i in range(len(data)):
        data_list.append(tuple(data[i].text.replace('\n', '').split(' ')))
    data_set = set(data_list)
    assert len(data_list) == len(data_set)