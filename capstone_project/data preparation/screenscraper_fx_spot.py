__author__ = 'kai.aeberli'

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys
import itertools
from collections import OrderedDict
import sys
import pandas as pd
import pymongo
import json, os


def Webscraping():


    webstr = "http://www.histdata.com/download-free-forex-historical-data/?/ascii/tick-data-quotes/EURUSD"
    driver.get(webstr)


    # get all hrefs that contain "historical"
    from selenium.webdriver.common.by import By
    all_links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="eurusd"')

    listHref = []
    for link in all_links:
        #print(link.get_attribute("href"))
        listHref.append(link.get_attribute("href"))

    # travel down each of them
    listHRefMonth = []
    # append months to each of them
    for strLink in listHref:
        for month in range(12):
            listHRefMonth.append(strLink + '/' + str(month+1))



    #liElements=driver.find_element_by_id("listed-islamic-securities").find_element_by_class_name("listed-securities").find_elements_by_xpath(".//li")
    #lisElementsDeep = liElements.copy()




    # listHref = []
    # for li in lisElementsDeep:
    #     href = li.find_element_by_tag_name("a").get_attribute("href")
    #     listHref.append(href)


    all_values = []
    for href in listHRefMonth[1:]:

        try:


            driver.get(href)
            import time
            time.sleep(2)  # give time to load - need this else animations are still running

            zip_file = driver.find_element(By.CSS_SELECTOR, 'a[id="a_file"')
            zip_file.click()


            # go through months
            #each_year_month_links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="eurusd"')

            # securityTable = driver.find_element_by_id("currencies-all").find_element_by_tag_name("tbody").find_elements_by_xpath(".//tr")
            #
            # #dailyValues = []
            #
            # for htmlRow in securityTable:
            #     #if len(htmlRow.find_elements(By.XPATH, "th")) == 0:
            #
            #     # read out all the td elements - each is one column of that row
            #
            #     # can i do it in one go???
            #     #htmlRow.find_elements(By.CSS_SELECTOR, "td")[2].text but each needs special treatment
            #     row = OrderedDict()
            #     row["Link"] = href
            #     row["hash"] = htmlRow.find_element_by_xpath("td[1]").text # #
            #     row["name"] = htmlRow.find_element_by_xpath("td[2]").find_element_by_tag_name('a').text # name
            #     row["symbol"] = htmlRow.find_element_by_xpath("td[3]").text # symbol
            #     row["market_cap"] = htmlRow.find_element_by_xpath("td[4]").get_attribute("data-usd") # market cap
            #     row["price"] = htmlRow.find_element_by_xpath("td[5]").find_element_by_tag_name("a").get_attribute("data-usd") # price
            #     row["available_supply"] = htmlRow.find_element_by_xpath("td[6]").text # available supply
            #     row["volume_24h"] = htmlRow.find_element_by_xpath("td[7]").find_element_by_tag_name("a").text  # low vol???
            #     row["percent_change_1h"] = htmlRow.find_element_by_xpath("td[8]").get_attribute("data-usd") # % 1h
            #     row["percent_change_24h"] = htmlRow.find_element_by_xpath("td[9]").text # % 24h
            #     row["percent_change_7d"] = htmlRow.find_element_by_xpath("td[10]").text  # % 7d
            #     row["date"] = href[-9:-1]
            #
            #     all_values.append(row)


            #all_values.append(dailyValues)

        except:
            print("exc")




    return all_values


def zip_extract(path):


    import zipfile
    archive = zipfile.ZipFile(path)
    archive.extractall()





def get_zipfiles():

    global driver
    #driver=webdriver.Firefox()
    chromedriver_path = os.path.dirname(__file__)
    driver=webdriver.Chrome(chromedriver_path+"/chromedriver.exe")
    webstr = "http://www.histdata.com/download-free-forex-historical-data/?/ascii/tick-data-quotes/EURUSD"
    driver.get(webstr)

    import time
    time.sleep(15)

    listSecurities=Webscraping()

    import pandas as pd
    df = pd.DataFrame.from_records(listSecurities)
    df.to_csv("fx_spot_quotes.csv")

    for val in listSecurities:
        print(val)


    driver.quit()



def run_function_on_all_files_in_dir(file_ending, file_function, dir = None):

    if dir == None:
        foldername = os.path.join(os.path.dirname(__file__), "")
    for base, dirs, files in os.walk(foldername):
        for file in files:
            if file[-3:] == file_ending:
                longfilepath = os.path.join(base, file)
                #zip_extract(longfilepath)
                #import_content(longfilepath)
                print("Processing "+longfilepath)
                file_function(longfilepath)




def import_content(filepath):


    mng_client = pymongo.MongoClient('localhost', 27017)
    mng_db = mng_client['fx_prediction'] # Replace mongo db name
    collection_name = 'fx_tick_data_typed' # Replace mongo db table name
    db_cm = mng_db[collection_name]

    data = pd.read_csv(filepath)

    data.columns = ["date", "bid", "ask", "vol"]
    #data.date = pd.to_datetime(data.date, format='%Y%m%d %H%M%S%f')
    data.bid = data.bid.astype(float)
    data.ask = data.ask.astype(float)
    data.vol = data.vol.astype(float)
    import datetime
    data_json = json.loads(data.to_json(orient='records'))
    for row in data_json:
        row["date"] = datetime.datetime.strptime(row['date'], '%Y%m%d %H%M%S%f')

    #db_cm.remove()
    db_cm.insert_many(data_json)


def main():
    #get_zipfiles() # goes to default download folder
    #run_function_on_all_files_in_dir("zip", zip_extract)
    run_function_on_all_files_in_dir("csv", import_content)
    pass

if __name__ == '__main__':
    main()