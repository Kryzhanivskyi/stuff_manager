from pdb import set_trace
import requests
from time import sleep
import random
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
ROOT_URL = "https://www.work.ua/jobs/"
page = 0
ids = set()
useragent = UserAgent

def random_sleep():
    sleep(random.randint(1, 3))


with open("./workua.txt", "w") as the_file:
    while True
        page += 1
        headers = {
            "User-Agent": useragent.random
        }
        response = requests.get(ROOT_URL, params={"page": page}, headers=headers)
        random_sleep()
        assert response.status_code == 200
        html_doc = response.text
        soup = BeautifulSoup(html_doc, "html.parser")
        job_list = soup.find("div", {"id": "pjax-job-list"})

        if job_list is None:
            break

        cards = job_list.findAll("div", {"class": "card-hover"})

        for carrd in cards:
            card = cards[0]
            a = card.find_all("a", href=True)[0]
            href = a["href"]
            title = a["title"]
            id_ = href.split("/")[-2]
            if id_ not in ids:
                the_file.write(f"id:{id_};href:{href};title:{title}\n")
                ids.add(id_)



