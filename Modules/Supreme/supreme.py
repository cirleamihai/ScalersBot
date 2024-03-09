import requests, json, datetime, random, sys, os
from time import sleep

BOT_VERSION = '0.3'
cur_path = os.path.dirname(os.path.realpath(__file__))

path_for_tools = cur_path + '\\Tools'
path_for_sizeer_module = cur_path + '\\Modules\\Sizeer'

sys.path.append(path_for_sizeer_module)
sys.path.append(path_for_tools)

# noinspection PyUnresolvedReferences
from json_handler import JsonClass
# noinspection PyUnresolvedReferences
from bot_tools import BotTools, LoadProfiles
# noinspection PyUnresolvedReferences
from sizeer import SizeerBOT
# noinspection PyUnresolvedReferences
from sizeer_mobile import SizeerMobileAPK, NewSizeerMobileAPK_AccGen


class Supreme():
    """The class representing the Supreme Module, Flow and Checkout"""

    def start_script(self):
        """Main Script"""
        global supreme_category, retry_timeout
        supreme_category = 'Jackets'
        retry_timeout = 1

        while True:
            # The process is being looped until we have succesfully checked out.
            print(f"[{datetime.datetime.now()}]\tStarting Session...")
            client = BotTools().create_client()
            headers = {
                'authority': 'www.supremenewyork.com',
                'pragma': 'no-cache',
                'cache-control': 'no-cache',
                'accept': 'application/json',
                'user-agent': 'Mozilla/5.0 (Linux; Android 10; Pixel C Build/QQ3A.200805.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.198 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
                'sec-gpc': '1',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://www.supremenewyork.com/mobile/?c=1',
                'accept-language': 'en-US,en;q=0.9',
                'dnt': '1',
            }

            try:
                self.monitoring_for_new_items(client, headers)
                break

            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError,
                    requests.exceptions.ProxyError) as err:
                print(f'[{datetime.datetime.now()}]\tError getting items [TIMED OUT]')
                continue

            except Exception:
                print(f"[{datetime.datetime.now()}]\tError getting items. [UNKNOWN]")
                # traceback.print_exc()
                continue

    def monitoring_for_new_items(self, client, headers):
        """
        A recursive function that checks for new items

        If the item is found -> the next function is called.
        """
        print(f"[{datetime.datetime.now()}]\tMonitoring...")

        response = client.get('https://www.supremenewyork.com/mobile_stock.json',
                              headers=headers, timeout=5)

        if response.status_code == 200:
            # If we succesfully got a response back
            json_category_items = json.loads(response.text)['products_and_categories'][supreme_category]
            item_found = False

            for item in json_category_items:
                if BotTools().keywords_filter(item['name']):
                    print(f"[{datetime.datetime.now()}]\tItem Found! {item['name']}")

                    item_found = True
                    prod_id = item['id']

                    # If the item is found, we jump to the next step.
                    sleep(0.5)
                    self.get_item_details(client, prod_id)

            if not item_found:
                print(f"[{datetime.datetime.now()}]\tNo items found. Retrying...")
                sleep(retry_timeout)

                self.monitoring_for_new_items(client, headers)

        else:
            print(f"[{datetime.datetime.now()}]\tError getting items [{response.status_code}]")
            self.start_script()

    def get_item_details(self, client, prod_id):
        """A function used in order to add the item to cart"""
        global supreme_item_color
        prod_link = f'https://www.supremenewyork.com/shop/{prod_id}.json'
        try:
            headers = {
                'authority': 'www.supremenewyork.com',
                'pragma': 'no-cache',
                'cache-control': 'no-cache',
                'accept': 'application/json',
                'user-agent': 'Mozilla/5.0 (Linux; Android 10; Pixel C Build/QQ3A.200805.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.198 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
                'sec-gpc': '1',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://www.supremenewyork.com/mobile/?c=1',
                'accept-language': 'en-US,en;q=0.9',
                'dnt': '1',
            }

            response = client.get(prod_link, headers=headers, timeout=5)

            if response.status_code == 200:

                item_styles = json.loads(response.text)['styles']
                found_color = False

                for style in item_styles:
                    # Iterating trhough all styles to see which one matches ours.
                    if style['name'] == supreme_item_color:
                        found_color = True
                        style_id = style['id']
                        sizes_list_w_ids = style['sizes']

                        self.add_to_cart_item(client, style_id, sizes_list_w_ids, prod_id)

                if not found_color:
                    print(f"[{datetime.datetime.now()}]\tNo item color {supreme_item_color}.")

            else:
                print(f"[{datetime.datetime.now()}]\tError getting items [{response.status_code}]")

                self.get_item_details(client, prod_id)

        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError,
                requests.exceptions.ProxyError) as err:
            print(f'[{datetime.datetime.now()}]\tError getting product info [TIMED OUT]')

            self.start_script()

        except Exception:
            print(f"[{datetime.datetime.now()}]\tError getting product info [UNKNOWN]")

            self.get_item_details(client, prod_id)
            # traceback.print_exc()

    def add_to_cart_item(self, client, style_id, sizes_list, prod_id):
        """A function used in order to ATC the item"""
        atc_link = f'https://www.supremenewyork.com/shop/{prod_id}/add.json'
        global supreme_size

        if supreme_size == 'Random':
            random_size = random.choice(sizes_list)
            chosen_size_name = random_size['name']
            size_id = random_size['id']
        else:
            found_size = False
            for size in sizes_list:
                if size['name'] == supreme_size:
                    size_id = size['id']
                    found_size = True
                    chosen_size_name = size['name']

            if not found_size:
                print(f"[{datetime.datetime.now()}]\tNo size called {supreme_size}. Going with random size.")
                random_size = random.choice(sizes_list)
                chosen_size_name = random_size['name']
                size_id = random_size['id']

        print(f"[{datetime.datetime.now()}]\tAdding to cart ~ [{chosen_size_name}]")

        headers = {
            'authority': 'www.supremenewyork.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'accept': 'application/json',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; Pixel C Build/QQ3A.200805.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.198 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded',
            'sec-gpc': '1',
            'origin': 'https://www.supremenewyork.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.supremenewyork.com/mobile/?c=1',
            'accept-language': 'en-US,en;q=0.9',
            'dnt': '1',
        }

        data = {
            'size': size_id,
            'style': style_id,
            'qty': '1'
        }

        try:
            response = client.post(atc_link, headers=headers, data=data, timeout=5)

            if "in_stock" in response.text:
                print(f'[{datetime.datetime.now()}]\tAdded!')

                self.submit_checkout(client, size_id)

            else:
                print(f'[{datetime.datetime.now()}]\tItem OOS')
                sleep(1)
                self.add_to_cart_item(client, style_id, sizes_list, prod_id)

        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError,
                requests.exceptions.ProxyError) as err:
            print(f'[{datetime.datetime.now()}]\tError Adding to cart [TIMED OUT]')

            self.add_to_cart_item(client, style_id, sizes_list, prod_id)

        except Exception:
            print(f"[{datetime.datetime.now()}]\tError Adding to cart [UNKNOWN]")
            # traceback.print_exc()

            self.add_to_cart_item(client, style_id, sizes_list, prod_id)

    def submit_checkout(self, client, size_id):
        """A function used in order to submit the checkout"""
        cookie_sub = {
            size_id: '1'
        }
        cookie_sub = json.dumps(cookie_sub)
        profile = LoadProfiles().get_profile_data('./csv/supreme.csv')[0]
        headers = {
            'authority': 'www.supremenewyork.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'accept': 'application/json',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; Pixel C Build/QQ3A.200805.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.198 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded',
            'sec-gpc': '1',
            'origin': 'https://www.supremenewyork.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.supremenewyork.com/mobile/?c=1',
            'accept-language': 'en-US,en;q=0.9',
            'dnt': '1',
        }

        data = [
            ('store_credit_id', ''),
            ('from_mobile', '1'),
            ('cookie-sub', cookie_sub),
            ('same_as_billing_address', '1'),
            ('order[billing_name]', profile['FULL NAME']),
            ('order[email]', profile['EMAIL']),
            ('order[tel]', profile['PHONE']),
            ('order[billing_address]', profile['ADDRESS LINE 1']),
            ('order[billing_address_2]', profile['ADDRESS LINE 2']),
            ('order[billing_address_3]', ''),
            ('order[billing_city]', profile['CITY']),
            ('atok', 'sckrsarur'),
            ('order[billing_zip]', profile['POSTCODE/ZIP']),
            ('order[billing_country]', profile['COUNTRY(ISO CODE)']),
            ('credit_card[type]', 'credit card'),
            ('credit_card[cnb]', profile['CREDIT CARD NUMBER']),
            ('credit_card[month]', profile['EXPIRY MONTH(mm)']),
            ('credit_card[year]', profile['EXPIRY YEAR(yyyy)']),
            ('credit_card[ovv]', profile['CVV']),
            ('order[terms]', '0'),
            ('order[terms]', '1'),
            ('h-captcha-response',
             'W0_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwYXNza2V5IjoiRHVqS05ZbFB0bldSOXJYLzg0aTAyeFlWSzJZUVI4aU5xa2JUY09TNnhqWU5jZ01zWnA5U2grYXpGNCtwbWlJYzZ0eURkZmU0T3RUNWhBeUhnTzFOcDBMK245SHNVcGpxNDEvSFVFMTRjNGxLOHE3Ukk1TVJRTStwREpHcTJ6OVl2QkVKTGNKUUZaSnRRZy9jNlpCRERyKzFydDRYdnduUlJyUVU0K1gveEU2dG1lWGZsWVZuUmJMRmdFSVp2aW9HaUlNSUhBbTR0eHY4bFRpdDd2VVNCMURVNGthN1ppZi9vTXJlSWx0YUxoM0lTM1crN2RsMWUvQXZHUDlnbXVPa0pxVW1wYVlaVk1NZFZFTVJ0cjVVUmxuNndFaWFGU2ZCUFVabHdKSlp2UVBQOVdMbEwzRXBpYmpMaGVQcFUzaHRBZGttWHlzYzJkdC92LzBxUW5jSzByNjlMbXNSeFFVRnNIV2F1a2llZ2dTalM1RUtFOWpVeThEelZ4ZFV1RlFIajNvd1VCYXFNczUrb1c3UWFqeWFiSjlvYmFyQitIZHY1LzBIR0dBNnFHR3RZQ1ZPWitOQmFrQWNFTStQOG1GdDliK3p0c3hZQ3VtWDJJaTRsMzF1TklIdTE1d0FjUlRqTGhaV0h5bnkveGZDb01nV1VpMHBVckdONWkrS0hEWjQwR0ZwVk43ZFRxbW9lMXAybFNYTXV6aURsQUJLODlyYzM4cTN1OUpCVDVpa2hJNzA4c2pjbWxJaHBQWWNoZWlaRllNK0RBMmlCSG1sRW9rdmRVNjhvSjVKWXhjWVdqRTcrT21uWERmdUJJMGlkVXhHTS9SQ0J0eGZDZTVqanExZXVvdk1SS2ZCVFJERGVPdnlLVU4xVS9sZCszQ1VuZlczZDBOdDk0dTlJb3UvV3FLRE1pT3E3T0VsRTlkVlFWa08xVmlMck5jYU9pVDBzRVRlaHFOMUFFTFIvN3FvaDZQMktFeVE2Y25zMENaMUxWU200VFIxNU9wWUs5bmZ4eW5FUm9qeGsyZkMzSnBpamJJN2ZVZVAvZURBY3hCRjIraGpxNSt4bE8wZ0pCcjdpQmZYRlJVbS81dzIzcHdNSVNkVnV2Q1ptcVFUVHhxeWR2cWxZMWkxV3VkZEtDdW9vUXJqallkd3pnPT04amhYTzlvNmpYNElSYzhEIiwic2l0ZWtleSI6IjljMWY3NjU4LTJkZTgtNDNkMi1hYmNhLTY2NjBmMzQ0ZWExYyIsImV4cCI6MTYyNjk2NzMzOCwicGQiOjAsImNkYXRhIjoiblk2SmpXZ29iN2l2MnVGMVNRcHJpeE1TaVowTnpMVC9XeGlGTHZxVDZtUkEwS3VadWx3TkRJRURtdkhEUUlaVXJ1MmRIMlFCRC9sNlcwVEZHaFpqOE1Fd1JTMjVWckxLdmFDM1BRSVEvQnVoSzZzT1lXVEwvRVkwT2tZdmlvR0V4UXJOdmtLQTQyRFE3MnQ0ZlFhR3pQR2dmNkNCNFFya0RndkRmQXVWd1V6RDlTYTVWNjFHaUMwSDNLZFBnYTQ0VjZIYVJZc1J1Si83eHUyeiJ9.AfqpRmu3KMhygdqDjI5yMaGB1fGF9RexsqDyKjtb4w4'),
            ('is_from_android', '1'),
        ]

        response = client.post('https://www.supremenewyork.com/checkout.json',
                               headers=headers, data=data, timeout=5)

        print(response.text)
