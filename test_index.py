import json
import validators

def test_index():
    with open("index.json") as f:
        index = json.load(f)
    
    names = []
    for i in index:
        assert validators.url(i["download_url"])
        assert i["download_url"].startswith("https://raw.githubusercontent.com/amidaware/reporting-templates/master")
        names.append(i["name"])
    
    # make sure names are all unique
    assert len(names) == len(set(names))