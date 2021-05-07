from selenium import webdriver
import unittest
from selenium.webdriver import ActionChains
from time import sleep
from selenium.webdriver.common.keys import Keys

firstName = "Monika"
lastName = "Kowalska"
gender = "female"
countryCode = "+48"
phoneNumber = "516233576"
invalidEmail = "zdydbs.pl"
password = "Qwe231323sds"
selectedCountry = "PL"

class WizzairRegistration(unittest.TestCase):
    def setUp(self):
        # Analogia: warunki wstepne testow
        # Otwarcie przegladarki
        self.driver = webdriver.Chrome(executable_path=r'D:\chromdriver\chromedriver.exe')
        self.driver.get("https://wizzair.com/pl-pl#/")
        self.driver.maximize_window()
        self.driver.implicitly_wait(60)

    def tearDown(self):
        # Zamkniecie przegladarki
        self.driver.quit()

    # Metoda testowa - koniecznie 'test' na poczatku
    def testInvalidEmail(self):
        driver = self.driver
        # 1. Kliknij ,,Zaloguj sie"
        # CSS  SELECTOR SKOPIOWANY
        # #app > div > header > div.header__inner > div > nav > ul > li:nth-child(6) > button
        # XPATH SKOPIOWANY:
        # //*[@id="app"]/div/header/div[1]/div/nav/ul/li[6]/button
        # FULL XPATH SKOPIOWANY
        # /html/body/div[2]/div/header/div[1]/div/nav/ul/li[6]/button
        # NASZ CSS SELECTOR
        # button[data-test="navigation-menu-signin"]
        # NASZ XPATH
        # //button[@data-test="navigation-menu-signin"]

        zaloguj_brn = driver.find_element_by_xpath('//button[@data-test="navigation-menu-signin"]')
        # zaloguj_brn = driver.find_element_by_xpath(//*[@id="app"]/div/header/div[1]/div/nav/ul/li[6]/button)
        zaloguj_brn.click()
        # 2. Kliknij „Rejestracja”
        zaloguj_brn = driver.find_element_by_xpath('//button[@data-test="registration"]')
        zaloguj_brn.click()
        # 3. Wpisz imię
        name_input = driver.find_element_by_name('firstName')
        name_input.send_keys(firstName)
        # 4. Wpisz nazwisko
        surname_input = driver.find_element_by_name('lastName')
        surname_input.send_keys(lastName)
        # 5. Wybierz płeć
        if gender == "female":
            driver.find_element_by_xpath('//label[@data-test="register-genderfemale"]').click()
        else:
            name_input.click()
            driver.find_element_by_xpath('//label[@data-test="register-gendermale"]').click()
        # 6. Wpisz kod kraju
        country_code = driver.find_element_by_xpath('//div[@data-test="booking-register-country-code"]').click()
        country_code = driver.find_element_by_name('phone-number-country-code').send_keys(countryCode + Keys.RETURN)
        # 7. Wpisz numer telefonu
        phone_number = driver.find_element_by_xpath('//input[@data-test="check-in-step-contact-phone-number"]')
        phone_number.send_keys(phoneNumber)
        # 8. Wpisz niepoprawny e-mail (brak znaku „@”)
        email_input = driver.find_element_by_xpath('//input[@data-test="booking-register-email"]')
        email_input.send_keys(invalidEmail)
        # 9. Wpisz hasło
        password_input = driver.find_element_by_css_selector('input[data-test="booking-register-password"]')
        password_input.send_keys(password)
        # 10. Wybierz narodowość
        country_select = driver.find_element_by_xpath('//input[@data-test="booking-register-country"]').click()
        # Wyszukaj kraje
        country_container = driver.find_element_by_xpath('//div[@class="register-form__country-container__locations"]')
        countries = country_container.find_elements_by_tag_name("label")
        for country in countries:
            option = country.find_element_by_tag_name('small')
            if option.get_attribute("innerText") == selectedCountry:
                # Przwijam do tego elementu
                option.location_once_scrolled_into_view
                # klikam
                option.click()
                # Opuszczam pętle
                break

        ### UWAGA! TUTAJ BĘDZIE TEST: SPRAWDZAMY OCZEKIWANY REZULTAT!!! ###
        # Wyszukuje wszystkie błedy
        error_notices = driver.find_elements_by_xpath('//span[@class="input-error__message"]/span')
        # Pusta lista na widoczne błedy
        visible_error_notices = []
        # Zapisuje widoczne błedy do listy visible_error_notices
        for error in error_notices:
            if error.is_displayed():
                visible_error_notices.append(error)
        # Sprawdzam czy widoczny jest tylko jeden bład
        # czysty python
        assert len(visible_error_notices) == 1
        # Sprawdzam tresć widocznego błędu
        assert visible_error_notices[0].text == "Nieprawidłowy adres e-mail"


        # Spij 3 sekundy bym zobaczyl o sie dzieje
        sleep(5)

if __name__ == "__main__":
    unittest.main(verbosity=2)