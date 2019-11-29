from bs4 import BeautifulSoup
import requests
import re
import sys

source_link = '/wiki/Patrick_Balkany'
target_link = '/wiki/Scientologie'

already_visited_pages = []
path = ''
find = False

max_try= 6000000
tries = 0

"""
    Fonction qui va filtrer les sites qui ont déjà été visités.
"""
def not_already_visited_page(link):
    global already_visited_pages
    return not link in already_visited_pages


"""
    Fonction qui va sur un lien récupérer une page et analyser tous les lien contenus dans la page.
"""
def parse_page(link):
    global tries
    global find
    global path

    # L'url passé à requests.get est potentiellement invalide.
    try:
        current_link = link[-1]
        
        r  = requests.get('https://fr.wikipedia.org' + current_link)
        
        data = r.text
        
        soup = BeautifulSoup(data, features="lxml")
        
        already_visited_pages.append(current_link)
        print(f"Try number {tries}")
        print(f"Try {current_link}...")
        
        # On récupère tous les liens dont la balise href respecte notre RegEx.
        all_links = soup.find_all('a', href=re.compile('^(/wiki/)((?!:).)*$'))
        
        parsed_links = set()
        
        for l in all_links:
            if 'href' in l.attrs:
                parsed_links.add(l.attrs['href'])
        
        parsed_links = list(filter(not_already_visited_page, parsed_links))
        
        if target_link in parsed_links:
            path = link + [target_link]
            find = True
            print(f"Vous avez trouvé un lien entre {source_link} et {target_link}")
            print(f"Le chemin trouvé est {' -> '.join(path)}")
            return
        
        organised_links = []
    
        # On entreprose le chemin et on initialise une liste de liens vide
        for li in parsed_links:
            organised_links.append({
                    "path": link + [li],
                    "links": []
                    })
    
        return organised_links
    
        
    except:
        print(f"Erreur lors de l'ouverture de {link}", file=sys.stderr)
        return


"""
    Fonction principale récursive sur la liste de liens qu'on trouve.
"""
def main(list_links):
    global tries
    global find
    global path
    global max_try

    for path_links in list_links:
        path_links['links'] = parse_page(path_links['path'])

        # Si on a dépassé le nombre d'essais ou qu'on a un type faux en retour ou qu'on a fin qui est vrais alors on met fin au programme.
        if (tries > max_try or not path_links['links'] or find):
            return
        
        tries += 1
    
    for all_lists in list_links:
        main(all_lists['links'])

# Début du programme.
main([
      {
       "path": [source_link],
       "links": []
       }
      ])

print("Program's end...")

    
    