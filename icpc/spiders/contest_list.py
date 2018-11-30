import scrapy
import json
import os

include_list = ["Regional"]
exclude_list = ["First Round", "Preliminary"]

def inc_exc_filter(s):
    for inc in include_list:
        if inc in s: break
    else:
        return False
    for exc in exclude_list:
        if exc in s: return False
    return True

class ContestListSpider(scrapy.Spider):
    name = "contest_list"
    allowed_domains = ["icpc.baylor.edu"]

    def __init__(self, year='', **kwargs):
        self.start_urls = [
            "https://icpc.baylor.edu/cm5-contest-rest/rest/contest/public/regionals/{}".format(year)
        ]
        self.year = year
        super().__init__(**kwargs)

    def parse(self, response):
        data = json.loads(response.body_as_unicode())
        reg_id = -1
        for entry in data:
            if "Asia East Continent" in entry["label"]:
                reg_id = entry["id"]
            elif reg_id == -1 and "Asia" in entry["label"]:
                reg_id = entry["id"]
        print("id =", reg_id)
        os.makedirs(self.year, exist_ok=True)
        yield scrapy.Request(
            "https://icpc.baylor.edu/cm5-contest-rest/rest/contest/public/contests-under/{}".format(reg_id),
            self.parse_contest_list,
        )

    def parse_contest_list(self, response):
        data = json.loads(response.body_as_unicode())
        contest_ids = [(entry["abbreviation"], entry["id"]) for entry in data if inc_exc_filter(entry["contest"])]
        print("ids =", *contest_ids, sep = '\n')
        for abbr, contest_id in contest_ids:
            yield scrapy.Request(
                "https://icpc.baylor.edu/cm5-contest-rest/rest/contest/standings/contest/{}?q=proj:place,institution,team,problemsSolved,totalTime,lastSolution%3Bsort:place+asc%3B&page=1&size=5000".format(contest_id),
                callback=self.parse_standing,
                meta={"abbr": abbr}
            )

    def parse_standing(self, response):
        with open(self.year + "/" + response.meta["abbr"] + ".json", "wb") as f:
            f.write(response.body)

        