   soup = BeautifulSoup(r.text, 'html.parser')

    links = soup.find_all('a')

    if r.status_code == 200:
        for link in links:
            href = link.get('href')
            print(href)