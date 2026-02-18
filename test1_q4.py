
def create_dict1(songs):
    # songs.keys = song names
    # songs.values = {"writers":[list], "perfomers":[list]}
    return_dict = {}
    #song_names["writers"]  = list
    #song_names["performers"] = list
    
    


songs = {
    "Rocket Man": {
    "writers": ["Elton John", "Bernie Taupin"],
    "performer":["Elton John"]
    },
    "Someone Like You": {
    "writers": ["Adele"],
    "performer": ["Adele"]
    },
    "Thinking Out Loud": {
    "writers": ["Ed Sheeran"],
    "performer": ["Ed Sheeran"]
    },
    }

print(create_dict1(songs))