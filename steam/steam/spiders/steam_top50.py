# This code script is written by @recberdeniz to exercise about python scrapy framework application for Python Programming
# This script is basically finding a top seller games on steam and scraping with Scrapy Framework script for find 
# For this script can describe that name, publish date on steam, review score, discount and price of first 50 games on Steam top seller list
# Data was scrapped from https://steam.com, robots.txt file checked and data just used for exercise.
# 
# Postscript: Before using scrapy framework, please check the robots.txt for that website. Such as; https://steam.com.robots.txt

# Modules
import scrapy
import pandas as pd


class SteamSpider(scrapy.Spider):
    name = "steam"
    start_urls = [
        'https://store.steampowered.com/search/?filter=topsellers&ndl=1', # URL info
    ]
    game_name = list()
    publish_date = list()
    review_score = list()
    discount = list()
    price = list()
    # lists of data to export a excel sheet
    def parse(self, response):
        newDiscount = list()
        review_score = list()
        new_review = list()
        new_publish = list()
        exactPrice = list()
        # extracting a data from steam top seller table
        names = response.css("div.col.search_name.ellipsis span.title::text").extract() 
        for i in response.css("div.col.search_released.responsive_secondrow"):
            if i.css("::text"):
                new_publish.append(i.css("::text").extract_first())
            else:
                new_publish.append("")
        prices = response.css("div.col.search_price_discount_combined.responsive_secondrow::attr(data-price-final)").extract()
        for i in prices:
            exactPrice.append(int(i)*0.01)
        for i in response.css("div.col.search_discount.responsive_secondrow"):
              if i.css("span::text"):
                newDiscount.append(i.css("span::text").extract_first())
              else:
                newDiscount.append("")
        # in this loop, review score data are re-organized, because some of data has not review score
        # thus, if game has not review score, null character should insert to data row equality
        for i in response.css("div.col.search_reviewscore.responsive_secondrow"):
             if i.css("span.search_review_summary::attr(data-tooltip-html)"):
                review_score.append(i.css("span.search_review_summary::attr(data-tooltip-html)").extract_first())
             else:
                review_score.append("")
        # There were some html tag on review score data, this loop replace the tag with space
        for i in review_score:
            new_review.append(i.replace("<br>", " "))

        # process end of the data scrape from the steam top seller table
        count = 0
        # here is creating a dictionary for the data that use for json extracting
        # by the way lists are used for excel data extraction
        while(count < len(names)):
            yield{
                'Names': names[count],
                'Published Date': new_publish[count],
                'Review Score': new_review[count],
                'Discount': newDiscount[count],
                'Price': exactPrice[count],
            }
            self.game_name.append(names[count])
            self.publish_date.append(new_publish[count])
            self.review_score.append(new_review[count])
            self.discount.append(newDiscount[count])
            self.price.append(exactPrice[count])
            count+=1
        # end of dictionary and list processes
        # creating a data frame with pandas
        steam_topseller = pd.DataFrame({'Game Name': self.game_name, "Publish Date": self.publish_date, "Review Score": self.review_score, "Discount": self.discount, "Price": self.price},
            index=range(1,51))
        # extracting the data frame to excel sheet that named steam_topseller.xlsx    
        steam_topseller.to_excel('steam_topseller.xlsx', sheet_name='new_sheet_name')

