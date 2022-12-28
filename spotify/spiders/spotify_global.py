# This code script is written by @recberdeniz to exercise about python scrapy framework application for Python Programming
# This script is basically finding a top 200 song on global from Spotify and scraping with Scrapy Framework 
# For this script can describe that order, status, artist, song name, week info, streams, streams+
# and total of the first 200 songs on Spotify global list. For this scraping process, unfortunately, I did not use spotify.com
# Thus, data was scrapped from https://kworb.net, robots.txt file checked and data just used for exercise.
# 
# Postscript: Before using scrapy framework, please check the robots.txt for that website. Such as; https://kworbs.net/robots.txt

# Modules
import scrapy
import numpy as np
import pandas as pd


class SpotifyGlobalSpider(scrapy.Spider):
    name = 'spotify_global'
    start_urls = ['https://kworb.net/spotify/country/global_weekly.html'] #URL info
    # Lists for the DataFrame was created in here
    last_values = list()
    position = list()
    posStat = list()
    artist = list()
    song_name = list()
    weeks = list()
    peak = list()
    streams = list()
    streamsT = list()
    total = list()
    # List creating process end

    # Parse function
    def parse(self, response):
        new_values = list()
        names_song = list()
        count = 0
        # Here is, data table that includes position, status, artist, week, peak, x(?), streams, streams+ and total
        # values selected with css selector and it was 1800 row. There were some empty rows that required to scrape,
        # thus, "if" condition used for that
        for i in response.css("table tr td"):
            if i.css("::text"): 
               new_values.append(i.css("::text").extract_first())
            else:
               new_values.append("")
        # new_values (1800 rows) was splitted to 200 rows and 9 column array
        values_new = np.array_split(new_values, 200)
        #array to list process
        for i in [*values_new]:
           self.last_values.append(i.tolist())

        song_names = response.css("table tr td a::text").extract()
        # Song name lists extracted in this loop, 'a' tag has artist info and song name 
        # But first list has been artist info, so just song name info was required and scraped from 'a' tag
        for i in song_names:
            if count % 2 != 0:
                names_song.append(i)
            count += 1
        j = 0
        while(j < len(names_song)):
        # here is creating a dictionary for the data that use for json extracting
        # by the way lists are used for excel data extraction
            yield{
                'Pos': self.last_values[j][0],
                'Pos+': self.last_values[j][1],
                'Artist': self.last_values[j][2],
                'Names': names_song[j],
                'Wks': self.last_values[j][3],
                'Pk': self.last_values[j][4],
                'x(?)': self.last_values[j][5],
                'Streams': self.last_values[j][6],
                'Streams+': self.last_values[j][7],
                'Total': self.last_values[j][8],
            }
            self.position.append(self.last_values[j][0])
            self.posStat.append(self.last_values[j][1])
            self.artist.append(self.last_values[j][2])
            self.song_name.append(names_song[j])
            self.weeks.append(self.last_values[j][3])
            self.peak.append(self.last_values[j][4])
            self.peakT.append(self.last_values[j][5])
            self.streams.append(self.last_values[j][6])
            self.streamsT.append(self.last_values[j][7])
            self.total.append(self.last_values[j][8])
            j+=1

        # creating a data frame with pandas
        spotify_global = pd.DataFrame({'Position': self.position, 'Stat': self.posStat, 'Artist': self.artist, 
        'Song Name': self.song_name, 'Weeks': self.weeks, 'Streams': self.streams, 
        'Stream+': self.streamsT, 'Total': self.total}, index=range(1,201))
        # extracting the data frame to excel sheet that named Spotify_Top200_Global.xlsx 
        spotify_global.to_excel('Spotify_Top200_Global.xlsx', sheet_name='new_sheet_name')
