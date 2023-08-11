from django.shortcuts import render
from .models import ScrapedPage
import httplib2
from bs4 import BeautifulSoup
import requests


# Create your views here.
def scrape(request):
    # Prüfen ob es sich um einen POST-request handelt
    if request.method == 'POST':
        if 'url' in request.POST:
        # Wert des POST-request printen
            print('Received data:', request.POST)
            print('Received data:', request)


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

            # Alle Objekte aus Datenbank holen
            all_items = ScrapedPage.objects.all()
            context = {
                'all_items': all_items
            }

        elif 'row_id' in request.POST:
            print('Received data:', request.POST)
            id = request.POST['row_id']

            # Objekt löschen
            post_to_delete = ScrapedPage.objects.get(id=id)
            post_to_delete.delete()

            # Alle Objekte aus Datenbank holen
            all_items = ScrapedPage.objects.all()
            context = {
                'all_items': all_items
            }

        elif 'filter' in request.POST:
            if request.POST['filter'] != 'reset':
                print('Received data:', request.POST)

                filter_value = request.POST['filter']

                # Ausgewählte Objekte aus Datenbank holen
                all_items = ScrapedPage.objects.filter(title_len__lt=filter_value).values()
                context = {
                    'all_items': all_items
                }
            else:

                # Alle Objekte aus Datenbank holen
                all_items = ScrapedPage.objects.all()
                context = {
                    'all_items': all_items
                }

        elif 'no_h1' in request.POST:
            # Ausgewählte Objekte aus Datenbank holen
            all_items = ScrapedPage.objects.filter(h1_text="No h1 found").values()
            context = {
                'all_items': all_items
            }

        else:

            # Alle Objekte aus Datenbank holen
            all_items = ScrapedPage.objects.all()
            context = {
                'all_items': all_items
            }
    else:
        # Alle Objekte aus Datenbank holen
        all_items = ScrapedPage.objects.all()
        context = {
            'all_items': all_items
        }

    # Pass name of html template
    print(context)
    return render(request, 'index.html', context)


