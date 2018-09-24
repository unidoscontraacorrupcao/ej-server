import os
from django.conf import settings

from ej_candidates.models.candidate import Candidate

def create_pages_dir():
    try:
       os.makedirs("./crawler_pages/candidate")
    except Exception as e:
        print("directory already exists")

def get_image_domain():
    if settings.ENVIRONMENT == 'dev':
        return 'https://dev.besouro.ejplatform.org'
    if settings.ENVIRONMENT == 'prod':
        return 'https://app.unidoscontraacorrupcao.org.br'
    return 'http://localhost:8000'

def get_image_url(candidate):
    domain = get_image_domain()
    return "{}/media/{}".format(domain, candidate.image.name)

def create_candidate_page(candidate):
    image_url = get_image_url(candidate)
    os.makedirs("./crawler_pages/candidate/{}".format(candidate.id))
    page_content = "<!doctype html> <html lang='en'> <head> <meta charset='utf-8'/> <title>Unidos Contra a Corrupção</title> <meta name='description' content='Conheça as Novas Medidas Contra a Corrupção e faça parte da maior união anticorrupção que o país já viu'/> <!-- Meta fo facabook --> <meta name='og:image' content='{}'/> <!-- Meta fo twitter --> <meta name='twitter:card' content='summary'/> <meta name='twitter:title' content='Unidos Contra a Corrupção'/> <meta name='twitter:image' content='{}'> <!-- default image meta --> <meta name='image' content='{}'> </head> <body> </body> </html>".format(image_url, image_url, image_url)
    with open("crawler_pages/candidate/{}/index.html".format(candidate.id), "w") as file:
        file.write(page_content)



def generate():
    create_pages_dir()
    candidates = Candidate.objects.all()
    for candidate in candidates:
        create_candidate_page(candidate)
