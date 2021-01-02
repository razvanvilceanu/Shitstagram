"""

 Created by Razvan at 1/2/2021
 
 
"""

from insta_scraper import InstaBot


if __name__ == "__main__":
    bot = InstaBot(input("Instagram username: "))
    bot.complete_tour()