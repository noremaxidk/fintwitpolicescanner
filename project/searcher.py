from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from sheet_reader import fintwit_police_scanner

#locates chromedriver.exe on the computer and opens the application
driver = webdriver.Chrome(executable_path=r'C:path\to\chomedriver.exe')

#sends a request to open this URL on the browser
driver.get('https://www.sec.gov/edgar/search/')
time.sleep(0.1)

#clicks the "more search options" button
more_search_options = driver.find_element_by_id('show-full-search-form')
more_search_options.click()
time.sleep(1)

#mimics highlighting the date that is in the box and then replaces it with the date select (must include the hyphens)
replace_text_from = driver.find_element_by_id('date-from');
replace_text_from.send_keys(Keys.CONTROL + "a")
replace_text_from.send_keys('2020-12-01')

#because of the calendar feature you have to mimic pressing enter so that it goes away and you can hit the search button that is in the for loop below
date_picker_day = driver.find_element_by_class_name('ui-state-default.ui-state-active')
date_picker_day.send_keys(Keys.ENTER)
time.sleep(0.1)

#enters the type of filings that you want
filing_drop_down = driver.find_element_by_id('category-select')
filing_drop_down.send_keys(Keys.ENTER)
time.sleep(0.5)

enter_the_filing_types = driver.find_element_by_xpath("//*[@id='category-type-grp']/ul/li[13]")
enter_the_filing_types.click()
time.sleep(0.3)

filing_types = driver.find_element_by_id('filing-types')
filing_types.send_keys('10-K, 10-Q, 8-K, 6-K, 20-F')

#for loop that cycles through the names in the excel file
for index, column in fintwit_police_scanner.iterrows():
    input_the_name = driver.find_element_by_class_name('company.form-control.border-onfocus.hide-on-short-form.text-black')
    input_the_name.send_keys(column['Name'])
    time.sleep(0.1)

    please_just_search = driver.find_element_by_class_name('btn.border-onfocus')
    please_just_search.submit()
    time.sleep(0.5)

    check_for_no_search_pls = driver.find_element_by_class_name('text-center')
    time.sleep(0.1)

    if check_for_no_search_pls.text == "No results found for your search!":
        print(column['Name'], "NULL")

    else:
        company_name = driver.find_element_by_xpath("//*[@id='hits']/table/tbody/tr[1]/td[4]")
        print(column['Name'], company_name.text)

    input_the_name.clear()

    time.sleep(0.5)
