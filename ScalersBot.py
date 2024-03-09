import requests, json, datetime, random, sys, uuid, threading, os, names, colorama, traceback
from time import sleep
from colorama import Fore

BOT_VERSION = '0.3'
cur_path = os.path.dirname(os.path.realpath(__file__))
colorama.init(autoreset=True)

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


class SizeerHandler:
    def __init__(self):
        """Setting the main values"""
        self.sizeer_link = ""
        self.sizeer_link_de = ""
        self.pioner_product_link = 'https://sizeer.ro/reebok-classic-leather-femei-pantofi-sport-alb-2232-2'

        self.sizeer_sizes_gs = [
            '36', '36,5', '37,5', '38', '38,5', '39', '40'
        ]
        self.sizeer_sizes_mens = [
            '40', '40,5', '41', '42', '42,5', '43', '44', '44,5', '45', '45,5', '46'
        ]

        self.number_of_tasks = 15
        self.max_retries_limit = 30
        self.continue_checkout = True
        self.max_checkouts = 1000
        self.full_throttle = True
        self.has_failed = False
        self.needs_new_cookie = False
        self.from_monitor = False
        self.number_of_preloads = 0
        self.enough_bad_cookies = 20
        self.farm_points_session = False
        self.sizes_selected = "36 - 48"
        self.safe_mode = "safe"
        self.safe_speed_mode = "safe speed"
        self.atack_mode_safe = 'attack safe'
        self.atack_mode_speed = 'attack speed'
        self.instances_for_atacking = 5
        self.task_category = 'dunk_low_adults.json'
        self.create_preload = False

    def run_sizeer_script(self, preload=False):
        if not preload:
            self.set_primitive_ui()

        script = SizeerBOT()
        threading.Thread(target=script.run_script, args=[self.number_of_tasks, self.sizeer_link,
                                                         self.max_retries_limit, self.continue_checkout,
                                                         self.max_checkouts, self.full_throttle, self.has_failed,
                                                         self.needs_new_cookie, self.from_monitor,
                                                         self.number_of_preloads, self.enough_bad_cookies,
                                                         self.farm_points_session, self.sizes_selected,
                                                         self.atack_mode_speed, self.instances_for_atacking,
                                                         self.task_category, self.create_preload]).start()

        # sleep(150)
        script.preload_mode_product_link = 'https://sizeer.de/nike-w-air-max-95-damen-sneaker-rosa-dj3859-600'
        script.found_item = True

    def run_sizeer_script_preloaded(self):
        """Used in order to run the script in preload mode"""
        self.create_preload = True
        self.sizeer_link = 'https://sizeer.ro/puma-graviton-mid-barbati-pantofi-sport-negru-38320401'
        self.sizeer_link = "https://sizeer.de/nike-w-air-max-95-damen-sneaker-rosa-dj3859-600"
        self.run_sizeer_script(preload=True)

    def set_primitive_ui(self):
        """A function used in order to fetch the UI"""
        # VIOLET DUNKS
        purple_pulse_sizeer_link = 'https://sizeer.ro/nike-dunk-low-og-femei-pantofi-sport-violet-dm9467-500'

        # BLACK WHITE DUNKS WOMEN
        bw_women_sizeer_link = 'https://sizeer.ro/nike-dunk-low-femei-pantofi-sport-negru-dd1503-101'

        # BLACK WHITE DUNKS MEN
        bw_men_sizeer_link = 'https://sizeer.ro/nike-dunk-low-retro-barbati-pantofi-sport-negru-dd1391-100'

        # Easter Dunks
        easter_sizeer_link = 'https://sizeer.ro/nike-w-dunk-low-se-femei-pantofi-sport-multicolor-dd1872-100'

        # Photon Dust
        photon_dust_sizeer_link = 'https://sizeer.ro/nike-dunk-low-femei-pantofi-sport-gri-dd1503-103'

        # Green Glow
        green_glow_sizeer_link = 'https://sizeer.ro/nike-dunk-low-femei-pantofi-sport-verde-dd1503-105'

        # TESTING LINK
        testing_sizeer_link = 'https://sizeer.ro/nike-dunk-low-femei-pantofi-sport-alb-dd1503-109'

        chosen_link = input("What link do you want to bot?"
                            "\n\t\t\t1 for ~ Purple Pulse Dunks"
                            "\n\t\t\t2 for ~ Women Black White Dunks"
                            "\n\t\t\t3 for ~ Mens Black White Dunks"
                            "\n\t\t\t4 for ~ Easter Dunks"
                            "\n\t\t\t5 for ~ Photon Dust Dunks"
                            "\n\t\t\t6 for ~ Green Glow Dunks"
                            "\n\t\t\tt for ~ TESTING PURPOSE"
                            "\n\t\t\tor simply input the link:   ")

        if chosen_link == '1':
            self.sizeer_link = purple_pulse_sizeer_link

        elif chosen_link == '2':
            self.sizeer_link = bw_women_sizeer_link

        elif chosen_link == '3':
            self.sizeer_link = bw_men_sizeer_link

        elif chosen_link == '4':
            self.sizeer_link = easter_sizeer_link

        elif chosen_link == '5':
            self.sizeer_link = photon_dust_sizeer_link

        elif chosen_link == '6':
            self.sizeer_link = green_glow_sizeer_link

        elif chosen_link == 't':
            self.sizeer_link = testing_sizeer_link

        else:
            self.sizeer_link = chosen_link

    def tool_fetch_system_accounts_handler(self):
        print(
            f'[SIZEER] [SYSTEM] [TOOL] [{datetime.datetime.now()}]\t'
            f'Initialising Account ID Retriever Tool...')
        mobile = SizeerMobileAPK()
        task_number = 0
        tool_sizeer_profiles = LoadProfiles().get_profile_data(f'sizeer_under_dev.csv')

        for profile in tool_sizeer_profiles:
            threading.Thread(target=self.fetch_system_accounts, args=[mobile, profile, task_number]).start()

            task_number += 1
            sleep(0.5)

    def fetch_system_accounts(self, mobile_class, task_number, email, password):
        """A function used in order to grab from the Sizeer's Data Base key information regarding accounts"""
        mobile = mobile_class
        mobile.set_beggining_variables(task_number)

        logs = "Initialising Account ID Retriever Tool..."
        BotTools().print_logs(logs, f'SIZEER', Fore.LIGHTMAGENTA_EX, task_mode='SYSTEM')

        # 1. First Step -> Login in the app
        client, bearer_token, unique_id = mobile.login(email, password, task_number)
        if not client:
            return

        # 2. Second Step -> Retrieve the coupons information
        coupons_infos = mobile.get_coupons_information(client, bearer_token, unique_id, task_number)
        if not coupons_infos:
            return

        # 3. Third Step -> Get account's number of points
        points = mobile.retrieve_user_points(client, bearer_token, unique_id, task_number)
        if not points:
            return

        json_dict = {
            "email": email,
            "in use": False,
            "last_used": str(datetime.datetime.now()),
            "points": points,
            "coupons": {},
        }

        coupon_names_list = ['Dunk High Adults', 'Dunk Low Adults', 'Dunk Low Kids', 'Uncaching coupon']

        try:
            for coupon in coupons_infos:
                coupon_name = coupon['name']
                if coupon_name in coupon_names_list:
                    if coupon['status']:
                        json_dict["coupons"][coupon_name] = str(coupon['id'])

            JsonClass().update_each_account_general_information(json_dict)

            print(
                f'[SIZEER] [TASK NUMBER {task_number}] [{datetime.datetime.now()}]\t'
                f'Account succesfully updated!')

        except:
            traceback.print_exc()
            print(
                f'[SIZEER] [TASK NUMBER {task_number}] [{datetime.datetime.now()}]\t'
                f'Failed unpacking the coupons.')

    def tool_place_fake_orders_get_points(self):
        obj = SizeerBOT()
        self.number_of_tasks = 13
        self.continue_checkout = False
        self.farm_points_session = True

        threading.Thread(target=obj.run_script, args=[self.number_of_tasks, self.pioner_product_link,
                                                      self.max_retries_limit, self.continue_checkout,
                                                      self.max_checkouts, self.full_throttle, self.has_failed,
                                                      self.needs_new_cookie, self.from_monitor, self.number_of_preloads,
                                                      self.enough_bad_cookies, self.farm_points_session]).start()

    def tool_account_generator_handler(self):
        """Main function that starts the account generators tasks"""
        csv_handler = LoadProfiles()
        # 1. First Step -> Generate the CSV File with the accounts
        self.create_csv_accounts()

        filename = f"sizeer_account_generator.csv"
        profiles = csv_handler.get_profile_data(filename)
        task_number = 0

        for profile in profiles:
            email = profile["EMAIL"]
            password = profile["PASSWORD"]
            fn = profile["FIRST NAME"]
            ln = profile["LAST NAME"]

            threading.Thread(target=self.account_generator, args=[task_number, email,
                                                                  password, fn, ln]).start()

            task_number += 1
            sleep(0.3)

    def account_generator(self, task_number, email, password, fn, ln):
        mobile = NewSizeerMobileAPK_AccGen()
        login_mobile = SizeerMobileAPK()
        tools = BotTools()
        json_handler = JsonClass()

        while True:
            client = tools.create_client()
            unique_id = str(uuid.uuid4())

            # 1. First Step -> Creating the session and getting a random token
            client, anonymous_token, \
                snrapi_anonymous_token = mobile.get_anonymous_token(client, task_number, unique_id)

            if not client:
                sleep(10)
                continue

            # 2. Second Step -> Create the account
            message, api_logs, \
                phone_number = mobile.create_new_account(client, anonymous_token, snrapi_anonymous_token,
                                                         task_number, unique_id, email, password, fn, ln)
            if message != "success":
                break

            # 3. Third Step -> Login
            client, bearer_token, api_logs = mobile.login(client, task_number, email, password,
                                                          unique_id, anonymous_token, api_logs,
                                                          snrapi_anonymous_token)

            # 4. Fourth Step -> Retrieve points
            client, points = mobile.retrieve_user_points(client, task_number, bearer_token, email,
                                                         unique_id, api_logs, snrapi_anonymous_token,
                                                         fn, ln, phone_number)
            if not client:
                break

            # 5. Fifth Step -> Store the accounts internally
            successfull = json_handler.store_new_account(email, password, points)

            sleep(15)
            threading.Thread(target=self.fetch_system_accounts,
                             args=[login_mobile, task_number, email, password]).start()

            break

    def create_csv_accounts(self):
        """A function used in order to generate the accounts required for creating the account"""
        csv_handler = LoadProfiles()
        tools = BotTools()
        csv_data = []
        csv_header = ["EMAIL", "PASSWORD", "FIRST NAME", "LAST NAME", "ADDRESS LINE 1",
                      "HOUSE NUMBER", "CITY", "POSTCODE/ZIP", "PROVINCE ID", "PHONE"]

        logs = "Generating emails..."
        tools.print_logs(logs, f'SIZEER', Fore.LIGHTMAGENTA_EX, task_mode='SYSTEM')

        bank_filename = f"sizeer_address_bank.csv"
        generated_filename = f"sizeer_account_generator.csv"
        profiles = csv_handler.get_profile_data(bank_filename)

        for profile in profiles:
            shipping_list = []
            for key, values in profile.items():
                shipping_list.append(profile[key])

            for i in range(0, 1):
                values_list = self.randomize_email()

                values_list.extend(shipping_list)
                csv_data.append(values_list)

        csv_handler.write_to_csv_file(generated_filename, csv_header, csv_data)

        logs = "Emails successfully generated!"
        tools.print_logs(logs, f'SIZEER', Fore.LIGHTGREEN_EX, task_mode='SYSTEM')

    def randomize_email(self):
        """Function that a list of random email and names based on a give catchall"""
        email = ""
        catchall = ""  # UPDATE WITH A CATCHALL
        password = ""
        gender_list = ['male', 'female']
        gender = random.choice(gender_list)

        fn = names.get_first_name(gender=gender)
        ln = names.get_last_name()

        choice_list = ['y', 'n']
        number_before = random.choice(choice_list)
        if number_before == 'y':
            email += f'{random.randint(1, 9)}'

        email += fn.lower()
        number_between = random.choice(choice_list)
        if number_between == 'y':
            email += f"{random.randint(1, 9)}"

        email += ln.lower()
        number_after = random.choice(choice_list)
        if number_after == 'y':
            email += str(random.randint(1, 9))

        email += catchall

        return [email, password, fn, ln]

    def tool_check_corrupted_storage_handler(self):
        """
        A function used in order to check for all the accounts
        that have been stored in a wrong way.
        """
        logs = "Initialising Corrupted Sessions Buster..."
        BotTools().print_logs(logs, f'SIZEER', Fore.LIGHTMAGENTA_EX, task_mode='SYSTEM')

        empty = 0
        corrupted = 0
        good = 0
        category = "good_accounts.json"
        stored_accounts = JsonClass().retrieve_dunks_accounts_by_category(category)

        for account in stored_accounts:
            email = account["email"]
            password = account["password"]
            ideal_account = {
                "email": email,
                "password": password,
                "in use": False,
                "last_used": str(datetime.datetime.now()),
                "placed orders": 0,
                "points": 500,
                "coupons": {
                    "Dunk Low Adults": "SIRODUNKL500",
                    "Dunk High Adults": "SIRODUNKH500",
                    "Dunk Low Kids": "SIRODUNK5",
                    "Uncaching coupon": "SIRO25022022"
                }
            }
            account_information = JsonClass().get_account_information(email)
            if not account_information:
                # Means that we failed storing the account
                JsonClass().write_corrupted_account(ideal_account)
                empty += 1
            else:
                try:
                    account_information = json.loads(account_information)
                except:
                    # Means that we failed storing the account
                    JsonClass().write_corrupted_account(ideal_account)
                    empty += 1
                else:
                    changed = False
                    for coupon_name, coupon_id in account_information["coupons"].items():
                        ideal_coupon_id = ideal_account["coupons"][coupon_name]
                        if ideal_coupon_id != coupon_id:
                            account_information["coupons"][coupon_name] = ideal_coupon_id
                            changed = True

                    if account_information["in use"]:
                        changed = True
                        account_information["in use"] = False

                    if changed:
                        JsonClass().write_corrupted_account(ideal_account)
                        corrupted += 1

                    else:
                        good += 1

        logs = f"Done Checking. Found [{empty} empty]  [{corrupted} corrupted]  [{good} good]"
        BotTools().print_logs(logs, f'SIZEER', Fore.LIGHTGREEN_EX, task_mode='SYSTEM')


if __name__ == "__main__":
    supreme_keywords = "+logo,+camo,+m-65"
    supreme_item_color = "Blue"
    supreme_size = "Medium"

    sizeer_handler = SizeerHandler()
    sizeer_handler.run_sizeer_script()
    # sizeer_handler.run_sizeer_script_preloaded()
    # sizeer_handler.tool_place_fake_orders_get_points()
    # sizeer_handler.tool_account_generator_handler()
    # sizeer_handler.tool_check_corrupted_storage_handler()
