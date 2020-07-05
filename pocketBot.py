from selenium import webdriver
from time import sleep
import copy
from credentials import user_email,user_pwd
import analize
class pocketBot():
    buy = 0
    sell = 0
    

    def __init__(self):
        self.driver = webdriver.Chrome()
        sleep(5)
        self.driver.get('https://pocketoption.com/en/login')
    
    #google login
    def google_login(self):
        #login_btn = self.driver.find_element_by_xpath('/html/body/div[2]/div/div/a[3]')
        #login_btn.click()
        sleep(2)
        google_sign_in = self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/div/div[3]/form/div[5]/div[1]/a[2]')
        google_sign_in.click()

        sleep(3)
        email = self.driver.find_element_by_xpath('//*[@id="identifierId"]')
        email.send_keys(user_email)

        sleep(3)
        next = self.driver.find_element_by_xpath('//*[@id="identifierNext"]')
        next.click()

        sleep(3)
        pwd = self.driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
        pwd.send_keys(user_pwd)

        sleep(3)
        next =self.driver.find_element_by_xpath('//*[@id="passwordNext"]')
        next.click()

    # select gold commodities
    def selectGold(self):
        rotate = self.driver.find_element_by_xpath('//*[@id="bar-chart"]/div/div/div[1]/div/div[1]/div[1]/div/a/div/i')
        rotate.click()

        commodities = self.driver.find_element_by_xpath('//*[@id="quotes-list"]/div[1]/ul/li[5]')
        commodities.click()

        gold = self.driver.find_element_by_xpath('//*[@id="quotes-list"]/div[2]/div[1]/div/div[2]/div[2]/a')
        gold.click()
        
        close = self.driver.find_element_by_xpath('//*[@id="modal-root"]/div[7]')
        close.click()
    
    def selectAppleStock(self):
        rotate = self.driver.find_element_by_xpath('//*[@id="bar-chart"]/div/div/div[1]/div/div[1]/div[1]/div/a/div/i')
        rotate.click()

        stock = self.driver.find_element_by_xpath('////*[@id="quotes-list"]/div[1]/ul/li[6]')
        stock.click()

        apple = self.driver.find_element_by_xpath('//*[@id="quotes-list"]/div[2]/div[1]/div/div[1]/div[1]')
        apple.click()

        close = self.driver.find_element_by_xpath('//*[@id="modal-root"]/div[7]')
        close.click()

    #buy higher price
    def buyHigherButton(self):
        return self.driver.find_element_by_xpath('//*[@id="put-call-buttons-chart-1"]/div/div[5]/a')
        #buy.click()

    # buy lower price
    def buyLowerButton(self):
        
        return self.driver.find_element_by_xpath('//*[@id="put-call-buttons-chart-1"]/div/div[1]/a')
        #sell.click()

    #get current second
    def getCurrentSecond(self):
        time = self.driver.find_element_by_xpath('//*[@id="put-call-buttons-chart-1"]/div/div[2]/div[2]/div/div[1]/div/div[2]')
        #get current time (in M1)
        time_number = time.get_attribute("innerHTML")
        time_number = time_number[3:5]
        time_value = int(time_number)
        return time_value

    #get current price
    def getCurrentPrice(self):
        price = self.driver.find_element_by_xpath('//*[@id="put-call-buttons-chart-1"]/div/div[4]/div[2]/div/div[1]/div')
        price_number = price.get_attribute("innerHTML")
        price_value = float(price_number)
        return price_value

    #get current money
    def getCurrentMoney(self):
        money = self.driver.find_element_by_xpath('/html/body/div[4]/div[1]/header/div[2]/div[2]/div[1]/a/span')
        money_number = money.get_attribute("innerHTML")
        money_value = float(money_number)
        return money_value

    #check if there is active trade
    def isActiveTrade(self):

        trade = 0
        try:
            trade = self.driver.find_element_by_xpath('//*[@id="bar-chart"]/div/div/div[2]/div/div[2]/div/div[3]')
        except:
            trade = 0

        if(trade == 0):
            return False
        
        return True
        

#fix timing 
#always start analyize at s = 10 to s = 0
    def run(self):
        #bot = pocketBot()
        analitic = analize.analysis()
        self.google_login()
        print('login')
        sleep(10)

        self.selectGold()
        #self.selectAppleStock()
        print('select commodities')
        sleep(5)
        cur_sec = self.getCurrentSecond()
        cur_money = self.getCurrentMoney()

        #flexible limit
        min_money = cur_money - cur_money*0.1
        max_money = cur_money + cur_money*0.2

        while(cur_money <= max_money and cur_money > min_money or self.isActiveTrade() == True):
            print('trade start')
            if(cur_money > max_money or cur_money <= min_money):
                print('money is over limit')
                sleep(2)
                continue
            cur_sec = self.getCurrentSecond()
            print('cur_sec:',cur_sec)
            if(cur_sec > 30):
                sleep(cur_sec - 30)
                cur_sec = self.getCurrentSecond()            

            #fix time until it goes to between 30 - 10 before sleep
            #7 second analysis
            if(cur_sec > 7 and cur_sec <= 30):
                sleep(cur_sec-7)
            time = self.driver.find_element_by_xpath('//*[@id="put-call-buttons-chart-1"]/div/div[2]/div[2]/div/div[1]/div/div[2]')
            price = self.driver.find_element_by_xpath('//*[@id="put-call-buttons-chart-1"]/div/div[4]/div[2]/div/div[1]/div')
            decision = analitic.decide(price,time)
            print('done analyze, decision = ', decision)
            sleep(1)
            if(decision == 0): continue
            buy = self.buyHigherButton()
            sell = self.buyLowerButton()
            
            cur_sec = self.getCurrentSecond()
            cur_price = self.getCurrentPrice()
            #prev_price = self.getCurrentPrice()
            lowest_price = self.getCurrentPrice()
            highest_price = self.getCurrentPrice()
            transaction = 0
            print('cur sec: ',cur_sec,'cur_price: ' ,cur_price)
            
            while(cur_sec > 30 and transaction < 5 ):
                
                if(decision == 1):
                    if(transaction == 0):
                        buy.click()
                        lowest_price = copy.deepcopy(cur_price)
                        transaction += 1
                        print('buy')
                    if(cur_price < lowest_price):
                        buy.click()
                        lowest_price = copy.deepcopy(cur_price)
                        transaction += 1
                        print('buy')
                
                if(decision == -1):
                    if(transaction == 0):
                        sell.click()
                        highest_price = copy.deepcopy(cur_price)
                        transaction += 1
                        print('sell')

                    if(cur_price > highest_price):
                        sell.click()
                        highest_price = copy.deepcopy(cur_price)
                        transaction += 1
                        print('sell')
                
                #prev_price = cur_price
                sleep(0.8)
                cur_sec = self.getCurrentSecond()
                cur_price = self.getCurrentPrice()

            print("out of buying phase")    
    


bot = pocketBot()
bot.run()
            
print("done")



            





