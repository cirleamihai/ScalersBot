import os, requests, random, datetime, zipfile, colorama, csv
from unipath import Path
from selenium import webdriver
from dhooks import Webhook, Embed

from colorama import Fore
colorama.init(autoreset=True)

global cur_path, BOT_VERSION, supreme_keywords
supreme_keywords = "+logo,+camo,+m-65"
BOT_VERSION = '0.3'
cur_path = os.path.dirname(os.path.realpath(__file__))

p = Path(cur_path)
cur_path = p.parent

class BotTools:
    """

    A class representing all the necessary tools that we are going
    to use in the bot to different modules

    """

    @staticmethod
    def get_user_agents():
        """A function used in order to get the user agents"""
        user_agents = []

        try:
            with open(f'{cur_path}\\Tools\\user_agents.txt') as f:
                user_agents = f.readlines()

        except:
            # traceback.print_exc()
            print(f'[{datetime.datetime.now()}]\tFailed to load User Agents.')
            pass
        random_ua = random.choice(user_agents)[:-2]

        return random_ua

    @staticmethod
    def get_proxies_data(filename=""):
        """We proccess the proxies data by a bit"""
        proxy_list = []
        if not filename:
            filename = 'proxies.txt'

        try:
            with open(f'{cur_path}\\Tools\\{filename}') as f:
                unpr_proxies_list = f.readlines()
                for unpr_proxy in unpr_proxies_list:
                    unpr_proxy = unpr_proxy.split('\n')[0]
                    part_of_proxy_list = unpr_proxy.split(':')

                    proxy = 'http://' + part_of_proxy_list[2] + ':' + part_of_proxy_list[3] + \
                            '@' + part_of_proxy_list[0] + ':' + part_of_proxy_list[1]

                    proxy_list.append(proxy)

            return proxy_list
        except:
            # traceback.print_exc()
            print(f'[{datetime.datetime.now()}]\tFailed to load proxies. Check your file: 1 proxy/ line.')
            pass

    def pick_random_proxy_tls(self, filename=""):
        proxies_list = self.get_proxies_data(filename)
        random_proxy = random.choice(proxies_list)
        random_proxy += '/'

        return random_proxy

    def pick_random_proxy(self, filename=""):
        """We pick a random proxy from the list"""
        proxy_list = self.get_proxies_data(filename)
        try:
            random_index = random.randint(0, len(proxy_list))
            proxy_dict = {}

            proxy = proxy_list[random_index - 1]
            proxy_dict['https'] = proxy
            proxy_dict['http'] = proxy

            return proxy_dict
        except:
            # traceback.print_exc()
            return ''

    def create_client(self, filename=""):
        """A function used in order the create the Requests Client"""
        try:
            # Getting the proxies.txt we are going to pass to the client
            random_proxies = self.pick_random_proxy(filename)

            client = requests.Session()
            client.proxies = random_proxies

            return client
        except:
            print(f"[{datetime.datetime.now()}]\tFailed to create client.")

    def create_browser(self, user_agent, proxy, caps):
        """A function used to create a browser with proxy option"""
        if proxy:
            # Setting up the Chrome Driver...
            proxy = proxy['https'].split('http://')[1]
            user = proxy.split('@')[0].split(':')[0]
            pswd = proxy.split('@')[0].split(':')[1]

            host = proxy.split('@')[1].split(':')[0]
            port = proxy.split('@')[1].split(':')[1]

            PROXY_HOST = host
            PROXY_PORT = port
            PROXY_USER = user
            PROXY_PASS = pswd

            self.manifest_json = """
                    {
                        "version": "1.0.0",
                        "manifest_version": 2,
                        "name": "Chrome Proxy",
                        "permissions": [
                            "proxy",
                            "tabs",
                            "unlimitedStorage",
                            "storage",
                            "<all_urls>",
                            "webRequest",
                            "webRequestBlocking"
                        ],
                        "background": {
                            "scripts": ["background.js"]
                        },
                        "minimum_chrome_version":"22.0.0"
                    }
                    """

            self.background_js = """
                    var config = {
                            mode: "fixed_servers",
                            rules: {
                              singleProxy: {
                                scheme: "http",
                                host: "%s",
                                port: parseInt(%s)
                              },
                              bypassList: ["localhost"]
                            }
                          };

                    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

                    function callbackFn(details) {
                        return {
                            authCredentials: {
                                username: "%s",
                                password: "%s"
                            }
                        };
                    }

                    chrome.webRequest.onAuthRequired.addListener(
                                callbackFn,
                                {urls: ["<all_urls>"]},
                                ['blocking']
                    );
                    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

            chrome_opt = self.get_chrome_options(use_proxy=True, user_agent=user_agent)
            driver = webdriver.Chrome(desired_capabilities=caps, executable_path=f'{cur_path}\Browser\chromedriver.exe',
                                      options=chrome_opt)

        else:

            driver = webdriver.Chrome(desired_capabilities=caps, executable_path=f'{cur_path}\Browser\chromedriver.exe')

        return driver

    def get_chrome_options(self, use_proxy=False, user_agent=None):
        """Setting Proxy"""
        chrome_options = webdriver.ChromeOptions()

        if use_proxy:
            pluginfile =f'{cur_path}\Browser\proxy_auth_plugin.zip'

            with zipfile.ZipFile(pluginfile, 'w') as zp:
                zp.writestr("manifest.json", self.manifest_json)
                zp.writestr("background.js", self.background_js)
            chrome_options.add_extension(pluginfile)

        if user_agent:
            chrome_options.add_argument('--user-agent=%s' % user_agent)

        return chrome_options

    def send_webhook(self, checkout_message, product_image, product_link, product_name, product_price, product_size,
                     product_pid, payment_method, task_mode, task_number, checkout_time, order_number, number_of_fails,
                     premature_cookie_bool, email):

        webhook = ''
        # image = 'https://images.weserv.nl/?url=' + 'https://sizeer.ro/media/cache/gallery/rc/qqxijlw1/nike-dunk-low-retro-barbati-pantofi-sport-negru-dd1391-100.jpg'
        bot_image = 'https://cdn.discordapp.com/attachments/864930808448286771/880074329818288199/logo.jpg'

        Embed_succes = Embed(
            color=0x000000,
            title=checkout_message,
            url=product_link,
        )

        hook = Webhook(webhook)

        Embed_succes.set_thumbnail(product_image)
        # Embed_succes.set_author(name="SIZEER")
        Embed_succes.add_field(name="Product", value=f"||{product_name}||", inline=True)
        Embed_succes.add_field(name="Price", value=f"||{product_price}||", inline=True)
        Embed_succes.add_field(name="Size", value=product_size, inline=True)
        Embed_succes.add_field(name="PID", value=f"||{product_pid}||", inline=True)
        Embed_succes.add_field(name="Payment Method", value=f"||{payment_method}||", inline=True)
        Embed_succes.add_field(name="Task Mode", value=f"||{task_mode}||", inline=True)
        Embed_succes.add_field(name="Task Number", value=f"||Task Number {task_number}||", inline=True)
        Embed_succes.add_field(name="Checkout Time", value=f"||{checkout_time} seconds||", inline=True)
        Embed_succes.add_field(name="Order Number", value=f"||{order_number}||", inline=True)
        Embed_succes.add_field(name="Number of Fails", value=f"||{number_of_fails} retries||", inline=True)
        Embed_succes.add_field(name="Premature Cookie", value=f"||{premature_cookie_bool}||", inline=True)
        Embed_succes.add_field(name="Email", value=f"||{email}||", inline=True)
        Embed_succes.set_footer(text=f"ScalersBot • VERSION {BOT_VERSION} • {datetime.datetime.now()}",
                                icon_url=bot_image)

        hook.send(embed=Embed_succes)

    def keywords_filter(self, product, prod_id=''):
        """Filtering out the good and the bad items so that it matches our criteria"""
        keywords_list = supreme_keywords.split(',')

        product = product.lower()
        true_false_list = []

        for keywords in keywords_list:
            if '+' == keywords[:1]:
                true_false_list.append(keywords[1:] in product)
            elif '-' == keywords[:1]:
                true_false_list.append(not keywords[1:] in product
                                       and str(keywords[1:]).lower() != str(prod_id).lower())

        if all(true_false_list):
            return True

        else:
            return False

    def print_logs(self, logs, store, chosen_color, task_number='', task_mode='', thread_number=''):
        store = f"[{store}]"
        time = f" [{datetime.datetime.now()}]\t"

        if str(task_number) != "":
            task_number = f' [TASK NUMBER {task_number}]'

        if str(thread_number) != "":
            task_number = f" [THREAD {thread_number}]"

        if task_mode:
            task_mode = f" [{task_mode}] "

        # Printing logs on the txt file
        log_for_file = f"{store}{task_mode}{task_number}{time}" + logs + "\n"
        filename = f"{cur_path}\\Tools\\logs.txt"

        if str(thread_number) == "":
            with open(filename, 'a', encoding='utf-8') as mytxt:
                mytxt.write(log_for_file)

        print(Fore.LIGHTCYAN_EX + f"{store}{task_mode}{task_number}{time}" +
              chosen_color + logs)

    def get_dummy_link(self, filename='dummy_link.txt'):
        """Function used in order to retrieve the link of a dummy product stored in real time in a txt"""
        filename = f'{cur_path}\\Json Related\\{filename}'

        with open(filename) as f:
            link = f.read()

        return link

class LoadProfiles():
    """A class i use in order to load my profiles"""

    def __init__(self):
        self.file_path = f"{cur_path}\\csv"

    def get_profile_data(self, filename):
        """Getting all the essential profile data"""
        filename = f"{self.file_path}\\{filename}"
        profiles_list = []

        with open(filename) as f:
            reader = csv.DictReader(f)
            for row in reader:
                shipping_dict = {}
                shipping_dict = row.copy()

                profiles_list.append(shipping_dict)

        return profiles_list

    def write_to_csv_file(self, filename, header, data):
        """Writing down the rows to a csv file"""
        filename = f"{self.file_path}\\{filename}"

        # Clearing the file
        with open(filename, 'r+') as f:
            f.truncate(0)

        with open(filename, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(header)

            # write multiple rows
            writer.writerows(data)