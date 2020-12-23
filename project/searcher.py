from tkinter import *
from tkinter.filedialog import askopenfilename
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

root = Tk()
root.geometry("500x500")
root.configure(background = "black")
root.title = ("FinTwit Police Scanner")

def buttonwidget():
    upload_button = Button(root, text="Upload", command=lambda:fintwitPoliceScanner())
    upload_button.pack(side=TOP, pady=10)

buttonwidget()

def fintwitPoliceScanner():
    file = askopenfilename(title = "Fintwit Police Scanner", filetypes = (("CSV Files","*.csv"),))
    fintwit_police_scanner = pd.read_csv(file)

    driver = webdriver.Chrome(executable_path=r'C:\Users\\Desktop\chromedriver.exe')
    driver.get('https://www.sec.gov/edgar/search/')
    time.sleep(0.1)

    more_search_options = driver.find_element_by_id('show-full-search-form')
    more_search_options.click()
    time.sleep(1)

    replace_text_from = driver.find_element_by_id('date-from');
    replace_text_from.send_keys(Keys.CONTROL + "a")
    replace_text_from.send_keys('2020-12-01')

    date_picker_day = driver.find_element_by_class_name('ui-state-default.ui-state-active')
    date_picker_day.send_keys(Keys.ENTER)
    time.sleep(0.1)

    filing_drop_down = driver.find_element_by_id('category-select')
    filing_drop_down.send_keys(Keys.ENTER)
    time.sleep(0.5)

    enter_the_filing_types = driver.find_element_by_xpath("//*[@id='category-type-grp']/ul/li[13]")
    enter_the_filing_types.click()
    time.sleep(0.3)

    filing_types = driver.find_element_by_id('filing-types')
    filing_types.send_keys('10-K, 10-Q, 8-K, 6-K, 20-F')

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
            pass

        else:
            company_name = driver.find_element_by_xpath("//*[@id='hits']/table/tbody/tr[1]/td[4]")
            print(column['Name'], company_name.text)

    time.sleep(0.5)

fintwitPoliceScanner()

root.mainloop()
