import requests
from bs4 import BeautifulSoup
import csv

def get_html(url):
    response = requests.get(url)
    return response.text

def get_total_pages(html):
    soup = BeautifulSoup(html, "lxml") 
    pages_ul = soup.find("div", class_="pager-wrap").find("ul")
    pages_a = pages_ul.find_all("li")[-1]
    total_pages = pages_a.find("a").get("href").split("=")[-1]
    return int(total_pages)

def write_to_csv(data):
    with open("kivano_telefon.csv", "a") as csv_file:
        writer = csv.writer(csv_file, delimiter="/")
        writer.writerow((data["title"],
                         data["price"],
                         data["photo"]))

def get_page_data(html):
    soup = BeautifulSoup(html, "lxml")
    product_list = soup.find("div", class_="list-view")
    products = product_list.find_all("div", class_="item product_listbox oh")

    for product in products:
        try:
            title = product.find("div", class_="listbox_title oh").find("a").text
        except:
            title = ""    
        try:
            price = product.find("div", class_="listbox_price text-center").find("strong").text
        except:
            price = ""
        try:
            photo = product.find("div", class_="listbox_img pull-left").find("a").find("img").get("src")
        except:
            photo = ""
        
        data = {"title": title, "price": price, "photo": "https://www.kivano.kg" + photo}
        write_to_csv(data)

def main():
    mobilnye_telefony = "https://www.kivano.kg/mobilnye-telefony"
    pages = "?page="
    total_pages = get_total_pages(get_html(mobilnye_telefony))
    for page in range(1, total_pages+1):
        url_with_page = mobilnye_telefony + pages + str(page)
        html = get_html(url_with_page)
        get_page_data(html)

main()    