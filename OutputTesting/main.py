import json
from datetime import date

if __name__ == '__main__':
    #Test data
    nameJson = "TestStation"
    today = date.today().strftime("%m/%d/%Y")
    data = {
        "station": "Fargo",
        "inches of snow": 10,
        "date": today
    }

    #Output
    file = open(nameJson + ".json", "w")
    json.dump(data, file, indent=3)
    file.close()