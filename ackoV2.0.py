import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.common.by import By
import time
import random
import string
import pprint
import csv
 
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# driver = webdriver.Chrome(options=chrome_options,executable_path=r"C:\webdrivers\chromedriver")
# driver.get('https://www.acko.com')

def calculatePolicy(car,pincode,input_reg_year,variant,fuel_type):

    try:
        error = False
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options,executable_path=r"C:\webdrivers\chromedriver")
        driver.get('https://www.acko.com')  

        info_dict = {
            'model' : '',
            'variant' : '',
            'type' : '',
            'Fuel Type':'',
            'pincode' : '',
            'previous_policy_expired' : '', 
            'policy_expiry_time' : '',
            'car_bought_year' : '',
            'car_bought_month' : '',
            'policy_claim_period' : '',
            'insured_price_value' : '',
            'premium_price':''
        }
        
        info_dict['type'] = 'private'
        info_dict['policy_expiry_time'] = 'None'

        time.sleep(2)
        view_prices_button = driver.find_element_by_link_text("Don't know your car number").click()

        time.sleep(2)
        car_model = driver.find_element_by_id('selectModelId')
        car_model.send_keys(car)

        time.sleep(1)
        select_car_model = driver.find_element_by_id('modelOption_0')
        info_dict['model'] = select_car_model.text
        select_car_model.click()

        if(fuel_type.lower() == 'petrol'):
            time.sleep(2)
            driver.find_element_by_id('fueltypeId0').click()

        else:
            time.sleep(2)
            driver.find_element_by_id('fueltypeId1').click()

        time.sleep(2)
        car_variant = driver.find_element_by_id('selectVariantId')
        car_variant.send_keys(variant)

        time.sleep(1)
        select_variant_option = driver.find_element_by_id('variantOption_0')
        info_dict['variant'] = select_variant_option.text
        select_variant_option.click()

        time.sleep(2)
        continue_button = driver.find_element_by_xpath('//*[@id="campaingnMMVContinueId"]')
        continue_button.click()

        time.sleep(2)
        private_car_button = driver.find_element_by_xpath('//*[@id="previousPolicyStausId_false"]').click()

        time.sleep(2)
        info_dict['pincode'] = pincode
        pin_input = driver.find_element_by_id('pinInputId')
        pin_input.send_keys(str(pincode))

        pin_continue = driver.find_element_by_xpath('//*[@id="pincodeContinueClickId"]').click()

        time.sleep(2)
        expired_button = driver.find_element_by_xpath('//*[@id="previousPolicyStausId_false"]').click()

        info_dict['previous_policy_expired'] = 'False'

        reg_year = getRegYear(input_reg_year)
        time.sleep(2)
        year_select = driver.find_element_by_id(reg_year)
        info_dict['car_bought_year'] = year_select.text
        year_select.click()

        time.sleep(2)
        month_select = driver.find_element_by_xpath('//*[@id="selectRegMonth_6"]')
        info_dict['car_bought_month'] = month_select.text
        month_select.click()

        time.sleep(2)
        claim_select = driver.find_element_by_xpath('//*[@id="lastclaimYear_2018"]')
        info_dict['policy_claim_period'] = claim_select.text
        claim_select.click()

        time.sleep(2)
        insured_value_price = driver.find_element_by_class_name('InsuredValuePrice').text
        info_dict['insured_price_value'] = insured_value_price
        
        premium_price = driver.find_element_by_class_name('CarPriceLabel').text
        info_dict['premium_price'] = premium_price
        
        info_dict['Fuel Type'] = fuel_type

        driver.quit()
        return [info_dict,error]
    
    except:
        error = True
        info_dict['model'] = car
        return [info_dict,error]

def getRegYear(year):
    reg_year = 'SelectRegYear_' + str(year)
    return reg_year

if __name__ == "__main__":

    input_file = csv.DictReader(open('./input-folder/Maruti_Borivali_Sample_Variant.csv'))

    with open("./output-folder/Maruti_Borivali_Sample_Variant_output.csv","w",newline='',encoding="utf-8") as f:
        field_names = ['model','variant','type','Fuel Type','pincode','previous_policy_expired','policy_expiry_time','car_bought_year','car_bought_month','policy_claim_period','insured_price_value','premium_price']
        writer = csv.DictWriter(f,fieldnames=field_names)
        writer.writeheader()

        for row in input_file:
            try:
                
                policy_information = calculatePolicy(row['model'],row['pincode'],row['reg_year'],row['variant'],row['Fuel Type'])
                if(policy_information[1] == True):
                    print("Error occured for Model : " + row['model'] + " , Variant : " + row['variant'])
                    writer.writerow(policy_information[0])
                    f.flush()
                else:
                    pprint.pprint(policy_information[0])
                    writer.writerow(policy_information[0])
                    f.flush()
            
            except Exception as ex:
                print("error in row")
                print(ex)
                continue


    

