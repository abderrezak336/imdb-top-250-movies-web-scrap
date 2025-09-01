import time
import lxml
import requests
from bs4 import BeautifulSoup


#the columns in csv file
#title,score,episode,year,members


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,fr;q=0.8"
}



class BestAnime:
    def __init__(self):
        self.URL= "https://myanimelist.net/topanime.php"
        self.anime_titles = []
        self.anime_score = []
        self.anime_episode = []

    def scap_page(self, limit):
        print(limit)
        if limit == 0:
            response = requests.get(url=f"{self.URL}", headers=headers)
        else:
            self.URL = f"https://myanimelist.net/topanime.php?limit={limit}"
            response = requests.get(url=f"{self.URL}", headers=headers)

        soup = BeautifulSoup(response.text, "lxml")

        # titles
        self.anime_titles = soup.find_all(name="h3", class_="fl-l fs14 fw-b anime_ranking_h3")
        self.anime_titles = [item.getText() for item in self.anime_titles]

        # scores
        self.anime_score = soup.find_all(name="td", class_="score ac fs14")
        self.anime_score = [item.getText() for item in self.anime_score]

        # episode
        self.anime_episode = soup.find_all(name="div", class_="information di-ib mt4")
        self.anime_episode = [item.getText() for item in self.anime_episode]



anime_list = BestAnime()
with open("best_anime.csv", mode="a") as file:
    for l in range(0, 10100, 50):
        time.sleep(0.2)
        anime_list.scap_page(limit=l)
        for d in range(50):
            file.write(f"{anime_list.anime_titles[d]},{anime_list.anime_score[d].strip()},"
                       f"{anime_list.anime_episode[d].split("\n")[1].lstrip()},"
                       f"{anime_list.anime_episode[d].split("\n")[2].strip()},"
                       f"{anime_list.anime_episode[d].split("\n")[3].lstrip().split(" ")[0].replace(",", "")}\n")

