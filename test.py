# from collections import OrderedDict
import heapq

import time
start_time = time.time()



def heapPop(orderid,book):          #removes and element from heap and heapifies it
    # myidorder = orderid
    # index = book.index(orderid)
    # print(orderid +" ========= ")
    # print(book)
    book.remove(orderid)
    
    heapq.heapify(book)
    

    return book
    # Book.(book_type) = book

#created a class Book for our OrderBooks
class Book:
    buy_book = []
    sell_book = []

    def __init__(self):
        self.buy_book = []
        self.sell_book = []
    


    #method to print or ORderBOok
    def print_book(self,book_id):
        first = "           Buy  -  Sell          \n"
        second = "====================================\n"
        buy_bk = Book.buy_book
        sell_bk = Book.sell_book
        # temp_lst = [heapq.heappop(buy_bk) for i in range(len(buy_bk))]
        # print(temp_lst)
        len_bk = 0
        # small_bk = []
        if(len(buy_bk) > len(sell_bk)):
            len_bk = len(buy_bk)
            # small_bk = sell_bk
        else:
            len_bk = len(sell_bk)

        finalstr = first + second
        for i in range(len_bk):
            buy_str = ""
            if(i < len(buy_bk)):
                buy_str = str(buy_bk[i][1])+"@"+str(buy_bk[i][0])
                # print(buy_str)

            sell_str = ""
            if(i < len(sell_bk)):
                sell_str = str(sell_bk[i][1])+"@"+str(sell_bk[i][0])

            finalstr  += buy_str + "  --  " + sell_str +"\n"
        
        text_file = open(book_id+"_results.txt", "w")
 
        #write string to file
        text_file.write(finalstr)
        
        #close file
        text_file.close()
        print(finalstr)


    # method to delete an order. compares both buy_book and sell_book of an OrderBook to find the order with orderid. Removes the order and heapifies the respective buy/sell book
    def delete_order(self,order_id):
        
        sell_bk = Book.sell_book
        myidorder = [elem for elem in sell_bk if (elem[2] == order_id)]
        if(len(myidorder) > 0 ):
            
            myidorder = myidorder[0]
            index = sell_bk.index(myidorder)
            sell_bk.remove(myidorder)
            heapq.heapify(sell_bk)
            Book.sell_book = sell_bk
            # heapq.heappop(Book.sell_book,myidorder)
        
        buy_bk = Book.buy_book
        myidorder = [elem for elem in buy_bk if (elem[2] == order_id)]
        if(len(myidorder) > 0 ):
            myidorder = myidorder[0]
            index = buy_bk.index(myidorder)
            buy_bk.remove(myidorder)
            heapq.heapify(buy_bk)
            Book.buy_book = buy_bk
        

        temp_buy = Book.buy_book
        Book.buy_book = heapq.heapify(temp_buy)
        temp_sell = Book.sell_book
        Book.sell_book = heapq.heapify(temp_sell)
        
        return -1
        

    # @classmethod
    def process_order(self,order_type , order_vol , order_price, order_id):  #Method to process the order
        order_vol = int(order_vol)
        order_price = float(order_price)
        if(order_type == 'buy'):
            sell_heap = Book.sell_book #retrieve the Sell order book to find comparable orders
            # print(sell_heap)
            i = 0
            if(len(sell_heap) == 0): # if no order in sell book then simply add buy order to buy book
                heapq.heappush(Book.buy_book,((-1)*order_price,order_vol,order_id))
                # print(Book.buy_book)
                return -1

            if(sell_heap[i][0] > order_price): #if first order of sell book has greater price than buy order price then simple add the buy oreder to buy book
                heapq.heappush(Book.buy_book,((-1)*order_price,order_vol,order_id))
                return -1
            buy_vol = order_vol
        

           

            while(i <= len(sell_heap) and sell_heap[i][0] <= order_price and buy_vol > 0 ): # starting from top most order in sell book and compares the price of sell vs buy order and goes untill the end of the list 
                                                                                            # or till the sell price < buy price and buy volume is greater than 0
                sell_price = sell_heap[i][0]
                sell_vol = sell_heap[i][1]
                sell_id = sell_heap[i][2]
                sell_old = sell_heap[i]


                # if(sell_price == order_price):
                #     loc_sel_price = sell_price
                    # while(i <= len(sell_heap) and sell_price == order_price):

                # print(str(sell_old) + "----------------------------5")
                if(sell_vol > buy_vol): # if the sell orderhas more volume thaan buy order just updates the remaining sell volume with orderid and buy order gets executed.
                    
                    Book.sell_book = heapPop(sell_old,sell_heap)
                    # heapq.heappop(Book.sell_book,(sell_price,sell_vol,sell_id))
                    heapq.heappush(Book.sell_book,(sell_price,sell_vol-buy_vol,sell_id))
                    # temp_buy = Book.buy_book
                    # Book.buy_book = heapq.heapify(temp_buy)
                    # temp_sell = Book.sell_book
                    # Book.sell_book = heapq.heapify(temp_sell)
                else:                                  # if sell vol is lower than buy vol than remove sell order from sell book and move on
                    # heapPop(sell_old,sell_heap)
                    Book.sell_book = heapPop(sell_old,sell_heap) 
                    # temp_buy = Book.buy_book
                    # Book.buy_book = heapq.heapify(temp_buy)
                    # temp_sell = Book.sell_book
                    # Book.sell_book = heapq.heapify(temp_sell)
                    # heapq.heappop(Book.sell_book,(sell_price,sell_vol,sell_id))
                
                
                buy_vol -= sell_vol # updates buy volume. if it goes negative or zero the loop stop
                i += 1

            if(buy_vol > 0):
                heapq.heappush(Book.buy_book,(-1*order_price,buy_vol,order_id))
                temp_buy = Book.buy_book
                Book.buy_book = heapq.heapify(temp_buy)
                temp_sell = Book.sell_book
                Book.sell_book = heapq.heapify(temp_sell)

            
            
            temp_buy = Book.buy_book
            Book.buy_book = heapq.heapify(temp_buy)
            temp_sell = Book.sell_book
            Book.sell_book = heapq.heapify(temp_sell)

        elif(order_type == 'sell'): # the lOGIC behind sell process is more or less same as behind the buy process. THe minor difference is that to sort the buy book in descending manner 
                                    # i multiply the orderprice with -1 and then the heap keeps the largest buy price at the top
            buy_heap = Book.buy_book
            # print(buy_heap)
            # print(Book.sell_book)

            j = len(buy_heap) - 1
            if(len(buy_heap) == 0):
                heapq.heappush(Book.sell_book,(order_price,order_vol,order_id))
                return -1

            if(buy_heap[j][0] < order_price):
                heapq.heappush(Book.sell_book,(order_price,order_vol,order_id))
                return -1
                # print(Book.sell_book)
            
            sell_vol = order_vol

            j = 0

            while(j < len(buy_heap)  and buy_heap[j][0]*(-1) >= order_price and sell_vol > 0):
                buy_price = buy_heap[j][0]*(-1)
                buy_vol = buy_heap[j][1]
                buy_id = buy_heap[j][2]
                buy_old = buy_heap[j]
                if(buy_vol > order_vol):
                    # heapPop(buy_old,buy_heap)
                    Book.buy_book = heapPop(buy_old,buy_heap)
                    # heapq.heappop(Book.buy_book,(buy_price,buy_vol,buy_id))
                    heapq.heappush(Book.buy_book,((-1)*buy_price,buy_vol - order_vol,buy_id))
                else:
                    # heapPop(buy_old,buy_heap)
                    Book.buy_book = heapPop(buy_old,buy_heap)
                    # heapq.heappop(Book.buy_book,(buy_price,buy_vol,buy_id))


                sell_vol -= buy_vol
                j += 1 
            

            if(sell_vol > 0 ):
                heapq.heappush(Book.sell_book,(order_price,sell_vol,order_id))
            

            temp_buy = Book.buy_book
            Book.buy_book = heapq.heapify(temp_buy)
            temp_sell = Book.sell_book
            Book.sell_book = heapq.heapify(temp_sell)

            
      

            
# from bs4 import BeautifulSoup 

# # Reading the data inside the xml file to a variable under the name  data
# with open('orders.xml', 'r') as f:
#     data = f.read() 
# bs_data = BeautifulSoup(data, features="xml")
# messages =   bs_data.find_all('AddOrder')   

import xml.etree.ElementTree as ET 

# Pass the path of the xml document 
tree = ET.parse('sample.xml') 

# get the parent tag 
root = tree.getroot() 

# print the root (parent) tag along with its memory location 
# print(root) 

# # print the attributes of the first tag  
# print(root[0].attrib)
# quit()
my_books = {} # dictionary to keep track of books
for msg in root: #reads the XML file line by line
    tagname = msg.tag
    # print(tagname)
    if(tagname == 'DeleteOrder'):
        msg = msg.attrib
        book_name = str(msg["book"])
        order_id = str(msg["orderId"])
        # print(order_id)
        temp_book = my_books[book_name]
        temp_book.delete_order(order_id)
    else:

        msg = msg.attrib
        book_name = str(msg["book"])
        order_t = str(msg["operation"]).lower()
        order_p = str(msg["price"])
        order_v = str(msg["volume"])
        order_id = str(msg["orderId"])
        # print(order_id)
        # print(order_id)
        # print(order_t)
        # print(order_p)
        # print(order_v)
        
        if book_name in my_books.keys():
            temp_book = my_books[book_name]
            temp_book.process_order(order_t,order_v,order_p,order_id)
            my_books[book_name] = temp_book
        else:
            loc_book  = Book()
            loc_book.process_order(order_t,order_v,order_p,order_id)
            my_books[book_name] = loc_book



for key,val in my_books.items():
    print("------------------------------------" + key + "------------------------------")
    print(val.print_book(key))
    # print("------------------------------------" + key + "------------------------------")


print("--- %s seconds ---" % (time.time() - start_time))










        