from bs4 import BeautifulSoup
from datetime import datetime
from colorama import init, Fore,Back
from matplotlib import pyplot as plt
import requests
import os

init() # FOR COLARAMA TO WORK

product_names = []
product_prices = [] #holds the string value of prices from ebay
proper_price = [] #proper price holds the numerical value for the prices
rating = []
extra_info = [] #extra info about product, whether it is on sale, or free international shipping etc etc
links = [] # holds links to the products loaded in
find = ""

'''

This function allows users to enter a product and how many items of that product do
they want to search, it then uses bs4 beautifulsoup API to scrape info from ebay
and loads the information into list.

Note: the search limit for number of items is 192 items

'''

def Ebay_read_in():
    global find

    find = input("Enter a Product: ")
    find = find.lower().replace(" ","")
    num_products = input("How many products do you want to search: ")

    Site_url = "https://www.ebay.com/sch/i.html?_from=R40&_nkw="+ find +"&_sacat=0&rt=nc&LH_BIN=1&_ipg=192"
    print("WEBLINK: "+ Site_url)
    web = requests.get(Site_url).content
    soup = BeautifulSoup(web,'lxml')
    container = soup.find_all("div",{"class":"s-item__wrapper clearfix"})
    
    Running = int(num_products)
    
    if(len(container) < Running):
        Running = len(container)

    if(int(num_products) > len(container)):
        Running = len(container) - 1

    for i in range(Running):
        
        if(container[i].find("h3","s-item__title") != None):
            product_names.append(container[i].find("h3","s-item__title").text)   
        else:
            product_names.append("None")

        temp = container[i].find_all("span",{"class":"s-item__price"})
        
        if(container[i].find("span","b-starrating__star") != None):
            rating.append(container[i].find("span","b-starrating__star").text)
        if(container[i].find("span","b-starrating__star") == None):
            rating.append("None")
        
        if(container[i].find("span","BOLD NEGATIVE") != None):
            S1 = container[i].find("span","BOLD NEGATIVE").text
        else:
            S1 = "None"
        if(container[i].find("span","BOLD") != None):
            S2 = " - " + container[i].find("span","BOLD").text
        else:
            S2 = " - None"

        extra_info.append(S1 + S2)

        links.append(container[i].find('a')['href'])
        
        hold = []

        if(len(temp) > 0):
            hold.append(temp[0].text)
            product_prices.append(hold)
        else:
            hold.append("$123456789") 
            product_prices.append(hold)

#------------------------------------------------------------------------------------------------------------------

'''

Ebay_print_out() function prints all data that was scraped from the Ebay website

'''
          
def Ebay_print_out():
    for i in range(len(product_names)):
        if(product_prices[i][0] != "Tap item to see current priceSee Price" and product_names[i] != "None"):
            print(Fore.LIGHTWHITE_EX + str(i+1) ,".", product_names[i], " - ", product_prices[i]," - ",rating[i]," | ",extra_info[i]+ "\n") 

#------------------------------------------------------------------------------------------------------------------
'''

prices() functions helps determine actual prices of products read in:
Ex: product_prices[1] = ["1 to 1.50"];
this price function converts that to being:
product_prices[1] = ["1 to 1.50"] --> proper_price[1] = 1.25

'''

def prices():
    for i in range(len(product_prices)):
        if(product_prices[i][0].find("Tap") == -1):
            if(len(product_prices[i][0].split(" to ")) > 1):
                L = product_prices[i][0].replace("$", "").replace(",","").split(" to ")
                average = (float(L[0]) + float(L[1]))/2
                average = round(average, 2)
                proper_price.append(average)
            else:
                P = product_prices[i][0].replace("$", "").replace(",","")
                proper_price.append(float(P))

#------------------------------------------------------------------------------------------------------------------
'''
Finds the lowest prices that are the proper prices list
and displays them

'''

def Ebay_find_lowest():

    String  = ''

    order = sorted(proper_price)

    if(len(order) >= 10):
        cheapest_10 = order[:10]
    else:
        cheapest_10 = order
    
    if 123456789.0 in cheapest_10:
        cheapest_10.remove(123456789.0) #the 12356789 price, is the price given to any item that hasnt been 
                                        #read in properly due to problems.
                    
    for i in range(len(proper_price)):
        for j in range(len(cheapest_10)):
            M = String
            if(product_prices[i][0].find("Tap") == -1):
                if(cheapest_10[j] == proper_price[i]):
                    String = product_names[i] + " || " + str(product_prices[i][0]) + " || "
                    I = extra_info[i].split(" - ")
                    if(I[0] != "None"):
                        String+=" -- " + str(I[0])
                    if(I[1]!= "None"):
                        String+=" -- " + str(I[1])
                    if(M != String):
                        print(Fore.CYAN + String)
                        print(Fore.WHITE + "LINK: " + links[i])
                        print("\n")


#------------------------------------------------------------------------------------------------------------------
'''
Saves all data collected into a file, which allows for the user
to create a log information they can pull up and if they want to Graph.

Note: the information is saved in this format:
New Men Women Cap with Fine Embroidery Small Pony Polo Logo Hat Baseball Cotton<<<7.29<<<None<<<528+ Sold - Free International Shipping<<<2019-09-11
                                (NAME)                                          (PRICE)  (RATING)      (Extra info)                    (DATE it was scraped)
'''

def save_info():
    global find

    day = datetime.today().strftime('%Y-%m-%d')
    exist = False
    info = os.listdir()

    for i in range(len(info)):
        if(info[i] == find+".txt"):
            exist = True

    if(exist == False):
        with open(find + ".txt", "w") as file:
            for i in range(len(product_names)):
                if(product_prices[i][0] != "Tap item to see current priceSee Price" and proper_price[i] != 123456789.0):
                    file.write(str(product_names[i])+"<<<"+str(proper_price[i])+"<<<"+str(rating[i])+ "<<<"+ str(extra_info[i])+"<<<"+ str(day) + "\n")

    if(exist == True):
        with open(find + ".txt", "a") as file:
            for i in range(len(product_names)):
                if(product_prices[i][0] != "Tap item to see current priceSee Price" and proper_price[i] != 123456789.0):
                    file.write(str(product_names[i])+"<<<"+str(proper_price[i])+"<<<"+str(rating[i])+ "<<<"+ str(extra_info[i])+"<<<"+ str(day) + "\n")


#------------------------------------------------------------------------------------------------------------------
'''
Finds anysales on productsm and displays those sales

'''
def find_sales():

    String = ""
    for i in range(len(extra_info)):
        I = extra_info[i].split(" - ")
    
        if(I[0].find("Sale") != -1 or I[0].find("off") != -1 or I[0].find("Free") != -1):
             String = product_names[i] + " || " + str(product_prices[i][0]) + " || " + I[0]    
        if(String == ""):
            if(I[1].find("Sale") != -1 or I[1].find("off") != -1 or I[1].find("Free ") != -1):
                String = product_names[i] + " || " + str(product_prices[i][0]) + " || " + I[1]

        if(String!=""):
            print(Fore.GREEN + String)
            print(Fore.WHITE + "LINK: " + links[i])
            print("\n")

        String = ""



#------------------------------------------------------------------------------------------------------------------
'''
Ebay doesnt have a proper rating system, only a select handful of products are actually rated, this
finds any products that are rated and displays them

'''

def rated_items():
    j = 0
    print(Fore.LIGHTBLUE_EX + "Most items aren't rated so here are some that are")

    for i in range(len(rating)):
        if(rating[i] != "None"):
            j+=1
            print(Fore.MAGENTA + product_names[i] + " || " + str(product_prices[i][0]) + " || " + rating[i])
            print(Fore.WHITE + "LINK: " + links[i])
            print("\n")
    if(j == 0):
        print(Fore.WHITE + "No items are rated")

#------------------------------------------------------------------------------------------------------------------
'''

determines the most bought items from the scrape

'''

def most_bought():

    index = []
    most = {}

    for i in range(len(extra_info)):
        I = extra_info[i].split(" - ") 
        if(I[0].find("Sold") != -1):
            index.append(i)

            num = I[0].split(" ")
            num[0] = num[0].replace(",","").replace("+","")
            string = Fore.RED + product_names[i] + " || " + str(product_prices[i][0]) + " || "

            if "Sold" in num[0]:
                N = num[0].split(" ")[0]
                d = {string:N}
                most.update(d)
            else:
                d = {string:num[0]}
                most.update(d)

    sorted(most, key=most.get)
    
    if(len(most) != 0):
        i = 0
        for keys,values in most.items() :
            print(keys,"Amount sold: ",values)
            print(Fore.WHITE + "LINK: " + links[index[i]])
            print("\n")
            i+=1
    else:
        print(Fore.LIGHTRED_EX + "NO ITEMS FOUND")
    
    
#-------------------------------------------GRAPHING FUNCTION---------------------------------------------------------------

'''
Using matplotlib library the user has the ability to graph all the information they collected for that day.
if the user uses the Ebay_pricescrape frequently they can amass a catalogue of data which they can graph.
seeing any changes and fluctuations in prices.

'''

current_Date = [] 
Num_Dates = [] #holds number of dates that are going to be read in
Avg_price = []

'''

Creates the the graph, where x is the date the information was scraped from ebay and the
y is average price when the product was scraped.

'''

def create_xy():
    global find

    i = 0
    hold_price = 0
    N = 0
    with open(find + ".txt","r") as F:

        First_date = F.readline().split("<<<")[-1] #inital date inputed
        i+=1
        current_Date.append(First_date)
        Num_Dates.append(i)
        while F.readline() != "":
            line = F.readline().split("<<<")
            Date = line[-1]    
            if(current_Date.count(Date) != 0):
                if(line[1] != '123456789.0'):
                    hold_price += float(line[1])
                    N+=1

            if(current_Date.count(Date) == 0):
                Avg_price.append(hold_price/N)
                hold_price = 0
                N = 0
                if(Date == ""):
                   break
                else:
                    i+=1
                    current_Date.append(Date)
                    Num_Dates.append(i)
           
            F.readline()

        if(N != 0):   
            Avg_price.append(hold_price/N)
       
        for i in range(len(current_Date)):
            current_Date[i] = current_Date[i].rstrip()

        if(current_Date[-1] == '' or current_Date[-1] == '\n'):
            del current_Date[-1]
            del Num_Dates[-1]

#------------------------------------------------------------------------------------------------------------------
'''
prints Graph

'''
def graph():
    global find

    plt.title("Price Of: " + find)
    plt.xticks(Num_Dates, current_Date)
    plt.plot(Num_Dates, Avg_price)
    plt.show()
    