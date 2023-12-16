import re
import requests
from bs4 import BeautifulSoup
from mysql.connector import (connection)
cnx = connection.MySQLConnection(user='username', password='yourpass',
                                 host='127.0.0.1',
                                 database='databasename')

vehicle = input('what car are u looking for?(brand and model): ').split(' ')


res = requests.get('https://www.truecar.com/used-cars-for-sale/listings/%s/%s/' % (vehicle[0],vehicle[1]))
soup = BeautifulSoup(res.text,'html.parser')
cars = soup.find_all('div',attrs = {'data-test':"cardContent", 'class':"card-content order-3 vehicle-card-body"})

    
count = 0
for car in cars:
    want = re.findall(r'\w*?(\d+ \w+ \w+) .* list price(\$\d+\,\d{3})*(\$\d+\,\d{3})(\d+\,*\d*)',car.text)
    if want==[]:
        continue
    final = []
    for i in want:
        for j in i:
            if j!='':
                final.append(j)
    if len(final)==4:
        final.remove(final[1])    
    
    all = final[0].split(' ')
    year = all[0]
    year = int(year)
    brand = all[1]
    model = all[2]
    price = final[1]
    mile = final[2]

    cursor = cnx.cursor()
    cursor.execute('INSERT INTO cars VALUES (\'%s\',\'%s\' , \'%i\' , \'%s\' , \'%s\') '  % ((brand,model,year,price,mile)))
    cnx.commit()        
    #print('%s %s %i is %s and mileage is %s'%(brand,model,year,price,mile))
    count+=1
    if count==20:
        break
cnx.close()        
                    
