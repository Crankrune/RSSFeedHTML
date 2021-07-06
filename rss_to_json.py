import json
import xml.etree.ElementTree as ET

tree = ET.parse("./Inoreader Subscriptions 20201104_full.xml")
root = tree.getroot()

feeds = {}
for item in root.findall("body/outline/outline"):
    d = item.attrib
    title = d.pop("title", None)
    feeds[title] = d

with open("inoreader_feeds_20201104.json", "w") as fl:
    json.dump(feeds, fl, indent=4, sort_keys=True)
