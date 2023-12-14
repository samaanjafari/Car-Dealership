import re
import requests
from bs4 import BeautifulSoup
from mysql.connector import connection
from sklearn import tree
keeper = []
x = []
y = []
cnx = connection.MySQLConnection(user='username', password='yourpass',
                                 host='127.0.0.1',
                                 database='yourdatabase')

estimate = input('write coronologically 1-brand 2-model 3-year and 4-mileage of your car and seprate them with just one withespace to estimate how much does it worth.(BE CATIUOS U HAVE TO SEPRATE DATAS WITH ONLY  JUST ONE SPACE OTHERWISE IT WONT WORK) ').split(' ')

for i in range (1,20):
    res = requests.get('https://www.truecar.com/used-cars-for-sale/listings/%s/%s/?page=%i' % (estimate[0],estimate[1],i))
    soup = BeautifulSoup(res.text,'html.parser')
    cars = soup.find_all('div',attrs = {'data-test':"cardContent", 'class':"card-content order-3 vehicle-card-body"})

        
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
        if final in keeper:
            continue
        else:
            keeper.extend(final)
            
        cursor = cnx.cursor()
        cursor.execute('INSERT INTO cars VALUES (\'%s\',\'%s\' , \'%i\' , \'%s\' , \'%s\') '  % ((brand,model,year,price,mile)))
        cnx.commit()        
        print('%s %s %i is %s and mileage is %s'%(brand,model,year,price,mile))
        
    
    cursor = cnx.cursor()    
    query = 'SELECT * FROM cars WHERE brand = brand or model = model;'    
    cursor.execute(query)
    
    for brand,model,year,price,mile in cursor:
        mile = mile.split(',')
        mile = ''.join(mile)
        mile = int(mile)
        price = price.split('$')
        price = price[1].split(',')
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
            
                 
 
