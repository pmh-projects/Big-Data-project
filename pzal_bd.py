#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup as bs
import requests
import numpy
import pandas
import matplotlib.pyplot as plt
import csv
import time
get_ipython().run_line_magic('matplotlib', 'inline')


# In[3]:


wszystkie_ceny_kursow = []
wszystkie_typy_kursow = []
wszystkie_rodzaje_kursow = []
sposob_prowadzenia_lista = []
ceny_niesformatowane = []
czestotliwosc_lista=[]
wszystkie_kategorie = []
tytuly_kursow = []
lista_do_csv = []


for i in range(54):
    url = f"https://pll.harvard.edu/catalog?page={i}"

    print(url)
    response = requests.get(url, timeout=20)
    
    if response.status_code==200:
        print("Polaczono.")
        print(i)
        
    else:
        while response != 200:           
            url = f"https://pll.harvard.edu/catalog?page={i}"
            response = requests.get(url, timeout=30)
            
            if response.status_code==200:
                print("Polaczono.")
                
            else:
                print("Nie polaczono.")
                time.sleep(2)
            
        
    html = response.content
    time.sleep(0.5)
    soup = bs(html, "lxml")
    time.sleep(0.5)
        
    scrap1 = soup.select("div.field.field-name-price span.paid")
    scrap2 = soup.select("div.group-right div.field-name-modality")
    scrap3 = soup.select("div.field.field-name-subject-area")
    tytuly = soup.find_all("div", class_="field field-name-title-qs")

    scrap4 = soup.find_all("div", class_="field field-name-price")
    scrap5 = soup.find_all("div", class_="field field-name-modality")
    scrap6 = soup.find_all("div", class_="field field-name-subject-area")
    scrap7 = soup.find_all("div", class_="field field-name-duration")
      
  
    for cena in scrap4:
        
        wyczysc_cena= cena.get_text(strip=True).strip('$')
        ceny_niesformatowane.append(wyczysc_cena)
        
    for sp in scrap5:    
        wyczysc_sp= sp.get_text(strip=True)
        sposob_prowadzenia_lista.append(wyczysc_sp)
            
      
    for kategoria in scrap6:
        wyczysc_kategoria= kategoria.get_text(strip=True)
        wszystkie_kategorie.append(wyczysc_kategoria)

            
    for czestotliwosc in scrap7:
        wyczysc_czestotliwosc= czestotliwosc.get_text(strip=True)
        czestotliwosc_lista.append(wyczysc_czestotliwosc)
            
    for tytul in tytuly:    
        tytuly_kursow.append(tytul.get_text(strip=True))                
            
    for cena_kursow in scrap1:
        wszystkie_ceny_kursow.append(cena_kursow.get_text(strip=True).strip('$'))
            
    for typ_kursow in scrap2:
         wszystkie_typy_kursow.append(typ_kursow.get_text(strip=True))     
            
    for rodzaj_kursow in scrap3:
         wszystkie_rodzaje_kursow.append(rodzaj_kursow.get_text(strip=True))
            
    courses = soup.find_all("div", "group-right")
    data=[]
            
    for c in courses:
        
        course={}
        course1 = c.find("div", class_="field field-name-title-qs") 
        course2 = c.find("div", class_="field field-name-field-course-summary")
        course3 = c.find("div", class_="field field-name-price")
        
        course["Tytul"] = course1.get_text(strip=True)
        course["Opis"] = course2.get_text(strip=True)
        course["Cena"] = course3.get_text(strip=True)
        data.append(course)
        

    df= pandas.DataFrame(data)
    df.to_csv("courses.csv", mode='a', header=None)


# In[ ]:





# In[4]:


df2 = pandas.read_csv('courses.csv',header=None, names=["Nazwa","Opis","Cena"])
df2


# In[5]:


df.to_csv("courses2.csv")


# In[6]:


ceny_kursow = pandas.Series(wszystkie_ceny_kursow)
ceny_kursow.value_counts().to_frame().reset_index().rename(columns={"index":"Koszt w $", 0:"Liczba kursów"})


# In[7]:


ceny_kursow = pandas.Series(wszystkie_ceny_kursow)
ceny_kursow.value_counts(normalize = True).to_frame().reset_index().rename(columns={"index":"Koszt w $", 0:"Liczba kursów"})


# In[8]:


tytuly_kursow_lista = []
nr = 1
for tytul in tytuly_kursow[:900]:
    tytuly_kursow_lista.append(tytul)
    print(nr)
    print(tytul)
    nr+=1


# In[9]:


print(tytuly_kursow_lista)


# In[10]:


df = pandas.DataFrame(tytuly_kursow)
df.to_csv (r'C:\Users\user4\Pictures\Debut\export_dataframe.csv', index = False, header=True, encoding ='utf-8')


# In[11]:


data = open(r'C:\Users\user4\Pictures\Debut\export_dataframe.csv', encoding ='utf-8')
df5 = pandas.read_csv(data)
df5.head(100).rename(columns={"0":"Tytuł Kursu"})


# In[12]:


print(ceny_niesformatowane)


# In[13]:


ceny_sformatowane = []

for cf in ceny_niesformatowane:
    nowa_cf = cf.replace("Free*", "0").replace(",", "")
    ceny_sformatowane.append(nowa_cf)
    ceny_sformatowane.sort()

print(ceny_sformatowane)


# In[17]:


graf_cen = pandas.Series(ceny_sformatowane)
plt.figure(figsize=(100, 50))
plt.title("Cena pojedynczego kursu harvard.edu", fontsize = 18)
plt.xticks(numpy.arange(0, 1000, step=1))
plt.yticks(numpy.arange(0, 1000, step=1))
plt.xlabel("Kwota w $")
plt.ylabel("Liczba kursów")
graf_cen.hist(bins=200)


# In[18]:


typy_kursow = pandas.Series(wszystkie_typy_kursow)
typy_kursow.value_counts().to_frame().reset_index().rename(columns={"index":"Typ kursu", 0:"Liczba kursów"})


# In[19]:


df2 = pandas.DataFrame(typy_kursow.value_counts().reset_index().rename(columns={"index":"Typ kursu", 0:"Liczba kursów"}))
df2.to_csv (r'C:\Users\user4\Pictures\Debut\export_dataframe2.csv', index = False, header=True, encoding ='utf-8')


# In[20]:


df2


# In[21]:


data2 = open(r'C:\Users\user4\Pictures\Debut\export_dataframe2.csv',encoding ='utf-8')
df6 = pandas.read_csv(data2)
df6.head(100)


# In[22]:


print(sposob_prowadzenia_lista)


# In[27]:


graf_sposob_prowadzenia_lista = pandas.Series(sposob_prowadzenia_lista)
plt.figure(figsize=(100, 50))
plt.title("Tryb kursów dostępnych na harvard.edu", fontsize = 18)
plt.xticks(numpy.arange(0, 1000, step=1))
plt.yticks(numpy.arange(0, 1000, step=1))
plt.xlabel("Tryb kursów")
plt.ylabel("Liczba kursów")
graf_sposob_prowadzenia_lista.hist(bins=20)


# In[28]:


rodzaje_kursow = pandas.Series(wszystkie_rodzaje_kursow)
rodzaje_kursow.value_counts().to_frame().reset_index().rename(columns={"index":"Rodzaj kursu", 0:"Liczba kursów"})


# In[29]:


print(wszystkie_rodzaje_kursow)


# In[35]:


graf_wszystkie_kategorie = pandas.Series(wszystkie_rodzaje_kursow)
plt.figure(figsize=(100, 50))
plt.title("Typy kursów dostępnych na harvard.edu\nz zakresu 'Computer Science Courses'", fontsize = 18)
plt.xticks(numpy.arange(0, 1000, step=1))
plt.yticks(numpy.arange(0, 1000, step=1))
plt.xlabel("Kategoria")
plt.ylabel("Liczba kursów")
graf_wszystkie_kategorie.hist(bins=30)


# In[36]:


print(czestotliwosc_lista)


# In[38]:


graf_final_duration = pandas.Series(czestotliwosc_lista)
plt.figure(figsize=(100, 50))
plt.title("Czas trwania kursów dostępnych na harvard.edu\nz zakresu 'Computer Science Courses'", fontsize = 18)
plt.xticks(numpy.arange(0, 900, step=1))
plt.yticks(numpy.arange(0, 900, step=1))
plt.xlabel("Czas trwania kursów w tygodniach", fontsize = 12)
plt.ylabel("Liczba kursów", fontsize = 12)
graf_final_duration.hist(bins=100)

