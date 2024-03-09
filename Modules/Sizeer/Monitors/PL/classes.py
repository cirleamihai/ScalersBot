import datetime, sys, string, random, requests, threading, os, sys, traceback
from bs4 import BeautifulSoup
from time import sleep, time
from dhooks import Webhook, Embed
from unipath import Path

import colorama
from colorama import Fore
colorama.init(autoreset=True)

cur_path = os.path.dirname(os.path.realpath(__file__))
cur_path = Path(cur_path).parent.parent

sys.path.append(cur_path)
# noinspection PyUnresolvedReferences
from sizeer import SizeerBOT

path_for_tools = cur_path.parent.parent + '\\Tools'
sys.path.append(path_for_tools)
# noinspection PyUnresolvedReferences
from bot_tools import BotTools, LoadProfiles

path_for_old_script = cur_path.parent.parent
sys.path.append(path_for_old_script)
# noinspection PyUnresolvedReferences
from ScalersBot_0_2_5 import SizeerBOT as OLDSizeerBOT

# noinspection PyUnresolvedReferences
from json_class import Json_kws

class SizeerMonitor:
    """

    A class used in order to monitor the web traffic

    Currently supports ... [to be updated]
    """

    def __init__(self, threads_number=5, #Number of Threads for Monitoring
                 number_of_preloads=15,
                 category="dunks"):
        """Defining the function"""
        self.number_of_threads = threads_number
        self.number_of_preloads = number_of_preloads
        self.category = category
        self.store_name = 'SIZEER PL'
        self.abreviation = "  [PL]"
        self.home_link = 'https://sklep.sizeer.com'
        self.new_item_found = False
        self.pulled_product = False

        self.checkout_module = SizeerBOT()
        self.done_checking = []
        self.queued_items = []
        self.queued_items_list_of_dicts = []

        self.discord_init()
        self.keywords_endpoint_prelucrator()
        self.unpack_old_items()

    def discord_init(self):
        """A function used in order to set the self discord values."""
        self.filtered_webhook_url_private = ''
        self.filtered_webhook_scalers = ''
        self.unfiltered_webhook_url_private = ''
        self.unfiltered_webhook_url_scalers = ''
        self.banner_image = ''

    def set_old_bot_conditions(self, prod_link, prod_sizes_number, prod_id):
        """

        Function used in order to check wether the new item is a profitable item or not.

        If it is, we are going to start the script for it.

        """
        worth_items_list = [
            'DD1872-100',
            'DD1503-101',
            'DD1391-100',
            'DD1503-105',
            'DM9467-500',
            'DD1503-103',
            'DD1503-102',  # Orange Pearls
            'DD1503-108',  # Bordeaux
            'DD1873-102',  # NEXT NATURES BW
            'DD1873-100',  # NEXT NATURES LIGHT PINK/ PALE CORAL
            'DN1431-101',  # NEXT NATURES GYM RED
            'DD1503-116',  # Light Violet
            'DD1391-101',  # Spartan Greens
            'DD1503-107',  # Fosils
            'DD1391-102',  # UNCs
            'DD1391-104',  # Court Purples
            'DD1391-700',  # Michigans
            'DD1391-003',  # GeorgeTowns
            'DD1503-800',  # Laser Orange
            'DD1391-103',  # Grey Fogs
            'DD3363-100',  # EMBs Reds
            'DD1503-114',  # Harvest Moons
            'DO6485-600',  # Velvet Pinks GS
            'CW1590-700',  # Michigans GS
            'CW1590-103',  # UNCs GS
            'DO3806-100',  # Halloween GS
            'CW1590-102',  # Spartan Greens GS
            'CW1590-004',  # Georgetowns GS
            'CW1590-100',  # Pandas GS
            'CW1590-601',  # Pink Foams GS
            'DO6723-800',  # Winter Solstice
            'DD1503-111',  # Archeo Pinks
            'CW1590-600',  # Championship Reds GS
            'DD1391-600',  # Championship Reds
            'DD1869-110',  # Pink Prime Highs
            'DD3357-100',  # Halloween Dunks
            'DD1869-107',  # Alluminium Highs
        ]

        special_items_list = [
            'BQ6472-105',  # Mids Wolf Grey
            'CW5379-600',  # Mids Digital Pinks
            'DC9517-600',  # Mids Arctic Pinks 2021
            'BQ6472-015',  # Mids Light Smoke Grey 2021 !!
            'BQ6472-500',  # Mids Violet Purple
            '554724-173',  # Mids Chicago 2020
            '554724-069',  # Mids Chicago Toe 2019
            '554724-074',  # Mids Banned 2021
            '554725-074',  # Mids Banned 2021 Gs
            'CZ4385-016',  # Mids Betroots
            'BQ6472-500',  # Mids Barely Roses
            'BQ6472-800',  # Mids Barely Orange
            'CZ0774-300',  # Mids Dutch Green
            '554724-092',  # Mids Light Smoke Greys 2019
            '554725-092',  # Mids Light Smoke Greys 2019 GS
            'DO7440-821',  # Mids Dark Pony Smoky Mauve
            'CW1140-100',  # Mids Multi Color
            '554724-073',  # Mids Shadow White Black
            '554725-073',  # Mids Shadow White Black GS
            'DC9035-100',  # Mids Camo Grey
            'DH4270-800',  # Mids Apricot
            '554724-075',  # Mids Chile
            '554725-075',  # Mids Chile Gs
            'BQ6472-104',  # Mids Kentucky
            '554724-078',  # Mids Light Smoke Grey Anthrachite 2022
            '55472-371',  # Mids Dark Teals GS
            '554725-411',  # Mids Dark Teal GS
            '554724-140',  # Mids Racer Blue
            '554725-140',  # Mids Racer Blue GS
            '554725-133',  # Mids Crimson Tint GS
            '554724-411',  # Mids Dark Teal Mens
            '554724-122',  # Mids Gym Reds Mens
            'DJ4695-122',  # Mids Gym Reds GS
            '554724-116',  # Mids White Gym Red Mens
            'DC7294-103',  # Mids Grey Green Mens
            'DC7248-103',  # Mids Grey Green GS
            'DD3235-100',  # Mids Camo Grey GS
            '554724-082',  # Mids Linen
            'DR0174-500',  # Mids V-Day Special
            'DH6933-100',  # Mids Diamond Short
            'DN4045-001',  # Mids Iron Ore
            'DC7267-500',  # Mids Berry Pink
            'DN4346-100',  # Mids Coconut Milk Particle Grey GS
            'DN4281-100',  # Mids Coconut Milk Particle Grey
            'BQ6472-121',  # Mids Coconut Milk
            '554724-271',  # Mids Temps Tan White
            'DO7440-821',  # Mids Dark Pony Smoky
            '852542-801',  # Mids Hyper Pink
            '554725-132',  # Mids Igloos
            '852542-105',  # Mids SE Purple
            '553558-030',  # Lows Smoke Greys
            '553560-030',  # Lows Smoke Greys GS
            'DH4269-100',  # Lows Elephant Greys
            'DC0774-105',  # Lows Wolf Grey
            'AO9944-441',  # Lows UNC
            'DC0774-050',  # Lows Uni Blue 2022
            '553558-144',  # Lows UNC 2021
            'CZ0790-801',  # Lows Starfish
            'CZ0775-801',  # Lows Starfish Womens
            'CZ0858-801',  # Lows Starfish GS
        ]

        test = []
        atack_speed = "attack speed"

        if prod_id in test:
            SizeerBOT().run_script(number_of_tasks=1,
                                   product_link=prod_link,
                                   max_retries_limit=15,
                                   max_checkouts=30,
                                   number_of_preloads=0,
                                   continue_checkouts=True,
                                   from_monitor=True,
                                   mode=atack_speed)

        if prod_id in worth_items_list:
            if prod_sizes_number == 1:
                SizeerBOT().run_script(number_of_tasks=20,
                                       product_link=prod_link,
                                       max_retries_limit=10,
                                       number_of_preloads=0,
                                       continue_checkouts=True,
                                       from_monitor=True,
                                       mode=atack_speed)

            elif prod_sizes_number > 1 and prod_sizes_number <= 4:
                SizeerBOT().run_script(number_of_tasks=35,
                                       product_link=prod_link,
                                       max_retries_limit=15,
                                       number_of_preloads=0,
                                       from_monitor=True,
                                       continue_checkouts=True,
                                       full_throttle=True,
                                       mode=atack_speed)

            else:
                SizeerBOT().run_script(number_of_tasks=50,
                                       product_link=prod_link,
                                       max_retries_limit=25,
                                       number_of_preloads=0,
                                       from_monitor=True,
                                       continue_checkouts=True,
                                       full_throttle=True,
                                       mode=atack_speed)

        elif prod_id in special_items_list:
            if prod_sizes_number == 1:
                SizeerBOT().run_script(number_of_tasks=15,
                                       product_link=prod_link,
                                       max_retries_limit=10,
                                       max_checkouts=20,
                                       number_of_preloads=0,
                                       continue_checkouts=True,
                                       from_monitor=True,
                                       mode=atack_speed)

            elif prod_sizes_number > 1 and prod_sizes_number <= 4:
                SizeerBOT().run_script(number_of_tasks=30,
                                       product_link=prod_link,
                                       max_retries_limit=15,
                                       max_checkouts=45,
                                       number_of_preloads=0,
                                       from_monitor=True,
                                       continue_checkouts=True,
                                       full_throttle=True,
                                       mode=atack_speed)

            else:
                SizeerBOT().run_script(number_of_tasks=40,
                                       product_link=prod_link,
                                       max_retries_limit=25,
                                       max_checkouts=60,
                                       number_of_preloads=0,
                                       from_monitor=True,
                                       continue_checkouts=True,
                                       full_throttle=True,
                                       mode=atack_speed)

    def keywords_endpoint_prelucrator(self):
        """
        A function used in order to prelucrate the keywords

        filename: File Path to a JSON Arranged List of Dicts.

        """
        if self.category == 'dunks':
            self.filename = 'dunks.json'
            self.endpoint = 'https://sklep.sizeer.com/nike-dunk'
        else:
            self.filename = 'jordans.json'
            self.endpoint = 'https://sklep.sizeer.com/jordan-air-1'

        self.json_items = Json_kws(self.filename)

    def unpack_old_items(self):
        """Using Json Class, we unpack the old prods"""
        # If the file doesn't exist, we create the list and pass it as NULL
        try:
            self.old_prods_list = self.json_items.load_old_items()
            self.old_prods_len = len(self.old_prods_list)

        except:
            self.old_prods_list = []
            self.old_prods_len = 0

    def start_tasks(self):
        """A function used in order to start the tasks"""
        for thread_number in range(0, self.number_of_threads):
            threading.Thread(target=self.run_monitor, args=[thread_number]).start()

            self.done_checking.append(False)
            sleep(0.15)

        threading.Thread(target=self.initialize_queue, args=[]).start()

    def initialize_queue(self):
        """A function that disbables all pings for the same items for 30 seconds"""
        while True:
            increment = 0
            queued_len = len(self.queued_items_list_of_dicts)

            # Iterating through each element to see wether we have to remove it from queue
            while increment < queued_len:
                item = self.queued_items_list_of_dicts[increment]
                product = item["product"]
                time_added = item["time_added"]
                time_ago_added = int(time()) - time_added

                if time_ago_added >= 30:
                    self.queued_items.remove(product)
                    self.queued_items_list_of_dicts.remove(item)
                    queued_len -= 1

                else:
                    increment += 1

            sleep(1)

    def run_monitor(self, thread_number):
        """

        A function used in order to run the monitor

        This function will loop for as long as the application lasts

        """
        while True:
            client = BotTools().create_client(filename="monitoring_proxies.txt")
            user_agent = BotTools().get_user_agents()

            # 1. First Step -> Get the starting cookies
            client = self.set_starting_cookies(client, user_agent, thread_number)
            if not client:
                continue

            # 2. Second Step -> Scrape the page for changes
            self.scrape_items(client, user_agent, thread_number)

            # @todo: connect SizeerBot to module
            # @todo: finish prelaod mode for web

    def set_starting_cookies(self, client, user_agent, thread_number):
        """A function used in order to set the starting cookies dict"""
        logs = "Setting Cookies..."
        BotTools().print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX,
                              thread_number, task_mode="SCRAPER", thread_number=thread_number)

        length = 5
        ran1 = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=length))
        ran2 = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=length))

        url = f'https://sklep.sizeer.com/manifest.json?{ran1}={ran2}'
        headers = {
            'authority': 'sklep.sizeer.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'user-agent': user_agent,
            'accept': '*/*',
            'sec-gpc': '1',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'manifest',
            'accept-language': 'en-US,en;q=0.9',
            'dnt': '1'
        }

        try:
            response = client.get(url, headers=headers, timeout=7)

        except:
            logs = "Error setting session cookies... [TIMED OUT]"
            BotTools().print_logs(logs, self.store_name, Fore.RED, thread_number,
                                  task_mode="SCRAPER", thread_number=thread_number)

            return False

        return client

    def scrape_items(self, client, user_agent, thread_number):
        """A function used in order to scrape the web version"""
        iterator = 0
        prods_number = 0
        new_item_found_local = False

        ran1 = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=random.randint(3, 10)))
        ran2 = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=random.randint(3, 10)))
        url = self.endpoint + f"?{ran1}{ran2}"

        headers = {
            'authority': 'sklep.sizeer.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'user-agent': user_agent,
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-gpc': '1',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'reffer': 'https://sklep.sizeer.com/manifest.json',
            'accept-language': 'en-US,en;q=0.9',
        }

        try:
            response = client.get(url, headers=headers, timeout=15)

        except:
            logs = f"Error Scraping Products. [TIMED OUT] [{self.category}]"
            BotTools().print_logs(logs, self.store_name, Fore.RED, thread_number,
                                  task_mode="SCRAPER", thread_number=thread_number)

        else:
            if int(response.status_code) == 200:
                prod_id_dict_list = []

                soup_response = BeautifulSoup(response.text, 'lxml')
                products_list = soup_response.find_all('div', attrs={"data-brand": "Nike"})

                for product in products_list:
                    product_dict = {}
                    self.done_checking[thread_number] = False

                    sizes_no = product.find_all('span', class_='b-itemList_sizesItem')
                    prod_sizes_no = len(sizes_no)

                    if prod_sizes_no:
                        product_id = product['data-ga-id']
                        product_title = product['data-ga-name']
                        prods_number += 1

                        prod_id_dict = {}
                        prod_id_dict[product_title] = product_id
                        prod_id_dict_list.append(prod_id_dict)

                        if prod_id_dict not in self.old_prods_list and prod_id_dict not in self.queued_items:
                            # We announce the other threads that we have found a new product
                            self.old_prods_list.insert(iterator, prod_id_dict)
                            self.old_prods_len += 1

                            #Adding the item in the queue so we don't ping it within the next 30 seconds
                            queued_dict = {
                                "product": prod_id_dict,
                                "time_added": int(time())
                            }
                            self.queued_items_list_of_dicts.append(queued_dict)
                            self.queued_items.append(prod_id_dict)

                            logs = f"New Item Found! [{product_title}] [{prod_sizes_no} sizes loaded]"
                            BotTools().print_logs(logs, self.store_name, Fore.LIGHTGREEN_EX,
                                                  thread_number, task_mode="SCRAPER", thread_number=thread_number)

                            self.new_item_found = True
                            new_item_found_local = True
                            product_price = product['data-price'] + ' PLN'
                            bot_prod_link = self.home_link + product.find('a', class_='b-itemList_photoLink')['href']
                            product_link = bot_prod_link + f'?highscam_items_id_new={ran1}'

                            product_image = 'https://images.weserv.nl/?url=' + \
                                             self.home_link + \
                                             product.find('img', class_='b-itemList_photoMain b-lazy js-offer-photo')['data-src']

                            # A thread which checks wether we should start the bot for this product or not
                            #threading.Thread(target=self.set_old_bot_conditions,
                            #                 args=[bot_prod_link, prod_sizes_no, product_id]).start()

                            resell_platforms = self.stockx_klekt_links_getter(product_id)
                            hooks = self.webhook_filtered_unfiltered_setter(product_title, product_id)
                            embed_title = product_title + self.abreviation

                            minimalEmbed = Embed(
                                color=0x000000,
                                title=embed_title,
                                url=product_link,
                            )

                            minimalEmbed.set_author(name="New Item Found")
                            minimalEmbed.set_thumbnail(product_image)
                            minimalEmbed.add_field(name="**PRICE**", value=product_price, inline=True)
                            minimalEmbed.add_field(name="**StockX/ Klekt**", value=resell_platforms, inline=True)
                            minimalEmbed.add_field(name="**PID**", value=product_id, inline=True)
                            minimalEmbed.set_footer(
                                text=f"Written & performed by Cirlea Mihai • {datetime.datetime.now()}",
                                icon_url=self.banner_image)

                            for hook in hooks:
                                hook.send(embed=minimalEmbed)

                            try:
                                self.ping_detailed_item(client, user_agent, resell_platforms, product_link,
                                                        product_title, product_price, product_image, hooks)

                                logs = f"Printed ATC details! [{product_title}]"
                                BotTools().print_logs(logs, self.store_name, Fore.LIGHTGREEN_EX,
                                                      thread_number, task_mode="SCRAPER", thread_number=thread_number)

                            except:
                                logs = f"Failed printing ATC details! [TIMED OUT] [{product_title}]"
                                BotTools().print_logs(logs, self.store_name, Fore.RED,
                                                      thread_number, task_mode="SCRAPER", thread_number=thread_number)

                    iterator += 1

                self.done_checking[thread_number] = True

                if self.new_item_found:
                    self.json_items.write_new_items(self.old_prods_list)

                    self.new_item_found = False

                if not len(products_list):
                    logs = f"No products Loaded. Monitoring FrontEnd... [{response.status_code}]"
                    BotTools().print_logs(logs, self.store_name, Fore.LIGHTBLUE_EX,
                                          thread_number, task_mode="SCRAPER", thread_number=thread_number)

                    return

                if not new_item_found_local:
                    if prods_number == self.old_prods_len:
                        # Means nothing changed
                        logs = f"Monitoring FrontEnd... [{response.status_code}] [{self.old_prods_len}]"
                        BotTools().print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX,
                                              thread_number, task_mode="SCRAPER", thread_number=thread_number)
                    elif prods_number < self.old_prods_len:
                        # Means a product has been pulled:
                        self.ping_pulled_products(prod_id_dict_list, response, thread_number)
                    else:
                        # Means that we have an item that got removed or added from one instance
                        # but the othes didn't recognize it
                        logs = f"Monitoring FrontEnd... [{response.status_code}] " \
                               f"[{self.old_prods_len}] [{len(self.queued_items)} queued] [ADD]"
                        BotTools().print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX,
                                              thread_number, task_mode="SCRAPER", thread_number=thread_number)

            else:
                logs = f"WRONG RESPONSE CODE [{response.status_code}]"
                BotTools().print_logs(logs, self.store_name, Fore.RED, thread_number,
                                      task_mode="SCRAPER", thread_number=thread_number)

    def ping_pulled_products(self, prod_id_dict_list, response, thread_number):
        """
        Function used in order to check for the pulled items.

        Current Usage:
            -checks for each item from the json list to see if it still appears on the page.
            -if it doesn't appear anymore, we remove it from our list

        """
        iterator = 0
        pulled = False

        while not all(self.done_checking):
            sleep(0.1)

        self.done_checking[thread_number] = False

        while iterator < self.old_prods_len:
            # We iterate throught each old product
            old_product = self.old_prods_list[iterator]

            if old_product not in prod_id_dict_list and old_product not in self.queued_items:
                #If the old product is not in the new list, means it got pulled
                pulled_product = list(old_product.keys())[0]

                # We announced it and then we continue
                logs = f"Product pulled from the page [{old_product}]"
                BotTools().print_logs(logs, self.store_name, Fore.LIGHTMAGENTA_EX,
                                      thread_number, task_mode="SCRAPER", thread_number=thread_number)

                self.pulled_product = True

                # Adding the item in the queue so we don't ping it within the next 30 seconds
                queued_dict = {
                    "product": old_product,
                    "time_added": int(time())
                }
                self.queued_items_list_of_dicts.append(queued_dict)
                self.queued_items.append(old_product)

                # We remove the product from the list
                self.old_prods_list.remove(old_product)
                self.old_prods_len -= 1

                pulled = True
            else:
                #Otherwise, we continue with the next item
                iterator += 1

        if self.pulled_product:
            self.json_items.write_new_items(self.old_prods_list)

            self.pulled_product = False
        else:
            # Means that we have an item that got removed or added from one instance
            # but the othes didn't recognize it
            logs = f"Monitoring FrontEnd... [{response.status_code}] " \
                   f"[{self.old_prods_len}] [{len(self.queued_items)} queued] [PULL]"
            BotTools().print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX,
                                  thread_number, task_mode="SCRAPER", thread_number=thread_number)

        self.done_checking[thread_number] = True

    def get_item_details(self, client, user_agent, prod_link):
        """Accessing the item's page to see the sizes and get the ATC Links"""
        headers = {
            'authority': 'sklep.sizeer.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'user-agent': user_agent,
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-gpc': '1',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': self.endpoint,
            'accept-language': 'en-US,en;q=0.9',
        }

        #GET Request
        prod_response = client.get(prod_link, headers=headers, timeout=10)

        soup_response = BeautifulSoup(prod_response.text, 'lxml')
        sizes_raw_list = soup_response.find_all('p', class_='m-productDescr_sizeItem')

        atc_pattern_list = []
        sizes_list = []

        for one_size in sizes_raw_list:
            #Getting the sizes and the atc patterns
            size = one_size.a.text.split()
            sizes_list.append(size[0])

            atc_pattern = one_size.a['data-carturl']
            atc_pattern_list.append(atc_pattern)

        atc_string = self.create_atc_string_discord(sizes_list, atc_pattern_list)

        return atc_string

    def create_atc_string_discord(self, sizes_list, atc_pattern_list):
        """Creating the atc string"""
        home_link = 'https://sklep.sizeer.com'
        sizes_no = len(sizes_list)
        column_list = []

        first_column = int(sizes_no / 2)
        if first_column != sizes_no / 2:
            first_column += 1

        first_column_str = ""
        second_column_str = ""

        iterator = 0

        for size in sizes_list:
            if iterator < first_column:
                atc_link_per_size = f"{home_link}{atc_pattern_list[iterator]}"
                first_column_str += f"[{size}]({atc_link_per_size})\n"
            else:
                atc_link_per_size = f"{home_link}{atc_pattern_list[iterator]}"
                second_column_str += f"[{size}]({atc_link_per_size})\n"

            iterator += 1

        column_list.extend([first_column_str, second_column_str])

        return column_list

    def ping_detailed_item(self, client, user_agent, resell_platforms, prod_link,
                           prod_title, prod_price, prod_image, hooks):
        """Ping the item with the atc feature aswell"""
        prod_atc_script = self.get_item_details(client, user_agent, prod_link)
        first_collumn_atc = prod_atc_script[0]
        second_collumn_atc = prod_atc_script[1]
        embed_title = prod_title + self.abreviation
        pl_region = "[PL   :flag_pl:](https://sklep.sizeer.com/)"

        utilities = self.create_utilities()

        fullEmbed = Embed(
            color=0x000000,
            title=embed_title,
            url=prod_link,
        )

        if first_collumn_atc:
            fullEmbed.add_field(name="**SIZES**", value=first_collumn_atc, inline=True)

        if second_collumn_atc:
            fullEmbed.add_field(name="**SIZES**", value=second_collumn_atc, inline=True)

        fullEmbed.add_field(name="**PRICE**", value=prod_price, inline=True)
        fullEmbed.set_thumbnail(prod_image)
        fullEmbed.add_field(name="**StockX/ Klekt**", value=resell_platforms, inline=True)
        fullEmbed.add_field(name="**REGION**", value=pl_region, inline=True)
        fullEmbed.add_field(name="**UTILITIES**", value=utilities, inline=False)
        fullEmbed.set_footer(text=f"Written & performed by HigHScam#0001 • {datetime.datetime.now()}",
                             icon_url=self.banner_image)

        for hook in hooks:
            hook.send(embed=fullEmbed)

    def stockx_klekt_links_getter(self, id):
        """Creating the links of StockX and Klekt"""
        stockx_searching_link = 'https://stockx.com/search?s='
        klekt_searching_link = 'https://www.klekt.com/store/pattern,'

        stockx_searching_link += str(id)
        klekt_searching_link += str(id)

        embed_str = f"[StockX]({stockx_searching_link})/ [Klekt]({klekt_searching_link})"

        return embed_str

    def create_utilities(self):
        """Creating the UTILITIES Field with different links"""
        #Links
        checkout_last_step = 'https://sklep.sizeer.com/koszyk/podsumowanie'
        login_link = 'https://sklep.sizeer.com/login'
        address = 'https://sklep.sizeer.com/koszyk/adres'

        useful_links = f"[LOGIN]({login_link}) | " \
                       f"[ADDRESS]({address}) | " \
                       f"[CHECKOUT LAST STEP]({checkout_last_step}) |"
        return useful_links

    def webhook_filtered_unfiltered_setter(self, prod_title, prod_id):
        """We are setting up the webhook and checking for size changes to filtered items"""
        # if its filtered, we send it to the required channel
        filtered_item = self.keywords_filter(prod_title, prod_id)
        hooks = []

        if filtered_item:
            private_hook = Webhook(self.filtered_webhook_url_private)
            scalers_hook = Webhook(self.filtered_webhook_scalers)

        else:
            private_hook = Webhook(self.unfiltered_webhook_url_private)
            scalers_hook = Webhook(self.unfiltered_webhook_url_scalers)

        hooks = [private_hook, scalers_hook]

        return hooks

    def keywords_filter(self, product, prod_id):
        """Filtering out the good and the bad items and then sending the webhook"""
        keywords_list = self.json_items.load_keywords()

        product = product.lower()
        true_false_list = []

        for keywords in keywords_list:
            true_false_list = []

            #Going through the list of lists
            for word in keywords:
                if '+' == word[0]:
                    true_false_list.append(word[1:] in product or word[1:] == prod_id)
                elif '-' == word[0]:
                    true_false_list.append(not word[1:] in product
                                           and str(word[1:]).lower() != str(prod_id).lower())

            if all(true_false_list):
                break

        if all(true_false_list):
            #Checking to see wether the product that we are checking is in the list, if not, we are going
            #to exclude it next time it's readded since sizeer likes to readd lots of trash
            excluded_prod_id = f"-{prod_id}"
            if excluded_prod_id not in keywords_list[0]:
                keywords_list[0].append(excluded_prod_id)

            #We then dump the updated list back in the json file
            self.json_items.dump_keywords(keywords_list)

            return True

        else:
            return False