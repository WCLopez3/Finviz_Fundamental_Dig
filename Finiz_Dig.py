from tkinter import *
from tkinter import scrolledtext
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime


def finviz_open(event=None):
    # Initialize the Chrome Driver
    s = Service(r'C:\Users\wclop\PycharmProjects\chromedriver.exe')
    driver = webdriver.Chrome(service=s)
    driver.minimize_window()
    driver.get('https://finviz.com/')

    # Searching for the input box for finviz.com
    search_box = driver.find_element(By.XPATH, '//*[@id="search"]/div/form/input')
    search_box.send_keys(ticker_entry.get())
    search_box.send_keys(Keys.RETURN)

    try:
        # Waiting for the table to appear 
        snapshot = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'snapshot-table2')))
        marketcap = snapshot.find_element(By.XPATH, '/html/body/div[4]/div/table[2]/tbody/tr[2]/td[2]/b').text
        shrsfloat = snapshot.find_element(By.XPATH,'/html/body/div[4]/div/table[2]/tbody/tr[2]/td[10]/b').text
        ss = snapshot.find_element(By.XPATH, '/html/body/div[4]/div/table[2]/tbody/tr[3]/td[10]/b').text
        avgvol = snapshot.find_element(By.XPATH, '/html/body/div[4]/div/table[2]/tbody/tr[11]/td[10]/b').text
        instown = snapshot.find_element(By.XPATH, '/html/body/div[4]/div/table[2]/tbody/tr[3]/td[8]/b').text
        prevclose = snapshot.find_element(By.XPATH, '/html/body/div[4]/div/table[2]/tbody/tr[11]/td[12]/b').text
        time.sleep(2)
        SSR = float(prevclose) * .9
        time.sleep(1)

        # Date and Time format M/D/YYYY H:M:S
        now = datetime.now()
        date_string = now.strftime("%m/%d/%y %H:%M:%S")
        #print(date_string)


        # Creating a Python dictionary
        data = {'': [date_string, marketcap, shrsfloat, instown, ss, avgvol, prevclose, SSR],

                }
        # Creating the dataframe of above data
        df = pd.DataFrame(data)
        df.index = [ticker_entry.get(), 'Market Cap:', 'Shrs Float:', 'Inst Own:', 'Short Float', 'Avg Volume:', 'Prev Close:', 'SSR:']
        #df.index.name = ticker_entry.get()
        df_str = str(df)
        txtbox.insert(0.0, df_str)
        
        # Append data frame to CSV file
        df.to_csv('fundies.csv', mode='a')
        
        print(df)
        time.sleep(1)

    finally:
        driver.quit()



# Tkinter Windows
master_window = Tk()
master_window.title('The Dream')
master_window.geometry('300x500')

# Auto Cap
def caps(event):
    v.set(v.get().upper())
# Deletes Ticker
def del_entry(event):
    ticker_entry.delete(0, END)

buttons_frame = Frame(master_window)
buttons_frame.grid(row=0, column=0, sticky=W+E)

# Search Button
search_but = Button(buttons_frame, text='Search', command = finviz_open)
search_but.grid(row=0, column=1)

# Input box for the Ticker
v = StringVar()
ticker_entry = Entry(buttons_frame, textvariable=v)
ticker_entry.grid(row = 0, column = 0, padx = 10, pady = 10)
ticker_entry.insert(0, 'Search Ticker')
ticker_entry.bind('<Button-1>', del_entry)
ticker_entry.bind('<KeyRelease>', caps)
ticker_entry.bind('<Return>', finviz_open)

# WindowFrame 
group1 = LabelFrame(master_window, text=" The Process ", padx=5, pady=5)
group1.grid(row=1, column=0, columnspan=3, padx=2, pady=0, sticky=E+W+N+S)

master_window.columnconfigure(0, weight=1)
master_window.rowconfigure(1, weight=1)

group1.rowconfigure(0, weight=1)
group1.columnconfigure(0, weight=1)

# Create the textbox
txtbox = scrolledtext.ScrolledText(group1, width=40, height=10,)
txtbox.grid(row=0, column=0,   sticky=E+W+N+S)
mainloop()
