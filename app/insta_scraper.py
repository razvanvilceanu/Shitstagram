from selenium import webdriver
from time import sleep
from app.email_handle.email_handler import (get_contacts,
                                        send_email)
from app.compare_last_files import (import_data,
                                    files_to_lists,
                                    get_unfollowers,
                                    get_new_followers)
import datetime
import os



class InstaBot:

    def __init__(self, usr, email_password = input("Enter your email password: "), instagram_password=input("Enter your Instagram password: "), sender=input("Enter your email address: ")):
            self.email_sender = sender
            self.email_password = email_password
            self.instagram_passowrd = instagram_password
            self.usr = usr


    def start_scraping(self):

        """Init function. Takes the bot from opening the browser to getting and saving the followers"""


        self.driver = webdriver.Firefox()
        self.driver.get("https://instagram.com")
        sleep(3)

        self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/button[1]').click()
        sleep(3)

        self.driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input").send_keys(self.usr)
        sleep(3)

        self.driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input").send_keys(self.instagram_passowrd)
        sleep(3)

        self.driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button/div").click()
        sleep(3)

        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div/div/button").click()
        sleep(3)

        self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]").click()
        sleep(3)

        self.driver.find_element_by_xpath(
            "/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[5]/span/img").click()
        sleep(3)

        self.driver.find_element_by_xpath(
            "/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[5]/div[2]/div[2]/div[2]/a[1]/div/div[2]/div/div/div/div").click()
        sleep(3)



    def get_followers(self):

        """Function which opens the followers list, scrolls through them and stores them in a separate variable.
            Uses the number of followers to filter the people added from the suggestion pane."""

        flw = int((
            (self.driver.find_element_by_css_selector(
                "li.Y8-fY:nth-child(2) > a:nth-child(1) > span:nth-child(1)").text)))
        sleep(2)

        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a").click()
        sleep(1)

        scroll_box = self.driver.find_element_by_css_selector(".isgrP")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(2)

            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        followers = [names[e] for e in range(flw)]
        print("Having %s followers" % len(followers))
        print(followers)

        self.followers = followers
        self.driver.find_element_by_css_selector(
            "div.WaOAr:nth-child(3) > button:nth-child(1) > div:nth-child(1) > svg:nth-child(1)") \
            .click()
        return followers


    def save_followers(self):

        """Function to save the followers data in a new file."""

        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d-%H-%M")


        if not os.path.exists(os.path.join(os.getcwd(), '..//data' ,str(self.usr))):
            os.makedirs('../data/' + self.usr)

        with open('../data/{}/'.format(self.usr) + now + '.txt', 'w') as file:
            file.write("Followers: " + str(len(self.followers)) + "\n")
            for e in self.followers:
                file.write(e + "\n")


    def complete_tour(self):
        self.start_scraping()
        sleep(3)
        self.get_followers()
        sleep(3)
        self.save_followers()
        sleep(1)

        first, second = import_data(PATH='../data/' + self.usr)
        first, second = files_to_lists(first, second)
        followers = get_new_followers(first, second)
        unfollowers = get_unfollowers(first, second)

        names, emails = get_contacts('email_handle/email_list')
        for e in range(len(names)):
            send_email(followers, unfollowers, emails[e], self.usr, self.email_password, self.email_sender)

