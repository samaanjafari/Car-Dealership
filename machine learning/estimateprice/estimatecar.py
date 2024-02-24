import re
import requests
from bs4 import BeautifulSoup
from mysql.connector import connection
from sklearn import tree
keeper = []
x = []
y = []
cnx = connection.MySQLConnection(user='root', password='samanJA1381',
                                 host='127.0.0.1',
                                 database='maktabkhooneh')

estimate = input('write coronologically 1-brand 2-model 3-year and 4-mileage of your car and seprate them with just one withespace to estimate how much does it worth.(BE CATIUOS U HAVE TO SEPRATE DATAS WITH ONLY  JUST ONE SPACE OTHERWISE IT WONT WORK) ').split(' ')

base_url = 'https://www.truecar.com/used-cars-for-sale/listings/%s/%s/?page=' % (estimate[0], estimate[1])

for i, p in enumerate(estimate):
    if estimate[0]=="bmw" and ('x' or 'm' in estimate[1]):
        estimate[i] = p.upper()
    elif estimate[0]=="bmw" and ('i' in estimate[1]):
        estimate[0] == "BMW"  
    else:    
        estimate[i] = p.capitalize()



for i in range(1,20):
    url = base_url + str(i)
    print(f"Rquesting URL: {url}")
    
    res = requests.get(url)
    if res.history:
       print("Request was redirected.")
       for r in res.history:
           print(r.status_code, r.url)
           print("Final Dest:")
           print(r.status_code, r.url)
           default = 'https://www.truecar.com/used-cars-for-sale/listings/%s/%s/' % (estimate[0], estimate[1])
           if r.url==default:
               continue
           
    print(f"Status code: {res.status_code}")
    
    soup = BeautifulSoup(res.text,'html.parser')
    cars = soup.find_all('div', attrs = {"class":"mt-1 flex w-full items-start p-2"})

    pattern = r'Used.* (\d+) (%s)(%s) (.*)(\$\d+,\d+).*Price(\d+)' % (re.escape(estimate[0]), re.escape(estimate[1]))



    for car in cars:
        matches = re.findall(pattern, car.text) 
        #print(car.text)
        if matches:
            #result = []
            for match in matches:
                year, brand, model, trim, price, mile = match
                year = int(year)
                mile = mile.split(",")
                mile = ''.join(mile)
                mile = str((int(mile)*1000))
                link = None
                if match in keeper:
                    continue
                
                keeper.append(match)
                
                # for el in match:
                #     result.append(el)
                # print(result)
    
                cursor = cnx.cursor()
                cursor.execute('INSERT INTO cars VALUES (\'%s\',\'%s\', \'%s\' , \'%i\' , \'%s\' , \'%s\', \'%s\') '
                            % ((brand, model, trim, year, price, mile, link))) 
                cnx.commit()  
        
                #print('%s %s %s %i is %s and mileage is %s' %(brand, model, trim, year, price, mile))
        else:
            continue    
            
            
    cursor = cnx.cursor()    
    query = '''SELECT * FROM cars WHERE brand=brand AND model=model;'''   
    cursor.execute(query)
    
    for brand, model, trim, year, price, mile, link in cursor:
        mile = int(mile)
        price = price[1:]
        price = price.split(',')
        price = ''.join(price)
        price = int(price)
        x.append([year,mile])
        y.append(price)
        
        
    removal = 'TRUNCATE TABLE cars;'
    cursor.execute(removal)         
cnx.close()         
           
clf = tree.DecisionTreeClassifier()
clf = clf.fit(x, y)    
estimate[2] = int(estimate[2])
estimate[3] = int(estimate[3])
new_data = [[estimate[2],estimate[3]]]
awnser = clf.predict(new_data)
print('%s$' % (awnser[0]))          
            
                 
 