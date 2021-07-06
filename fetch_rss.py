import feedparser
import jinja2
import json
from bs4 import BeautifulSoup
from datetime import datetime
from pprint import pprint
from time import mktime

with open("inoreader_feeds_20201104.json", "r") as fl:
    feeds_dict = json.load(fl)


class feed_item(object):
    def __init__(self, d: dict, source: str):
        self.title = d["title"]
        # self.summary = d["summary"]
        self.summary = self.html_clean(d["summary"])
        self.link = d["link"]
        self.date = self.get_date(d["published_parsed"])
        self.date_str = self.date_to_str(self.date)
        self.author = d.get("author")
        self.dateline = f"By {self.author} on {self.date_str}"
        self.source = source

    def get_date(self, date) -> datetime:
        dt = datetime.fromtimestamp(mktime(date))
        return dt

    def date_to_str(self, dt) -> str:
        dt_str = self.custom_strftime("%b {S}, %Y at %I:%M %p", dt)
        return dt_str

    def suffix(self, d) -> str:
        return "th" if 11 <= d <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(d % 10, "th")

    def custom_strftime(self, format, t) -> str:
        return t.strftime(format).replace("{S}", str(t.day) + self.suffix(t.day))

    def html_clean(self, html):
        bs = BeautifulSoup(html, "lxml")
        return bs.text


def page_gen(source, entries):
    feed = []
    for item in entries:
        feed.append(feed_item(item, source=source))

    title = f"{feed[0].source} - Feed"
    filename = "{}_{}".format(title, datetime.now().strftime("%Y%m%d"))

    jfile = (
        jinja2.Environment(
            loader=jinja2.FileSystemLoader("./"),
        )
        .get_template("feed_template.html")
        .render(feed=feed, title=title)
    )

    with open(f"{filename}.html", "w", encoding="utf-8") as f:
        f.write(jfile)


# pprint(feeds_dict)

# source = "Axios"
# feed = feeds_dict["TV Series Finale"]["xmlUrl"]
# feed = feeds_dict["The Hard Times"]["xmlUrl"]
# feed = feeds_dict["Axios"]["xmlUrl"]
# fdp = feedparser.parse(feed)
# for item in fdp["entries"]:
#     # pprint(item)
#     fi = feed_item(item, source=source)
#     print(fi.date, fi.dateline)

for src in [
    "TV Series Finale",
    "The Hard Times",
    "Axios",
    "The Onion",
    "PBS NewsHour - Headlines",
    "News : NPR",
]:
    feed_url = feeds_dict[src]["xmlUrl"]
    fdp = feedparser.parse(feed_url)
    page_gen(src, fdp["entries"])
