from django.shortcuts import render
from .models import ScrapedPage
import httplib2
from bs4 import BeautifulSoup
import requests


# Create your views here.
def scrape(request):
    # Prüfen ob es sich um einen POST-request handelt
    if request.method == 'POST':
        # Wert des POST-request printen
        print('Received data:', request.POST)
        print('Received data:', request)

        try:
            URL = request.POST['url']

            page = requests.get(URL)

            http = httplib2.Http()
            status, response = http.request(URL)

            soup = BeautifulSoup(response, "html.parser")

            title_text = soup.title.text
            title_len = len(title_text)
            try:
                meta_text = soup.find("meta", {"name": "description"})["content"]
            except:
                try:
                    meta_text = soup.find("meta", {"name": "Description"})["content"]
                except:
                    meta_text = "No meta description found"
            meta_len = len(meta_text)

            try:
                h1_text = soup.h1.text
            except:
                h1_text = soup.h1

            if h1_text == None:
                h1_text = "No h1 found"
                h1_len = 0
            else:
                h1_len = len(h1_text)


            # Neues Objekt erstellen
            ScrapedPage.objects.create(url=URL, title_text=title_text, title_len=title_len, meta_text=meta_text, meta_len=meta_len, h1_text=h1_text, h1_len=h1_len)
        except:
            print(request.POST['delete'])
            id = request.POST['delete']

            # Objekt löschen
            post_to_delete = ScrapedPage.objects.get(id=id)
            post_to_delete.delete()

        # Alle Objekte aus Datenbank holen
    all_items = ScrapedPage.objects.all()
    context = {
        'all_items': all_items
    }

    # Pass name of html template
    return render(request, 'index.html', context)


