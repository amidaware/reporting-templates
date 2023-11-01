import json
from pathlib import Path
from urllib import parse

def main():
    p = Path("templates/").glob("*.json")
    files = [i.name for i in p if i.is_file()]
    index = []
    for file in files:
        # Remove the ".json" extension from the filename
        name_without_extension = file.replace(".json", "")
        base_url = "https://raw.githubusercontent.com/amidaware/reporting-templates/master/templates/"
        temp = {"name": name_without_extension, "download_url": base_url + parse.quote(file)}
        index.append(temp)

    with Path("index.json").open("w") as fp:
        json.dump(index, fp)

if __name__ == "__main__":
    main()
