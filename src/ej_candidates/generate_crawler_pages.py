import os
from ej_candidates.models.candidate import Candidate


def create_pages_dir():
    try:
       os.makedirs("./crawler_pages/candidate")
    except Exception as e:
        print("directory already exists")

def create_candidate_page(candidate):
    os.makedirs("./crawler_pages/candidate/{}".format(candidate.id))
    page_content = "<!doctype html> <html lang='en'> <head> <meta charset='utf-8'> <title>Unidos Contra a Corrupção</title> <meta name='description' content='Conheça as Novas Medidas Contra a Corrupção e faça parte da maior união anticorrupção que o país já viu'> <!-- Meta fo facabook --> <meta name='og:image' content='http://admin.dev.besouro.ejplatform.org/media/{}'> <!-- Meta fo twitter --> <meta name='twitter:image' content='http://admin.dev.besouro.ejplatform.org/media/{}'> <!-- default image meta --> <meta name='image' content='http://admin.dev.besouro.ejplatform.org/media/{}'> <head> </body> <body> </html>".format(candidate.image.name, candidate.image.name, candidate.image.name)
    with open("crawler_pages/candidate/{}/index.html".format(candidate.id), "w") as file:
        file.write(page_content)



def generate():
    create_pages_dir()
    candidates = Candidate.objects.all()
    for candidate in candidates:
        create_candidate_page(candidate)
