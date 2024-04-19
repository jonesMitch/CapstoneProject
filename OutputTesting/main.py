import json

if __name__ == '__main__':
    #Test data
    nameJson = "TestStation"
    data = {
        "station": "Fargo",
        "inches of snow": None,
        "needs review": True
    }

    #Output
    file = open(".\JSONs\\" + nameJson + ".json", "w")
    json.dump(data, file, indent=3)
    file.close()