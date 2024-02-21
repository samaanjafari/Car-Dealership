import re
import requests
from bs4 import BeautifulSoup
from mysql.connector import (connection)
cnx = connection.MySQLConnection(user='root', password='samanJA1381',
                                 host='127.0.0.1',
                                 database='maktabkhooneh')

vehicle = input('what car are u looking for?(brand and model): ').split(' ')


base_url = 'https://www.truecar.com/used-cars-for-sale/listings/%s/%s/?page=' % (vehicle[0], vehicle[1])

for i, p in enumerate(vehicle):
    if vehicle[0]=="bmw" and ('x' or 'm' in vehicle[1]):
        vehicle[i] = p.upper()
    elif vehicle[0]=="bmw" and ('i' in vehicle[1]):
        vehicle[0] == "BMW"  
    else:    
        vehicle[i] = p.capitalize()



for i in range(1,3):
    url = base_url + str(i)
    print(f"Rquesting URL: {url}")
    
    res = requests.get(url)
    print(f"Status code: {res.status_code}")
    
    soup = BeautifulSoup(res.text,'html.parser')
    cars = soup.find_all('div', attrs = {"class":"mt-1 flex w-full items-start p-2"})
    car_link = soup.find_all('a', attrs = {'class':"absolute top-0 left-0 bottom-0 right-0 w-full z-[2]", 'data-test':"vehicleCardLink",'href': True})

    pattern = r'Used.* (\d+) (%s)(%s) (.*)(\$\d+,\d+).*Price(\d+)' % (re.escape(vehicle[0]), re.escape(vehicle[1]))

    for i,car in enumerate(cars):
        matches = re.findall(pattern, car.text)
        link = car_link[i]['href']
        matches[0] = matches[0] + (link,) 
        print(car.text)
        if matches:
            #result = []
            for match in matches:
                year, brand, model, trim, price, mile, link = match
                year = int(year)
                mile = mile.split(",")
                mile = ''.join(mile)
                mile = str((int(mile)*1000))
                
                # for el in match:
                #     result.append(el)
                # print(result)
            
                cursor = cnx.cursor()
                cursor.execute('INSERT INTO cars VALUES (\'%s\',\'%s\', \'%s\' , \'%i\' , \'%s\' , \'%s\', \'%s\') '
                            % ((brand, model, trim, year, price, mile, link))) 
                cnx.commit()  
            
                print('%s %s %s %i is %s and mileage is %s'%(brand, model, trim, year, price, mile))

        else:
            continue
cnx.close()        
                    