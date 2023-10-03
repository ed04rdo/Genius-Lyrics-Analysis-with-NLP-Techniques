from settings import CLIENT_ID,CLIENT_SECRET,CLIENT_ACCESS_TOKEN
from os import getcwd,chdir
from re import match
import json
import pandas as pd
import lyricsgenius
import requests

artist = 'Los Tigres Del Norte'
lyrics_dir = '\API_requests'

def main():
    working_dir_setup()
    #extract_data()
    json_to_df()

def working_dir_setup():
    chdir(getcwd()+lyrics_dir)

def extract_data():
    """
        save_lyrics() 
            saves Artist object as JSON in cwd, doesn't let you set it up
            if you want to save in in other location, you need to change cwd,
            thats the purpose of working_dir_setup()
    """
    try:
        genius = lyricsgenius.Genius(CLIENT_ACCESS_TOKEN)
        artist_request = genius.search_artist(artist,get_full_info=False)
        artist_request.save_lyrics(ensure_ascii=False)
    except requests.exceptions.Timeout:
        print("Timeout occurred")
    

def json_to_df():
    with open ('Lyrics_' + artist.replace(' ', '') + '.json',encoding='utf-8') as lyrics_file:
        data = json.load(lyrics_file)
        df =[]
        for song in data['songs']:
            temp_dict = {}
        
            try: 
                temp_dict["title"] = song["title"]
            except:
                temp_dict["title"] = None
            
            try: 
                date = str(song["release_date_components"]['year']) + '-' + str(song["release_date_components"]['month']).zfill(2) + '-' + str(song["release_date_components"]['day']).zfill(2)
                if match('^\d{4}-\d{2}-\d{2}$',date):
                    temp_dict["release_date"] = date
                else:
                    raise Exception
            except: 
                temp_dict["release_date"] = None
                
            try: 
                temp_dict["album"] = song["album"]["name"]
            except: 
                temp_dict["album"] = None
                
            try:     
                temp_dict["lyrics"] = song["lyrics"]
            except: 
                temp_dict["lyrics"] = None
            
            df.append(temp_dict)

    df = pd.DataFrame(df)
    df.to_csv(getcwd() + '/../datasets/' + artist.replace(' ','') + '_df.csv',index=False)


if __name__=="__main__":
    main()