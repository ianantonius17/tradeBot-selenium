from time import sleep
import copy
class analysis():
    p = 0
    t = 0
    cur_time = 0
    start_price = 0
    prev_price = 0
    cur_price = 0
    def __init__(self):
        p = 0
        t = 0
    
    def decide(self,price,time):

        print('decides()')
        
        up = 0
        down = 0
        cur_time = int(time.get_attribute("innerHTML")[3:5])
        prev_price = float(price.get_attribute("innerHTML"))

        print('curtime: ',cur_time,' prev_price: ',prev_price)
        while(cur_time > 0):
            sleep(1)
            cur_price = float(price.get_attribute("innerHTML"))
            #down
            if(prev_price < cur_price):
                up += 1
                print('up')
            #up
            elif(prev_price > cur_price):
                down += 1
                print('down')
            
            prev_price = copy.deepcopy(cur_price)
            cur_time = int(time.get_attribute("innerHTML")[3:5])


        if(up > down):
            return 1
        elif(down > up):
            return -1
        else:
            return 0

        

