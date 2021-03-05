from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import tree
import requests
from bs4 import BeautifulSoup
import pandas as pd


# Create your views here.

def index(request):
    return render(request, 'index.html')

def titanic(request):
    return render(request, 'titanic_prediction.html')

def match_image(request):
    return render(request, 'match_image.html')

def ebay_scraping(request):
    base_url = "https://www.ebay.com/sch/i.html?_from=R40&_nkw="
    url_separator = "&_sacat=0&_pgn="
    request = "watches"
    page_num = "1"
    
    #------Single page
    url = base_url + request + url_separator + page_num
    products = get_page_links(get_page(url))
    for link in products:
        data = detail_data(get_page(link))
        print(data)
        
    #------Multiple pages
    #elif(type_of_scraping == "Multiple"):
    #    print("First page number")
    #    start_page = input()
    #    print("Last page number")
    #    end_page = input()
    #    for pages in range(start_page, end_page):
    #        url = base_url + request + url_separator + str(pages)
    #        products = get_page_links(get_page(url))
    #        for link in products:
    #            data = detail_data(get_page(link))
    #            print(data)
                
    else:
        print("Sorry unable to detect:(")

    return render(request, 'ebay_scraping.html')

def get_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    return soup

def detail_data(soup):
    try:
        name = soup.find('h1', id='itemTitle').text.strip().replace('Details about  \xa0', ' ')
    except:
        name = ''
    try:
        price = soup.find('div', id='vi-mskumap-none').find('span').text.strip()
    except:
        price = ''
    try:
        sold = soup.find('span', class_='vi-qtyS-hot-red').find('a').text.strip().split(' ')[0]
    except:
        sold = ''
    product_details = {
        'name' : name,
        'price' : price,
        'total_sold' : sold
    }
    
    return product_details

def get_page_links(soup):
    try:
        links = soup.find_all("a", class_="s-item__link")
    except:
        links = []
        
    urls = [item.get('href') for item in links]
    
    return urls



def classify(request):
    df = pd.read_csv('Titanic_Prediction\\dataset\\Titanic Disaster Dataset.csv')
    
    df.drop(['PassengerId'],axis='columns',inplace=True)
    inputs = df.drop('Survived',axis='columns')
    target = df.Survived
    inputs.columns[inputs.isna().any()]
    inputs = inputs.fillna('S')
    inputs.Gender = inputs.Gender.map({'male':0,'female':1})
    inputs.Embarked = inputs.Embarked.map({'S':0,'C':1, 'Q':2})
    X_train, X_test, y_train, y_test = train_test_split(inputs, target, test_size=0.2)
    
    clf = tree.DecisionTreeClassifier()
    clf.fit(X_train,y_train)
    y_pred = clf.predict(X_test)

    check = False
    gender_value = 2
    embarked_value = 2

    pclass = request.POST.get('pclass')
    gender = request.POST.get('gender')
    sibling = request.POST.get('sibling')
    embarked = request.POST.get('embarked')

    if(gender=='male'):
        gender_value = 0
        check = True
    elif(gender=='female'):
        gender_value = 1
        check = True

    if(embarked == 'S'):
        embarked_value = 0
        check = True
    elif(embarked == 'C'):
        embarked_value = 1
        check = True
    elif(embarked == 'Q'):
        embarked_value = 2   
        check = True 

    encoded_values = [[pclass,gender_value,sibling,embarked_value]]
    prediction = clf.predict_proba(encoded_values)[0][1]
    pred = round(prediction*100)
    if pred < 50:
        alert_class = "alert alert-danger"
    if pred > 50:
        alert_class = "alert alert-success"
    
    data = {
        'alert' : alert_class,
        'pred' : pred
    }

    return render(request, 'result_titanic.html', {'data':data})

