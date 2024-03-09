import requests, json, traceback, datetime, random, string, sys, threading, colorama, uuid, os, playsound
import time as timp

from bs4 import BeautifulSoup
from unipath import Path
from time import time, sleep

from colorama import Fore

colorama.init(autoreset=True)

cur_path = os.path.dirname(os.path.realpath(__file__))
cur_path = Path(cur_path).parent.parent

path_for_tls_client = cur_path + '\\TLSClient'
path_for_tools = cur_path + '\\Tools'
path_for_antibots = cur_path + '\\Bot Protection'

sys.path.append(path_for_tls_client)
sys.path.append(path_for_tools)
sys.path.append(path_for_antibots)

from tlsclient import TLS_CLIENT
from json_handler import JsonClass
from bot_tools import BotTools, LoadProfiles
from akamai_solver import Abck, Akamai
from sizeer_mobile import SizeerMobileAPK, NewSizeerMobileAPK_AccGen


class SizeerBOT():
    def __init__(self):
        """Declaring the values that are going to be used for threading"""
        self.is_dunk = True
        self.all_sizes_sold_out = False
        self.full_throttle = False
        self.germany_region = False
        self.task_creates_preload = False
        self.farm_points_session = False
        self.cid = ''
        self.authority = 'sizeer.ro'
        self.home_page = 'https://sizeer.ro'
        self.selected_sizes = ""
        self.store_name = ""
        self.task_category = ""
        self.payment_method = "Cash ~ Fan Curier"

        # Product related
        self.prod_title = {}
        self.prod_image = {}
        self.prod_sku = {}
        self.discounted_price = {}
        self.product_link = {}
        self.product_price = {}
        self.start_time_dict = {}

        # App Related
        self.mobile = SizeerMobileAPK()
        self.mobile_client = {}
        self.app_access_token = {}
        self.activated_discount = {}
        self.app_unique_id = {}
        self.coupons_dict = {}
        self.dunk_coupon_id = {}
        self.dunk_coupon_name = {}
        self.entered_dead_zone = {}

        # Preload Related
        self.preload_mode = {}
        self.preloading_proccess = {}
        self.ready_preloaded_accounts = {}
        self.email = {}
        self.password = {}
        self.used_same_cookie = {}
        self.lost_session = {}
        self.client = {}
        self.logged_in = {}
        self.preload_mode_product_link = ""
        self.real_product_link = ""
        self.number_of_preloads = 0
        self.sold_out_preloaded = False
        self.found_item = False
        self.enp_cart_error = False
        self.sizes_not_written_out = True

        # Json related
        self.max_retries = {}
        self.chosen_size_dict = {}
        self.accounts_list_json = {}
        self.disabled_accounts_list_json = {}
        self.sold_out_sizes = []

        # CSV Related
        self.profiles_by_task_number = {}

        # System related
        self.tools = BotTools()
        self.enough_bad_cookies = 0
        self.bad_cookie_errors = 0
        self.number_of_checkouts = 0
        self.max_checkouts = 0
        self.number_of_profiles = 0
        self.accounts_used = []
        self.task_mode = {}
        self.global_abck_cookie = {}
        self.global_max_retries = {}
        self.has_failed_needs_restarting = {}
        self.has_failed_needs_restarting_with_new_cookie = {}
        self.has_succesfully_checked_out = {}
        self.continue_script = {}
        self.proxy_akam = {}
        self.prepare_session_early = {}
        self.has_failed_reloading = {}
        self.second_try_placing_order = {}
        self.checked_out = {}
        self.coupon_preserved = {}

        # Caching related
        self.uncached_succesfully = {}
        self.failed_uncaching = {}
        self.uncaching_link = {}

        # Atack Mode related
        self.instances_for_atacking = 0
        self.got_product_page = {}
        self.got_login_page = {}
        self.posted_login_page = {}
        self.got_shipping_page = {}
        self.posted_shipping_page = {}
        self.client_by_fastest_instance = {}
        self.response_by_fastest_instance = {}
        self.failed_getting_product_page = {}
        self.failed_getting_login_page = {}
        self.failed_posting_login_page = {}
        self.failed_getting_shipping_page = {}
        self.failed_posting_shipping_page = {}

    # -----------MONITOR RELATED CURRENTLY NOT IN USE DUE TO THREADS MISSMATCH-----------
    def check_for_max_retries(self, task_number):
        """

        Function works this way:
            -If the number of maximum retries has been reached, it will stop all the threads
            and exist the system
            -currently refreshes every 7 seconds

        """
        exists_main_thread = False
        sleep(3)
        while True:
            # Checking to see if this is the last thread alive
            mythreads = threading.enumerate()

            for thread in mythreads:
                if thread.name == 'MainThread':
                    exists_main_thread = True

            if exists_main_thread:
                if len(mythreads) == 2:
                    break
            elif len(mythreads) == 1:
                os._exit(0)

            # If there are other threads alive, then we continue

            if self.max_retries[task_number] >= self.global_max_retries[task_number]:
                print(f"[SIZEER{self.cid}] [TASK NUMBER {task_number}] [{datetime.datetime.now()}]\t"
                      f"MAXIMUM RETRIES REACHED!")

                os._exit(0)

            sleep(5)

    # -----------AKAMAI RELATED-----------
    def get_valid_akamai_cookie(self, client, user_agent, task_number):
        """A function used in order to generate valid Akamai Cookies _abck"""
        need_again = False
        while True:
            akamai_class = Akamai()
            print(
                f'[SIZEER{self.cid}] [TASK NUMBER {task_number}] [{datetime.datetime.now()}]\tGetting Akamai cookie...')

            if need_again:
                device_data = Akamai().get_database(task_number)
                user_agent = device_data['user-agent']

            headers = {
                'authority': self.authority,
                'pragma': 'no-cache',
                'cache-control': 'no-cache',
                'user-agent': str(user_agent),
                'accept': '*/*',
                'sec-gpc': '1',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'manifest',
                'referer': self.product_link[task_number],
                'accept-language': 'en-US,en;q=0.9',
                'dnt': '1',
            }

            try:
                response = client.get('https://sizeer.ro/manifest.json', headers=headers, timeout=7)
            except:
                print(
                    f'[SIZEER{self.cid}] [TASK NUMBER {task_number}] [{datetime.datetime.now()}]\tTimeout While fetching manifest...')
                continue

            headers = {
                'authority': self.authority,
                'pragma': 'no-cache',
                'cache-control': 'no-cache',
                'user-agent': str(user_agent),
                'accept': '*/*',
                'sec-gpc': '1',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'no-cors',
                'sec-fetch-dest': 'script',
                'referer': self.product_link[task_number],
                'accept-language': 'en-US,en;q=0.9',
                'dnt': '1',
            }

            start_ts = int(time() * 1000)
            response = client.get(
                'https://sizeer.ro/shzx6w01bTQGT/JH-D/-6pVCtz0_M/1kiVJcSkL5/YxU3A31SAw/eF9VM/UMKMT8', headers=headers,
                timeout=10)

            first_abck_cookie = response.cookies['_abck']
            first_sensor_data, start_ts, o9_value, d3, device_data, doact = \
                akamai_class.bpd(task_number, first_abck_cookie, user_agent, self.product_link[task_number],
                                 start_ts=start_ts)

            headers = {
                'authority': self.authority,
                'pragma': 'no-cache',
                'cache-control': 'no-cache',
                'user-agent': str(user_agent),
                'content-type': 'text/plain;charset=UTF-8',
                'accept': '*/*',
                'sec-gpc': '1',
                'origin': 'https://sizeer.ro',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': self.product_link[task_number],
                'accept-language': 'en-US,en;q=0.9',
                'dnt': '1',
            }

            data = {
                'sensor_data': first_sensor_data
            }
            dumped_json_data = str(json.dumps(data))

            response = client.post(
                'https://sizeer.ro/shzx6w01bTQGT/JH-D/-6pVCtz0_M/1kiVJcSkL5/YxU3A31SAw/eF9VM/UMKMT8',
                headers=headers, data=str(dumped_json_data), timeout=10)

            second_sensor_data, ran_fpcf_td, random_bmak_ta, start_ts, doact, same_last_shit, random_decimal_number \
                = akamai_class.bpd(task_number, first_abck_cookie, user_agent, self.product_link[task_number],
                                   has_challenge=True,
                                   start_ts=start_ts,
                                   o9_value=o9_value,
                                   d3=d3, )

            data = {
                'sensor_data': second_sensor_data
            }
            dumped_json_data = str(json.dumps(data))

            response = client.post(
                'https://sizeer.ro/shzx6w01bTQGT/JH-D/-6pVCtz0_M/1kiVJcSkL5/YxU3A31SAw/eF9VM/UMKMT8',
                headers=headers, data=str(dumped_json_data), timeout=10)
            challenge_abck_cookie = response.cookies['_abck']

            if '~0~' in challenge_abck_cookie:
                third_sensor_data = akamai_class.bpd(task_number, challenge_abck_cookie, user_agent,
                                                     self.product_link[task_number],
                                                     has_challenge=True,
                                                     is_second_challenge=True,
                                                     ran_fpcf_td=ran_fpcf_td,
                                                     random_bmak_ta=random_bmak_ta,
                                                     start_ts=start_ts,
                                                     o9_value=o9_value,
                                                     d3=d3,
                                                     doact=doact,
                                                     same_last_shit=same_last_shit,
                                                     random_decimal_number=random_decimal_number
                                                     )
                data = {
                    'sensor_data': third_sensor_data
                }
                dumped_json_data = str(json.dumps(data))

                response = client.post(
                    'https://sizeer.ro/shzx6w01bTQGT/JH-D/-6pVCtz0_M/1kiVJcSkL5/YxU3A31SAw/eF9VM/UMKMT8',
                    headers=headers, data=str(dumped_json_data), timeout=10)
                received_abck_cookie = response.cookies['_abck']

                if '||-1||' in received_abck_cookie and '~0~' in received_abck_cookie:
                    if len(received_abck_cookie) == 464:
                        print(
                            f"[SIZEER{self.cid}] [TASK NUMBER {task_number}] [{datetime.datetime.now()}]\tAkamai Cookie Succesfully set!")
                        # print(first_sensor_data, '\n\n', second_sensor_data, '\n\n', third_sensor_data)

                        return client, received_abck_cookie

                    else:
                        print(
                            f"[SIZEER{self.cid}] [TASK NUMBER {task_number}] [{datetime.datetime.now()}]\tBad cookie length! Length: {len(received_abck_cookie)}")
                        client = BotTools().create_client()
                        user_agent = BotTools().get_user_agents()

                else:
                    print(
                        f'[SIZEER{self.cid}] [TASK NUMBER {task_number}] [{datetime.datetime.now()}]\tInvalid Sensor sent. [#3]')
                    client = BotTools().create_client()
                    user_agent = BotTools().get_user_agents()

            else:
                print(
                    f'[SIZEER{self.cid}] [TASK NUMBER {task_number}] [{datetime.datetime.now()}]\tInvalid Sensor sent. [#2]')

                print(first_sensor_data, '\n', second_sensor_data)

                need_again = True
                client = BotTools().create_client()
                user_agent = BotTools().get_user_agents()

    def get_valid_akamai_cookie_api(self, proxy, task_number):
        pass

    # -----------MAIN HANDLERS-----------
    def initial_task_handler(self, client, user_agent, task_number, from_monitor,
                             max_retries_limit, proxy_akam, in_preload=False, uncaching_discount_task=False):
        """
        THE MOST IMPORTANT FUNCTION. SETS THE MAIN STEPS FOR THE CHECKOUT FLOW. AUTONOMOUS FUNCTION.

        Manages the initial task of the checkout process. It is responsible for setting up the checkout process,
        including retrieving product information, adding the product to the cart, managing the login process,
        and handling the shipping and order submission process.

        In the case of a successful checkout, the function updates the number of successful checkouts and resets the retry counter.
        If the checkout process fails at any step, the function handles the reinitialization of the checkout process and
        ensures that the checkout process is repeated until the maximum number of retries is reached.

        The function also manages the process of changing the account's password and email, and re-logging into the
        application if the product being checked out is a "dunk". On sizeer, dunks need special accounts.

        In the case of a successful preload, the function updates the preload status and prepares the task for
        the actual checkout process

        This function is designed to be robust and handle various scenarios and exceptions that might occur during the
        checkout process. It is an essential part of ensuring a smooth and successful checkout experience.
        """
        while True:
            # 1. First Step -> Get Request to manifest.json in order to set some sess cookies
            client = self.get_starting_cookies(client, user_agent, task_number)
            if not client:
                return self.kill_task(task_number, step="Manifest Step")

            # 1.1 Extra Step -> Login
            if self.is_dunk or self.farm_points_session:
                client = self.login(client, user_agent, self.email[task_number],
                                    self.password[task_number], task_number,
                                    from_monitor, uncaching_discount_task)

                if not client:
                    break

            # 2. Second Step -> Getting Product Information (Get Request + Scraping)
            client, chosen_size, prod_pid = self.retrieve_product_information(client, user_agent, task_number,
                                                                              from_monitor, in_preload,
                                                                              uncaching_discount_task)
            if not client:
                return

            # 3. Third Step -> Add to Cart (Post Request + Activating the Code if needed)
            client, email, password = self.add_to_cart_script(client, user_agent, prod_pid,
                                                              task_number, chosen_size,
                                                              in_preload, uncaching_discount_task)
            if not client:
                break

            # 3.1. Extra Step -> If we have a dunk/ farm for points, we are going to check for discounted
            if self.is_dunk or self.farm_points_session:

                if uncaching_discount_task:
                    self.check_discounted(client, user_agent, task_number,
                                          uncaching_discount_task=uncaching_discount_task)
                    break

            # 4.1. Fourth Step -> Get Shipping Token
            client, shipping_token, response = self.get_shipping(client, user_agent, task_number, email)
            if not client:
                break

            # 4.2. Fourth Step -> Submit Shipping
            client, response = self.submit_shipping(client, user_agent, task_number, shipping_token, response)
            if not client:
                break

            # 5.1. Fifth Step -> Get Cart Token
            client, cart_token = self.get_order_page(client, user_agent, task_number,
                                                     email, response)
            if not client:
                break

            # 5.2. Fifth Step -> Submit Order
            client = self.submit_order(client, user_agent, email,
                                       task_number, cart_token)

            if not client:
                break

            # In case it was a dunk, we are calling a function in order to change
            # the accounts password and email and relogin into apk
            self.change_coupon(task_number, email, password, from_monitor)

            # CHECK after checkout
            continue_checkouts = self.after_tasks_end_check_if_checked_out(task_number)
            if continue_checkouts:
                if "safe" in self.task_mode[task_number].lower():
                    self.has_failed_needs_restarting[task_number] = True

                elif 'speed' in self.task_mode[task_number].lower():
                    self.checked_out_task_handler(client, user_agent, task_number,
                                                  from_monitor, in_preload, email,
                                                  max_retries_limit, uncaching_discount_task,
                                                  get_new_cookie=False)

            break

        # After we are done with everything
        # If we finished the uncaching proccess, we will finish the dummy task
        if uncaching_discount_task:
            if self.has_failed_needs_restarting[task_number]:
                self.failed_uncaching[task_number] = True

            return

        # Only if it's a dunk we're going to write the updated accounts availability
        if not self.has_failed_needs_restarting[task_number]:
            self.after_tasks_end_disable_dunks_accounts(task_number)

        # If it needs restarting, we restart it. Did this in order to avoid
        # some missmatches due to using Threading
        else:
            self.entered_dead_zone[email] = False

            self.start_tasks_threading(task_number,
                                       has_failed=True,
                                       from_monitor=from_monitor,
                                       needs_new_cookie=self.has_failed_needs_restarting_with_new_cookie[
                                           task_number])

    def checked_out_task_handler(self, client, user_agent, task_number, from_monitor,
                                 in_preload, email, max_retries_limit,
                                 uncaching_discount_task, get_new_cookie):
        """
        The function is a key component of the checkout process in the SizeerBOT class. This function is responsible
        for managing the checkout process after a successful cart addition.

        It handles the entire checkout flow, including retrieving product information, adding the product to the cart,
        getting and submitting shipping information, and finally, submitting the order.

        The function also handles the reinitialization of the checkout process in case of a failure at any step. It
        ensures that the checkout process is repeated until the maximum number of retries is reached.

        In the case of a successful checkout, the function updates the number of successful checkouts and resets the retry counter.

        It also manages the process of changing the account's password and email, and re-logging into the application
        if the product being checked out is a "dunk".

        This function is designed to be robust and handle various scenarios and exceptions that might occur during the checkout process.
        It is an essential part of ensuring a smooth and successful checkout experience.
        """
        while True:
            # Before all, we clear the trash values from the previous checkout process
            self.prepare_session_for_more_checkouts(task_number, email, max_retries_limit, get_new_cookie)

            # 0. Intern Step -> Get Request to manifest.json in order to set some sess cookies
            client = self.get_starting_cookies(client, user_agent, task_number)
            if not client:
                break

            # 1. First Step -> Get a required information about sizes
            size_variant, chosen_size = self.check_sizes_already_stored(task_number)
            if not size_variant:
                break

            # 2. Second Step -> Add the product to cart
            client, email, password = self.add_to_cart_script(client, user_agent, size_variant,
                                                              task_number, chosen_size, in_preload,
                                                              uncaching_discount_task)

            if not client:
                break

            # 4.1. Fourth Step -> Get Shipping Token
            client, shipping_token, response = self.get_shipping(client, user_agent, task_number, email)
            if not client:
                break

            # 4.2. Fourth Step -> Submit Shipping
            client, response = self.submit_shipping(client, user_agent, task_number, shipping_token, response)
            if not client:
                break

            # 5.1. Fifth Step -> Get Cart Token
            client, cart_token = self.get_order_page(client, user_agent, task_number,
                                                     email, response)

            if not client:
                break

            # 5.2. Fifth Step -> Submit Order
            client = self.submit_order(client, user_agent, email,
                                       task_number, cart_token)

            if not client:
                break

            # CHECK after checkout
            continue_checkouts = self.after_tasks_end_check_if_checked_out(task_number)

            if not continue_checkouts:
                break

            # In case it was a dunk, we are calling a function in order to change
            # the accounts password and email and relogin into apk
            self.change_coupon(task_number, email, password, from_monitor)

    def preload_task_handler(self, client, user_agent,
                             task_number, from_monitor,
                             max_retries_limit, uncaching_discount_task=False):
        """
        ENTIRE CHECKOUT SPEED: 2 - 3 seconds

        Responsible for managing the preloading process of the checkout flow. This function is specifically designed to
        handle tasks related to preloading, which is a process that prepares the checkout process ahead of time to
        increase the speed and efficiency of the checkout when the actual product is released.

        The function initiates the preloading process by setting up the checkout process, including retrieving product
        information, adding the product to the cart, managing the login process, and handling the shipping
        and order submission process.

        In the case of a successful preload, the function updates the preload status and prepares the task for the actual
        checkout process. If the preloading process fails at any step, the function handles the reinitialization of the
        preloading process and ensures that the preloading process is repeated until the maximum number of retries is reached.

        This function is designed to be robust and handle various scenarios and exceptions that might occur during the
        preloading process. It is an essential part of ensuring a smooth and successful checkout experience, especially
        for high-demand products that require quick checkout times.
        """
        in_preload = True
        self.task_mode[task_number] = 'preload web'

        # 1. First Step -> Get Request to manifest.json in order to set some sess cookies
        client = self.get_starting_cookies(client, user_agent, task_number)
        if not client:
            return False

        # 2. Second Step -> Login
        client = self.login(client, user_agent, self.email[task_number],
                            self.password[task_number], task_number,
                            from_monitor, uncaching_discount_task)

        if not client:
            return False

        # 3. Third Step -> Getting Product Information (Get Request + Scraping)
        client, chosen_size, prod_pid = self.retrieve_product_information(client, user_agent, task_number,
                                                                          from_monitor, in_preload,
                                                                          uncaching_discount_task,
                                                                          create_preload=True)
        if not client:
            if self.sold_out_preloaded:
                return True

            return False

        # 4. Fourth Step -> Add to Cart (Post Request + Activating the Code if needed)
        client, email, password = self.add_to_cart_script(client, user_agent, prod_pid,
                                                          task_number, chosen_size,
                                                          uncaching_discount_task=uncaching_discount_task,
                                                          create_preload=True)
        if not client:
            return False

        # 5.1. Fifth Step -> Get Shipping Token
        client, shipping_token, response = self.get_shipping(client, user_agent, task_number, email)
        if not client:
            return False

        # 5.2. Fifth Step -> Submit Shipping
        client, response = self.submit_shipping(client, user_agent, task_number, shipping_token, response)
        if not client:
            return False

        # 6. Sixth Step -> Get Cart Token
        client, cart_token = self.get_order_page(client, user_agent, task_number,
                                                 email, response)
        if not client:
            return False

        # 7. Seventh Step -> Clear Cart
        client, succesfully_preloaded = self.empty_cart(client, user_agent, task_number)

        if succesfully_preloaded:
            threading.Thread(target=self.successfully_preloaded_task_handler,
                             args=[client, user_agent, task_number, from_monitor, cart_token]).start()

        return succesfully_preloaded

    def successfully_preloaded_task_handler(self, client, user_agent, task_number, from_monitor, cart_token):
        """

        Function is being called after a task has successfully ended up the preloading process.

        PHP Sess ID lasts for around 6 hours [not sure yet], then it resets no matter of the
        user's activity

        After 30 minutes of inactivity, the session's information is being deleted.

        """
        threading.Thread(target=self.sleep_and_refresh_preloaded, args=[client, user_agent, task_number]).start()

        while not self.found_item:
            if self.lost_session[task_number]:
                self.kill_preload_task_start_new_one(task_number, preload_mode=True,
                                                     from_monitor=from_monitor)

                return

            sleep(0.5)

        # If we just found our item we are going to start the checkout proccess.
        self.set_found_item_variables(task_number)

        # 1. First Step -> Get the product information
        client, chosen_size, prod_pid = self.retrieve_product_information(client, user_agent, task_number,
                                                                          from_monitor, in_preload=True)
        if not client:
            if prod_pid:
                # If prod_pid is True when client is false, means the item
                # has gone out of stock so we stop the proccess
                return

            self.kill_preload_task_start_new_one(task_number, preload_mode=False,
                                                 from_monitor=from_monitor)
            return

        # 2. Second Step -> Add to cart
        client, email, password = self.add_to_cart_script(client, user_agent, prod_pid,
                                                          task_number, chosen_size,
                                                          in_preload=True)
        if not client:
            if email:
                # If email is True when client is false, means the item
                # has gone out of stock so we stop the proccess
                return

            self.kill_preload_task_start_new_one(task_number, preload_mode=False,
                                                 from_monitor=from_monitor)
            return

        # 2.1 Extra Step -> Log cart on site's backend.
        normal_product = not self.is_dunk
        discount_applied = self.check_discounted(client, user_agent, task_number, normal_product=normal_product)
        if not discount_applied:
            return

        # 3. Third Step -> Place Order
        client = self.submit_order(client, user_agent, email,
                                   task_number, cart_token)

        if not client:
            JsonClass().update_each_account_general_information(self.disabled_accounts_list_json[task_number])

            return

        # In case it was a dunk, we are calling a function in order to change
        # the accounts password and email and relogin into apk
        self.change_coupon(task_number, email, password, from_monitor)

        continue_checkouts = self.after_tasks_end_check_if_checked_out(task_number)
        if continue_checkouts:
            self.checked_out_task_handler(client, user_agent, task_number, from_monitor,
                                          in_preload=False,
                                          email=self.email[task_number],
                                          max_retries_limit=self.global_max_retries,
                                          uncaching_discount_task=False,
                                          get_new_cookie=True)

        if self.has_failed_needs_restarting[task_number]:
            self.start_tasks_threading(task_number,
                                       has_failed=True,
                                       needs_new_cookie=self.has_failed_needs_restarting_with_new_cookie[task_number],
                                       from_monitor=from_monitor,
                                       already_prelucrated=True)

    def out_of_stock_handler_dunks(self, client, user_agent, task_number, redirected_last_step=False):
        """
        Function used in case our product goes out of stock while we are in
        checkout process. It's reliable when dunks are being released, so the
        client doesn't have to relogin each time, which losses lot of seconds
        """

        # 1. First Step -> Empty the cart
        client, succesfully_preloaded = self.empty_cart(client, user_agent, task_number, redirected_last_step)
        if not client:
            return False, False

        # 2. Second Step -> Pick another in stock size
        size_variant, chosen_size = self.check_sizes_already_stored(task_number)
        if not size_variant:
            return False, False

        # 3. Third Step -> Add to cart
        client, email, password = self.add_to_cart_script(client, user_agent, size_variant,
                                                          task_number, chosen_size)

        return client, email

    # -----------MAIN STEPS-----------
    def run_script(self, number_of_tasks,
                   product_link="",
                   max_retries_limit=0,
                   continue_checkouts=False,
                   max_checkouts=1000,
                   full_throttle=False,
                   has_failed=False,
                   needs_new_cookie=False,
                   from_monitor=False,
                   number_of_preloads=20,
                   enough_bad_cookies=20,
                   farm_points_session=False,
                   sizes_selected="35.5 - 48",
                   mode="safe",
                   instances_for_atacking=5,
                   task_category="dunk_low_adults.json",
                   create_preload=False):
        """

        MAIN FUNCTION

        """
        self.payment_method = 'Cash ~ Fan Curier'

        self.set_if_preload_set_if_dunk_set_if_germany_region(product_link, mode)

        self.set_system_variables(product_link, max_checkouts, full_throttle,
                                  enough_bad_cookies, farm_points_session, create_preload,
                                  sizes_selected, instances_for_atacking, task_category)

        profiles, accounts = self.load_available_accounts_and_csv(task_category, create_preload)

        if profiles:
            increment = 0
            false_var = False

            # If the item is a dunk, we check the number of profiles since we need Account Mode
            if self.is_dunk or self.farm_points_session or create_preload:
                lowest_number = self.reduce_number_of_tasks_to_profiles_number(number_of_tasks, profiles,
                                                                               accounts, mode)

                task_number = 0
                while task_number < lowest_number:
                    threading.Thread(target=self.start_tasks_threading,
                                     args=[task_number, has_failed, needs_new_cookie,
                                           continue_checkouts, product_link,
                                           max_retries_limit, from_monitor,
                                           false_var, false_var, create_preload,
                                           mode]).start()

                    sleep(0.15)
                    task_number += 1

            # Otherwise we will run the threads and cop as many pairs as possible
            else:
                task_number = 0
                self.assign_first_profile_to_all_tasks(number_of_tasks, profiles, accounts, mode)

                while task_number < number_of_tasks:
                    threading.Thread(target=self.start_tasks_threading,
                                     args=[task_number, has_failed, needs_new_cookie,
                                           continue_checkouts, product_link,
                                           max_retries_limit, from_monitor, false_var,
                                           false_var, false_var, mode]).start()

                    sleep(0.2)
                    task_number += 1

        else:
            logs = f'Error starting module. No profiles saved! Please check! [profiles.csv]'
            self.tools.print_logs(logs, self.store_name, Fore.RED, task_mode='SYSTEM')

    def start_tasks_threading(self, task_number, has_failed=False,
                              needs_new_cookie=False,
                              continue_checkouts=True,
                              product_link="",
                              max_retries_limit=0,
                              from_monitor=False,
                              uncache_discount_task=False,
                              already_prelucrated=False,
                              create_preload=False,
                              task_mode="safe"):
        """A function used in order to start the tasks used for multiple profiles"""
        # Setting initial variables for each task
        if not uncache_discount_task:
            self.set_tasks_variables(task_number, create_preload, continue_checkouts,
                                     has_failed, product_link, max_retries_limit,
                                     needs_new_cookie, task_mode)
        else:
            self.uncaching_link[task_number] = product_link

        try:
            email, password = self.prelucrate_profiles(task_number, from_monitor, create_preload,
                                                       uncache_discount_task, already_prelucrated)

            if not email:
                return

        except:
            logs = 'Error to prelucrate profiles'
            self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)
            traceback.print_exc()

            return

        while True:
            # The process is being looped until we have succesfully checked out.
            logs = 'Creating Session...'
            self.tools.print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX, task_number)

            client, proxy, proxy_akam, user_agent = self.create_client_session(task_number)
            if not client:
                logs = 'Please adjust region for PRELOAD MODE.'
                self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

            in_preload = False

            try:

                if not create_preload:
                    threading.Thread(target=self.initial_task_handler,
                                     args=[client, user_agent, task_number, from_monitor, max_retries_limit,
                                           proxy_akam, in_preload, uncache_discount_task]).start()

                if not has_failed and not uncache_discount_task:

                    threading.Thread(target=self.get_valid_akamai_cookie,
                                     args=[client, user_agent, task_number]).start()

                    if (self.is_dunk or create_preload) and not self.germany_region:
                        # Logging in at the same time
                        threading.Thread(target=self.login_app_client,
                                         args=[task_number, email, password]).start()

                if needs_new_cookie:
                    self.global_abck_cookie[task_number] = ""
                    threading.Thread(target=self.get_valid_akamai_cookie,
                                     args=[client, user_agent, task_number]).start()

                if create_preload:
                    succesfully_preloaded = self.preload_task_handler(client, user_agent, task_number,
                                                                      from_monitor, max_retries_limit)

                    # If something went wrong while preloading, we will reset the session
                    if not succesfully_preloaded:
                        continue_module = self.count_error(task_number)
                        if not continue_module:
                            break

                        needs_new_cookie = self.has_failed_needs_restarting_with_new_cookie[task_number]
                        continue

                break

            except Exception:
                traceback.print_exc()

                logs = 'Error Starting Script. [UNKNOWN]'
                self.tools.print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX, task_number)

                return

    def retrieve_product_information_request(self, client, user_agent, task_number, uncaching_discount_task, instance):
        """A function containing the request malformed in order to retrieve the product information"""
        while True:
            if uncaching_discount_task:
                sizeer_link_uncached = self.randomize_link(task_number, self.uncaching_link[task_number])
            else:
                sizeer_link_uncached = self.randomize_link(task_number, self.product_link[task_number])

            headers = [
                ['method', 'GET'],
                ['authority', self.authority],
                ['scheme', 'https'],
                ['cache-control', 'no-cache'],
                ['upgrade-insecure-requests', '1'],
                ['user-agent', str(user_agent)],
                ['accept',
                 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'],
                ['sec-gpc', '1'],
                ['sec-fetch-site', 'none'],
                ['sec-fetch-mode', 'navigate'],
                ['sec-fetch-user', '?1'],
                ['sec-fetch-dest', 'document'],
                ['accept-encoding', 'gzip, deflate, br'],
                ['accept-language', 'en-US,en;q=0.9'],
                ['cookie', '']
            ]

            try:
                # GET Method
                response = client.makeRequest(sizeer_link_uncached, {
                    "method": "GET",
                    "headers": headers
                })

            except:
                if not self.got_product_page[task_number]:
                    logs = f"Failed getting product information. [TIMED OUT] [{instance}]"
                    self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

                    continue_module = self.count_error(task_number, atacking_instance=True)
                    if not continue_module:
                        self.failed_getting_product_page[task_number] += 1

                        break

                    continue

                else:
                    break

            else:
                if not self.got_product_page[task_number]:
                    self.got_product_page[task_number] = instance + 1
                    self.client_by_fastest_instance[task_number][instance] = client
                    self.response_by_fastest_instance[task_number][instance] = response

                break

    def retrieve_product_information(self, client, user_agent, task_number, from_monitor,
                                     in_preload=False, uncaching_discount_task=False, create_preload=False):
        """

        A function used in order to get product information

        If Atack mode is set to true:
            ~It will start few threads all requesting the same page.
            ~Whichever thread is the fastest, it will set the client's response

            ~self.got_product_page[task_number] -> has the increment of the fastest instance to load

        """
        while True:
            self.client_by_fastest_instance[task_number] = {}
            self.response_by_fastest_instance[task_number] = {}
            self.failed_getting_product_page[task_number] = 0

            logs = 'Getting product details...'
            self.tools.print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX, task_number)

            if in_preload:
                self.start_time_dict[str(task_number)] = int(time())

            try:
                instance_counter = 0
                instances_number = 1
                self.got_product_page[task_number] = 0

                if 'attack' in self.task_mode[task_number]:
                    instances_number = self.instances_for_atacking

                while instance_counter < instances_number:
                    threading.Thread(target=self.retrieve_product_information_request,
                                     args=[client, user_agent, task_number,
                                           uncaching_discount_task, instance_counter]).start()
                    instance_counter += 1
                    sleep(0.5)

                while not self.got_product_page[task_number]:
                    if self.failed_getting_product_page[task_number] == instances_number:
                        return self.kill_task(task_number, step="Just Disable"), False, False

                    sleep(0.1)

                fastest_instance = self.got_product_page[task_number] - 1
                client = self.client_by_fastest_instance[task_number][fastest_instance]
                response = self.response_by_fastest_instance[task_number][fastest_instance]

                if 'cp_challenge' in response.body:
                    # If this happens when we are in preload, means our session got flagged by akamai and
                    # we need to restart the entire process
                    if in_preload:
                        self.has_failed_needs_restarting_with_new_cookie[task_number] = True

                        return False, False, False

                    # We add the abck cookie before hand
                    self.prepare_session_early[task_number] = True

                    continue_module = self.count_error(task_number)
                    if not continue_module:
                        return self.kill_task(task_number, step="Just Disable"), False, False

                    # We restart the session with a good ABCK Cookie from the beggining
                    client = self.get_starting_cookies(client, user_agent, task_number)
                    if not client:
                        return self.kill_task(task_number, step="Manifest Step"), False, False

                    else:
                        continue

                if response.status != 200:
                    logs = f'Wrong Response Code! [{response.status}]'
                    self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

                    if in_preload:
                        self.has_failed_needs_restarting_with_new_cookie[task_number] = True

                        return False, False, False

                    if self.is_dunk and not uncaching_discount_task:
                        JsonClass().update_each_account_general_information(
                            self.disabled_accounts_list_json[task_number])

                    continue_module = self.count_error(task_number)
                    if not continue_module:
                        return False, False, False

                    if not uncaching_discount_task and not create_preload:
                        self.start_tasks_threading(task_number,
                                                   has_failed=True,
                                                   from_monitor=from_monitor,
                                                   needs_new_cookie=self.has_failed_needs_restarting_with_new_cookie[
                                                       task_number],
                                                   already_prelucrated=True)
                    return False, False, False

                size_list, sizes_pids_dict, prod_info, \
                    json_size_variant_dict, filtered_sizes = self.scrape_product_information(response, task_number)

                # Checking to see wether the product has gone out of stock or not
                size_list, sizes_pids_dict, \
                    json_size_variant_dict, cp_challenge = self.check_size_list(client,
                                                                                user_agent,
                                                                                task_number,
                                                                                size_list,
                                                                                sizes_pids_dict,
                                                                                json_size_variant_dict,
                                                                                from_monitor,
                                                                                filtered_sizes)

                """

                We have 3 bad Scenario Cases:
                1. We received a wrong response code while reloading -> reset the instance
                        ~new ip
                        ~new client
                        ~new user agent

                2. We got hit with a CP Challenge upon reloading the product page -> restart the instance
                    and use a Fresh and Good Abck Cookie while doing so

                3. The product Has gone Out Of Stock while reloading/ Has been Out Of Stock since 
                    the beggining -> we simply disable the accounts that have been used if that's 
                    the case and close the task instance

                If the results are good and as expected, we continue with the process.
                """

                # 1
                if self.has_failed_reloading[task_number]:
                    if in_preload:
                        self.has_failed_needs_restarting_with_new_cookie[task_number] = True

                        return False, False, False

                    continue_module = self.count_error(task_number)
                    if not continue_module:
                        return self.kill_task(task_number, step="Just Disable"), False, False

                    if not uncaching_discount_task and not create_preload:
                        self.start_tasks_threading(task_number,
                                                   has_failed=True,
                                                   from_monitor=from_monitor,
                                                   needs_new_cookie=True,
                                                   already_prelucrated=True)

                    return False, False, False

                # 2
                if cp_challenge:
                    if in_preload:
                        self.has_failed_needs_restarting_with_new_cookie[task_number] = True

                        return False, False, False

                    # We add the abck cookie before hand
                    self.prepare_session_early[task_number] = True

                    continue_module = self.count_error(task_number)
                    if not continue_module:
                        return self.kill_task(task_number, step="Just Disable"), False, False

                    # We restart the session with a good ABCK Cookie from the beggining
                    client = self.get_starting_cookies(client, user_agent, task_number)
                    if not client:
                        return self.kill_task(task_number, step="Manifest Step"), False, False
                    else:
                        continue

                # 3
                if not size_list:
                    if create_preload:
                        self.sold_out_preloaded = True

                    return self.kill_task(task_number, step="Just Disable"), False, True

                # Depending on the pricing, we are going to classify the pair of dunk by being adults or gs
                if self.is_dunk:
                    if uncaching_discount_task:
                        self.discounted_price[task_number] = 'No Price'

                    else:
                        price_dict = {
                            '1039': '659',
                            '989': '599',
                            '879': '549'
                        }

                        self.discounted_price[task_number] = price_dict[str(prod_info['old price'])]

                # If the product is not a dunk, we don't care about the pricing
                else:
                    self.discounted_price[task_number] = prod_info['new price']

                if not uncaching_discount_task:
                    self.prod_image[task_number] = prod_info['image']
                    self.prod_title[task_number] = prod_info['title']
                    self.prod_sku[task_number] = prod_info['pid']
                    self.product_price[task_number] = prod_info['new price']

                logs = f"Found item {prod_info['title']} - {prod_info['pid']}"
                self.tools.print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX, task_number)

                random_size = self.pick_size(task_number, prod_info['pid'], size_list, json_size_variant_dict)

                # Means we have ran out of sizes
                if not random_size:
                    return self.kill_task(task_number, step="Just Disable"), False, False

                prod_pid = sizes_pids_dict[random_size]
                logs = f"Picked Size - {random_size}"
                self.tools.print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX, task_number)

                return client, random_size, prod_pid

            except:
                logs = f"Error getting product information. [CHECK LOGS]"
                self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)
                traceback.print_exc()

                continue_module = self.count_error(task_number)
                if not continue_module:
                    return self.kill_task(task_number, step="Just Disable"), False, False

                if not create_preload:
                    self.start_tasks_threading(task_number,
                                               has_failed=True,
                                               from_monitor=from_monitor,
                                               already_prelucrated=True)

                return False, False, False

    def scrape_product_information(self, response, task_number):
        """A function used in order to scrape the product information like ATC variants, PIDs, etc."""
        sizes_pids_dict = {}
        size_list = []
        json_sizes_pids_list = []
        filtered_sizes = True

        pid_split = 'ului: '
        site_home = 'https://sizeer.ro'

        if self.germany_region:
            site_home = 'https://sizeer.de'
            pid_split = 'Produktcode: '

        # Getting sizes information
        soup_response = BeautifulSoup(response.body, 'lxml')
        sizes_raw_list = soup_response.find_all('p', class_='m-productDescr_sizeItem')
        if not len(sizes_raw_list):
            filtered_sizes = False

        for one_size in sizes_raw_list:
            json_s_p_dict = {}

            size = one_size.a.text.split()[0]
            good_size = self.filter_sizes(size)
            if not good_size:
                continue

            filtered_sizes = False
            size_pid = one_size.a['data-value']

            # Creating the Dictionary containing sizes and pids
            json_s_p_dict = {
                'size': size,
                'variant': size_pid,
                'in stock': True
            }

            sizes_pids_dict[size] = size_pid
            size_list.append(size)
            json_sizes_pids_list.append(json_s_p_dict)

        # Getting title, PID and image
        prod_title_pid = soup_response.find('div', class_='m-productDescr_header')
        prod_title = prod_title_pid.h1.text.strip()
        prod_pid = prod_title_pid.p.text.strip().split(pid_split)[1]
        prod_image = 'https://images.weserv.nl/?url=' + site_home + \
                     soup_response.find('img', class_='m-offerGallery_picture js-gallery_picture')['src']
        new_prod_price = int(soup_response.find('div', class_='s-newPrice').text.strip().split(',')[0])

        try:
            old_prod_price = int(soup_response.find('div', class_='s-oldPrice').text.strip().split(',')[0])
        except:
            old_prod_price = new_prod_price

        product_dict = {
            'pid': prod_pid,
            'title': prod_title,
            'image': prod_image,
            'old price': old_prod_price,
            'new price': new_prod_price
        }

        return size_list, sizes_pids_dict, product_dict, json_sizes_pids_list, filtered_sizes

    def reload_until_product_gets_instock(self, client, user_agent, task_number, from_monitor):
        """

        A function used in order to retrieve once the product is in stock

        Returns ->
                 ~ size_list -> False if product is OOS
                 ~ sizes_pids_dict -> False if product is OOS
                 ~ json_sizes_pids_list -> False if product is OOS
                 ~ cp_challenge -> True or False:
                        if the session needs abck cookie before doing anymore requests
        """
        max_retries = 3
        increment = 0

        while True:
            sizeer_link_uncached = self.randomize_link(task_number, self.product_link[task_number])
            sizes_filtered = True

            self.client_by_fastest_instance[task_number] = {}
            self.response_by_fastest_instance[task_number] = {}
            self.failed_getting_product_page[task_number] = 0
            self.got_product_page[task_number] = 0

            try:
                instance_counter = 0
                instances_number = 1
                uncaching_discount_task = False

                if 'attack' in self.task_mode[task_number]:
                    instances_number = self.instances_for_atacking

                while instance_counter < instances_number:
                    threading.Thread(target=self.retrieve_product_information_request,
                                     args=[client, user_agent, task_number,
                                           uncaching_discount_task, instance_counter]).start()

                    instance_counter += 1
                    sleep(0.5)

                while not self.got_product_page[task_number]:
                    if self.failed_getting_product_page[task_number] == instances_number:
                        return self.kill_task(task_number, step="Just Disable"), False, False

                    sleep(0.1)

                fastest_instance = self.got_product_page[task_number] - 1
                client = self.client_by_fastest_instance[task_number][fastest_instance]
                response = self.response_by_fastest_instance[task_number][fastest_instance]

            except Exception:
                logs = f"Error while waiting for product to get in stock. [HANDLING]"
                self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

                continue_module = self.count_error(task_number)
                if not continue_module:
                    return False, False, False, False

                traceback.print_exc()
                continue

            if response.status != 200:
                self.has_failed_reloading[task_number] = True

                logs = f"Wrong Response Code While Reloading. [{response.status}]"
                self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

                return False, False, False, False

            if 'cp_challenge' in response.body:
                return True, False, False, True

            soup_response = BeautifulSoup(response.body, 'lxml')
            sizes_raw_list = soup_response.find_all('p', class_='m-productDescr_sizeItem')
            size_list = []
            json_s_p_dict = {}
            sizes_pids_dict = {}
            json_sizes_pids_list = []

            if not sizes_raw_list and 'm-btn m-btn_primary js-pre-add-cart' in response.body:
                atc_variant = soup_response.find('a', class_='m-btn m-btn_primary js-pre-add-cart')['data-offer-id']
                size = 'N/A'
                size_pid = atc_variant

                # Creating the Dictionary containing sizes and pids
                json_s_p_dict = {
                    'size': size,
                    'variant': size_pid,
                    'in stock': True
                }

                sizes_pids_dict[size] = size_pid
                size_list.append(size)
                json_sizes_pids_list.append(json_s_p_dict)

                logs = f"Product IN STOCK!"
                self.tools.print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX, task_number)

                return size_list, sizes_pids_dict, json_sizes_pids_list, False

            elif sizes_raw_list:
                for one_size in sizes_raw_list:
                    size = one_size.a.text.split()[0]
                    good_size = self.filter_sizes(size)
                    if not good_size:
                        continue

                    sizes_filtered = False
                    size_pid = one_size.a['data-value']

                    # Creating the Dictionary containing sizes and pids
                    json_s_p_dict = {
                        'size': size,
                        'variant': size_pid,
                        'in stock': True
                    }

                    sizes_pids_dict[size] = size_pid
                    size_list.append(size)
                    json_sizes_pids_list.append(json_s_p_dict)
                if sizes_filtered:
                    logs = f"NO SIZE LEFT after filtering. Filters: {self.selected_sizes}"
                    self.tools.print_logs(logs, self.store_name, Fore.LIGHTMAGENTA_EX, task_number)

                else:
                    logs = f"Product IN STOCK!"
                    self.tools.print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX, task_number)

                return size_list, sizes_pids_dict, json_sizes_pids_list, False

            if not sizes_raw_list:
                sizes_filtered = False

            if from_monitor:
                increment += 1
                if increment >= max_retries:
                    return False, False, False, False

            logs = f"Product OUT OF STOCK. Retrying later..."
            self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

            sleep(random.randint(1, 3))

    def add_to_cart_script(self, client, user_agent, prod_pid,
                           task_number, chosen_size,
                           in_preload=False,
                           uncaching_discount_task=False,
                           create_preload=False):
        """A function used to add the item to cart"""
        retries = 0

        while True:
            site = "https://sizeer.ro/"
            if self.germany_region:
                site = "https://sizeer.de/"

            while not self.global_abck_cookie[task_number]:
                sleep(0.5)

            # If we are in preload and have failed, we will change the abck cookie in order not to get flagged
            if not in_preload or retries:
                client.addCookie({
                    "url": site,
                    "name": "_abck",
                    "value": self.global_abck_cookie[task_number]
                })

            # In case we are uncaching discount, we are going to change the product link
            if uncaching_discount_task:
                product_link = self.uncaching_link[task_number]
            else:
                product_link = self.product_link[task_number]

            data = {
                'id': prod_pid,
                'transport': '',
                'qty': '1'
            }

            adata = json.dumps(data)
            content_length = len(str(adata).replace('"', '').replace(" ", '')) - 2

            headers = [
                ['method', 'POST'],
                ['authority', self.authority],
                ['scheme', 'https'],
                ['cache-control', 'no-cache'],
                ['accept', '*/*'],
                ['x-requested-with', 'XMLHttpRequest'],
                ['user-agent', str(user_agent)],
                ['content-length', str(content_length)],
                ['content-type', 'application/x-www-form-urlencoded; charset=UTF-8'],
                ['sec-gpc', '1'],
                ['origin', self.home_page],
                ['sec-fetch-site', 'same-origin'],
                ['sec-fetch-mode', 'cors'],
                ['sec-fetch-dest', 'empty'],
                ['referer', product_link],
                ['accept-encoding', 'gzip, deflate, br'],
                ['accept-language', 'en-US,en;q=0.9'],
                ['cookie', '']
            ]

            logs = f"Adding to cart..."
            self.tools.print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX, task_number)

            if create_preload:
                self.used_same_cookie[task_number] += 1
                if self.used_same_cookie[task_number] > 1:
                    self.has_failed_needs_restarting_with_new_cookie[task_number] = True
            else:
                self.has_failed_needs_restarting_with_new_cookie[task_number] = True

            try:
                atc_url = 'https://sizeer.ro/cart/pre-x-add'
                if self.germany_region:
                    atc_url = 'https://sizeer.de/cart/pre-x-add'

                # POST Method
                response = client.makeRequest(atc_url, {
                    "method": "POST",
                    "headers": headers,
                    "applicationData": data

                })

            except:
                logs = f"Error While Adding to cart... [TIMED OUT]"
                self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

                retries = self.check_added_to_cart_times(retries, task_number)
                continue_module = self.count_error(task_number)
                if not continue_module:
                    return False, False, False

                continue

            else:
                if 'ak-challenge' in response.body:
                    print(self.global_abck_cookie[task_number])
                    logs = f"Bad Cookie..."
                    self.tools.print_logs(logs, self.store_name, Fore.LIGHTMAGENTA_EX, task_number)

                    self.has_failed_needs_restarting_with_new_cookie[task_number] = True
                    self.max_retries[task_number] += 5

                    if self.preload_mode[task_number] or in_preload or create_preload:
                        self.bad_cookie_errors += 1
                        return False, False, False

                    continue_module = self.count_error(task_number)
                    if not continue_module:
                        return False, False, False

                    self.has_failed_needs_restarting[task_number] = True
                    return False, False, False

                else:
                    if 's-preCart_name' in response.body and 's-priceBox' in response.body:
                        logs = f"Item Succesfully Added to cart! [{chosen_size}]"
                        self.tools.print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX, task_number)

                        email, password = self.email[task_number], self.password[task_number]

                        continue_module = self.limit_tasks_to_one_discount(task_number,
                                                                           email,
                                                                           uncaching_discount_task)
                        if not continue_module:
                            return False, False, False

                        return client, email, password

                    elif 'enp.cart.item_add_error' in response.body:
                        logs = f"Item OUT OF STOCK while adding to cart... Retrying..."
                        self.tools.print_logs(logs, self.store_name, Fore.LIGHTMAGENTA_EX, task_number)

                        retries = self.check_added_to_cart_times(retries, task_number)
                        self.announce_enp_error(task_number)
                        size_variant, chosen_size = self.check_sizes_already_stored(task_number)
                        if size_variant:
                            continue

                        # If the item has gone out of stock, size_variant is False so we stop the checkout Process
                        return False, True, False

                    else:
                        response = self.check_response(task_number, response, step="ATC")
                        if not response:
                            return False, False, False

                        logs = f"Unknown ATC response..."
                        self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)
                        print(response.body)

                        continue_module = self.count_error(task_number)
                        if not continue_module:
                            return False, False, False

                        return False, False, False

    def login(self, client, user_agent, email, password,
              task_number, from_monitor, uncaching_discount_task=False):
        """Function used in order to login"""
        while True:
            try:
                logs = f"Logging in..."
                self.tools.print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX, task_number)

                referer = "https://sizeer.ro/"
                login_page = "https://sizeer.ro/login"
                post_login = "https://sizeer.ro/login_check"
                login_type = "Autentificare"
                if self.germany_region:
                    referer = "https://sizeer.de/"
                    login_page = "https://sizeer.de/login"
                    post_login = "https://sizeer.de/login_check"
                    login_type = "Anmelden"

                headers = [
                    ['method', 'GET'],
                    ['authority', self.authority],
                    ['scheme', 'https'],
                    ['cache-control', 'max-age=0'],
                    ['upgrade-insecure-requests', '1'],
                    ['user-agent', str(user_agent)],
                    ['accept',
                     'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'],
                    ['sec-gpc', '1'],
                    ['sec-fetch-site', 'same-origin'],
                    ['sec-fetch-mode', 'navigate'],
                    ['sec-fetch-user', '?1'],
                    ['sec-fetch-dest', 'document'],
                    ['referer', referer],
                    ['accept-encoding', 'gzip, deflate, br'],
                    ['accept-language', 'en-US,en;q=0.9'],
                    ['cookie', '']
                ]

                try:
                    # GET Request
                    response = client.makeRequest(login_page, {
                        "method": "GET",
                        "headers": headers
                    })

                except:
                    logs = f"Error Getting Login Page! [TIMED OUT] "
                    self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

                    continue_module = self.count_error(task_number)
                    if not continue_module:
                        return False

                    continue

                else:
                    response = self.check_response(task_number, response, step="Getting Login")
                    if not response:
                        return False

                    login_token = \
                        BeautifulSoup(response.body, 'lxml').find('input', id='enp_customer_form_login__token')[
                            'value']

                    headers, data = self.prepare_login_credidentials(user_agent, email,
                                                                     password, login_token,
                                                                     login_page, login_type)

                    try:
                        # POST Request
                        response = client.makeRequest(post_login, {
                            "method": "POST",
                            "headers": headers,
                            "body": data
                        })

                    except:
                        logs = f"Error posting login data. [TIMED OUT]"
                        self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

                        continue_module = self.count_error(task_number)
                        if not continue_module:
                            return False

                        continue

                    else:
                        response = self.check_response(task_number, response, step="Logging in")
                        if not response:
                            return False

                        if response.url == referer or response.url == referer[:-1]:
                            logs = f"Logged in! [{email}]"
                            self.tools.print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX, task_number)

                            self.logged_in[task_number] = True

                            return client

                        else:
                            logs = f"Failed to login..."
                            self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

                            sleep(2)
                            return False
            except:
                logs = f"Failed proceeding with the login step..."
                self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

                traceback.print_exc()

                continue_module = self.count_error(task_number)
                if not continue_module:
                    return False

                # traceback.print_exc()
                continue

    def get_shipping(self, client, user_agent, task_number, email):
        """

        A function used in order to retrieve the shipping Token required in order to submit Shipping Form.

        It checks:
            1. Wether the product we have added to cart has gone or not OUT OF STOCK.
                ~if it went out of stock [enp.cart_error] -> It will announce the fact that
                    the specific size is not available anymore.

            2. What size we have in our cart
                ~if the bot wasn't able to determine the size successfully -> It will look up for the size
                    and use the filters to see if that size is the size we have been looking for.

            3. If the discount has successfully applied
                ~if the discount failed to apply, it will retry to debug the price

        """

        while True:
            try:
                logs = f"Getting shipping Page..."
                self.tools.print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX, task_number)

                headers = [
                    ['method', 'GET'],
                    ['authority', self.authority],
                    ['scheme', 'https'],
                    ['cache-control', 'no-cache'],
                    ['upgrade-insecure-requests', '1'],
                    ['user-agent', user_agent],
                    ['accept',
                     'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'],
                    ['sec-gpc', '1'],
                    ['sec-fetch-site', 'same-origin'],
                    ['sec-fetch-mode', 'navigate'],
                    ['sec-fetch-user', '?1'],
                    ['sec-fetch-dest', 'document'],
                    ['referer', self.product_link[task_number]],
                    ['accept-encoding', 'gzip, deflate, br'],
                    ['accept-language', 'en-US,en;q=0.9'],
                    ['cookie', '']
                ]

                try:
                    get_shipping_url = 'https://sizeer.ro/cos/adresa'
                    if self.germany_region:
                        get_shipping_url = 'https://sizeer.de/warenkorb/adresse'

                    # GET Request
                    response = client.makeRequest(get_shipping_url, {
                        "method": "GET",
                        "headers": headers
                    })

                except:
                    logs = f"Error getting Shipping Page. [TIMED OUT]"
                    self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

                    continue_module = self.count_error(task_number)
                    if not continue_module:
                        return False, False, False

                    # traceback.print_exc()
                    continue

                else:
                    response = self.check_response(task_number, response, step="Getting Shipping")
                    if not response:
                        return False, False, False

                    client, reload_page = self.check_response_shipping(client, user_agent, response, task_number)
                    if not client:
                        return False, False, False

                    if reload_page:
                        continue

                    continue_checkout = self.check_invalid_size_shipping(response, task_number)
                    if not continue_checkout:
                        return False, False, False

                    continue_checkout = self.check_if_discount_applied_shipping(client, user_agent, response,
                                                                                task_number, email)
                    if not continue_checkout:
                        return False, False, False

                    soup_response = BeautifulSoup(response.body, 'lxml')
                    cart_token = soup_response.find('input', attrs={'id': 'cart_flow_address_step__token'})[
                        'value']

                    return client, cart_token, response

            except:
                logs = f"Failed Getting Shipping Page..."
                self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

                traceback.print_exc()

                continue_module = self.count_error(task_number)
                if not continue_module:
                    return False, False, False

                continue

    def submit_shipping(self, client, user_agent, task_number, cart_token, response):
        """A class used in order to submit shipping"""
        while True:
            try:
                logs = f"Submitting shipping details..."
                self.tools.print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX, task_number)

                get_shipping_url = 'https://sizeer.ro/cos/adresa'
                post_shipping = 'https://sizeer.ro/cos/adresa/salva'
                if self.germany_region:
                    get_shipping_url = 'https://sizeer.de/warenkorb/adresse'
                    post_shipping = 'https://sizeer.de/warenkorb/adresse/sparen'

                headers, data = self.set_formdata_and_headers_post_shipping(task_number, user_agent,
                                                                            get_shipping_url, cart_token,
                                                                            response)
                if not headers:
                    return False, False

                try:
                    # POST Request
                    response = client.makeRequest(post_shipping, {
                        "method": "POST",
                        "headers": headers,
                        "applicationData": data

                    })

                except:
                    logs = f"Error Submitting Shipping. [TIMED OUT]"
                    self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

                    continue_module = self.count_error(task_number)
                    if not continue_module:
                        return False, False

                    # traceback.print_exc()
                    continue

                else:
                    response = self.check_response(task_number, response, step="Submitting Shipping")
                    if not response:
                        return False, False

                    if get_shipping_url != response.url and post_shipping != response.url:
                        logs = f"Shipping Succesfully Submitted!"
                        self.tools.print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX, task_number)

                        return client, response

                    else:
                        if 'Token-ul CSRF este invalid' in response.body:
                            logs = f"Failed to Submit Shipping! [Invalid Token]"
                            self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

                            continue_module = self.count_error(task_number)
                            if not continue_module:
                                return False, False

                            client, cart_token, response = self.get_shipping(client, user_agent,
                                                                             task_number, self.email[task_number])
                            if not client:
                                return False, False

                            continue

                        else:
                            logs = f"Failed to Submit Shipping!"
                            self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

                            print(response.url)
                            print(response.body)

                            return False, False

            except:
                logs = f"Failed Submitting Shipping... [INDEX ERROR]"
                self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

                traceback.print_exc()

                continue_module = self.count_error(task_number)
                if not continue_module:
                    return False, False

                continue

    def get_order_page(self, client, user_agent, task_number, email,
                       response, get_order_page=False):
        """Function used in order to retrieve the Cart Token"""
        enforce_reload = False

        while True:
            try:
                logs = f"Getting Cart Token..."
                self.tools.print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX, task_number)

                shipping_url = 'https://sizeer.ro/cos/adresa'
                get_cart_link = 'https://sizeer.ro/cos/sumar'
                if self.germany_region:
                    shipping_url = 'https://sizeer.de/warenkorb/adresse'
                    get_cart_link = 'https://sizeer.de/warenkorb/zusammenfassung'

                if self.is_dunk and not self.preload_mode[task_number]:
                    self.entered_dead_zone[email] = True

                if self.germany_region or get_order_page or enforce_reload:
                    client, response, \
                        continue_loop, break_loop = self.get_cart_page(task_number, client,
                                                                       user_agent, shipping_url,
                                                                       get_cart_link)

                    if continue_loop:
                        continue

                    if break_loop:
                        return False, False

                response = self.check_response(task_number, response, step="Getting Order Page")
                if not response:
                    return False, False

                if response.url == get_cart_link:
                    continue_script = self.check_if_discount_applied_last_step(client, user_agent,
                                                                               task_number, response,
                                                                               email)

                    if not continue_script:
                        return False, False

                    soup_response = BeautifulSoup(response.body, 'lxml')
                    cart_token = soup_response.find('input', attrs={'name': 'cart_flow_summation_step[_token]'})[
                        'value']

                    return client, cart_token

                else:
                    logs = f"Product OUT OF STOCK. [CART PAGE] [{response.url}]"
                    self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

                    self.announce_enp_error(task_number)

                    # Emptying cart and retrying with a different pair
                    client, out_of_stock = self.out_of_stock_handler_dunks(client, user_agent, task_number, last_step)
                    if client:
                        enforce_reload = True

                        continue

                    if not client and out_of_stock:
                        return False, False

                    continue_module = self.count_error(task_number)
                    if not continue_module:
                        return False, False

                    self.has_failed_needs_restarting[task_number] = True

                    return False, False
            except:
                logs = f"Failed while Getting Order Page... [INDEX ERROR]"
                self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

                traceback.print_exc()
                continue_module = self.count_error(task_number)
                if not continue_module:
                    return False, False

                continue

    def submit_order(self, client, user_agent, email, task_number, cart_token):
        """A function used in order to submit the order"""
        self.second_try_placing_order[task_number] = False
        while True:
            try:
                shipping_url = 'https://sizeer.ro/cos/adresa'
                get_cart_link = 'https://sizeer.ro/cos/sumar'
                if self.germany_region:
                    shipping_url = 'https://sizeer.de/warenkorb/adresse'
                    get_cart_link = 'https://sizeer.de/warenkorb/zusammenfassung'

                data = {
                    'cart_flow_summation_step[_token]': cart_token
                }

                if self.germany_region and not self.logged_in[task_number]:
                    # Possible bug upon placing order if they change the Consent Token
                    data = {
                        'cart_flow_summation_step[consentForm][consent_1746][]': '1746',
                        'cart_flow_summation_step[_token]': cart_token
                    }

                adata = json.dumps(data)
                content_length = len(str(adata).replace('"', '').replace(" ", '')) - 2

                headers = [
                    ['method', 'POST'],
                    ['authority', self.authority],
                    ['scheme', 'https'],
                    ['cache-control', 'max-age=0'],
                    ['sec-ch-ua-mobile', '?0'],
                    ['upgrade-insecure-requests', '1'],
                    ['origin', self.home_page],
                    ['content-length', str(content_length)],
                    ['content-type', 'application/x-www-form-urlencoded'],
                    ['user-agent', user_agent],
                    ['accept',
                     'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'],
                    ['sec-fetch-site', 'same-origin'],
                    ['sec-fetch-mode', 'navigate'],
                    ['sec-fetch-user', '?1'],
                    ['sec-fetch-dest', 'document'],
                    ['referer', get_cart_link],
                    ['accept-encoding', 'gzip, deflate, br'],
                    ['accept-language', 'en-US,en;q=0.9'],
                    ['cookie', '']
                ]

                # If we are on Romanian version, checkout it s much faster so we don't have to get the cart page
                # for the token
                if not self.germany_region:
                    headers[14][1] = shipping_url

                logs = f"Placing Order..."
                self.tools.print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX, task_number)

                if self.is_dunk:
                    threading.Thread(target=self.deactivate_coupon_before_checkout,
                                     args=[task_number]).start()

                    sleep(0.15)

                try:
                    post_order_link = 'https://sizeer.ro/cos/sumar/salva'
                    if self.germany_region:
                        post_order_link = 'https://sizeer.de/warenkorb/zusammenfassung/sparen'

                    # POST Request
                    response = client.makeRequest(post_order_link, {
                        "method": "POST",
                        "headers": headers,
                        "applicationData": data

                    })

                except:
                    logs = f"Error Placing Order. [TIMED OUT]"
                    self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

                    self.second_try_placing_order[task_number] = True
                    continue_module = self.count_error(task_number)
                    if not continue_module:
                        return False

                    continue

                else:
                    response = self.check_response(task_number, response, step="Placing Order")
                    if not response:
                        return False

                    if self.is_dunk:
                        checked_out = True
                        threading.Thread(target=self.apply_discount,
                                         args=[task_number, email, checked_out]).start()

                        checked_out, coupon_preserved = self.send_webhook_dunks(task_number, response, email)
                        self.has_succesfully_checked_out[task_number] = True
                        self.checked_out[task_number] = checked_out
                        self.coupon_preserved[task_number] = coupon_preserved

                        return client

                    else:
                        self.send_webhook_guest(task_number, response, email)
                        self.has_succesfully_checked_out[task_number] = True

                        return client

            except:
                logs = f"Failed while trying to Place Order..."
                self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

                traceback.print_exc()
                continue_module = self.count_error(task_number)
                if not continue_module:
                    return False

                continue

    # -----------------MINI FUNCTIONS------------------
    def get_order_number(self, body):
        """A mini function used in order to scrape for the order number"""
        try:
            order_nr = BeautifulSoup(body, 'lxml').find('input', attrs={'name': 'ordernr'})['value']

        except:
            order_nr = "COULDN'T RETRIEVE"

        return order_nr

    def get_order_number_ro(self, body):
        """A mini function used in order to scrape the Romanian website for the order number"""
        try:
            order_nr = BeautifulSoup(body, "lxml").find('p', class_="m-typo m-typo_primary").text.split(":")[1]
        except:
            order_nr = "COULDN'T RETRIEVE"

        return order_nr

    # -------------------------------------------------

    # -----------------SYSTEM FUNCTIONS-----------------
    def create_client_session(self, task_number):
        """Creating the client session"""
        filename = ""
        if self.task_creates_preload:
            # means we need specific region proxies
            if 'ro' in self.authority:
                filename = 'preload_proxies_ro.txt'

            elif 'de' in self.authority:
                filename = 'preload_proxies_de.txt'

            else:
                return False, False, False, False

        proxy = BotTools().pick_random_proxy_tls(filename)
        proxy_akam = proxy.split('://')[1].split('/')[0]
        self.proxy_akam[task_number] = proxy_akam

        client = TLS_CLIENT({
            "type": "chrome",
            "proxy": proxy,
            "cookieJar": True,
            "enableCookieJar": True,
            "timeout": 10

        })
        user_agent = BotTools().get_user_agents()

        return client, proxy, proxy_akam, user_agent

    def set_germany_variables(self):
        """Function used in order to set the germany values"""
        self.is_dunk = False
        self.germany_region = True
        csv_path = 'sizeer_germany_test.csv'
        self.authority = 'sizeer.de'
        self.cid = ' DE'
        self.home_page = 'https://sizeer.de'
        self.payment_method = 'Paypal'

    def set_if_preload_set_if_dunk_set_if_germany_region(self, product_link, mode):
        """Function used in order to set the starting variables"""
        germany_region = False

        # Setting to see if the product is a dunk or a jordan
        if 'dunk' in product_link:
            self.is_dunk = True
        else:
            self.is_dunk = False

        if 'sizeer.de' in product_link:
            self.set_germany_variables()

    def set_system_variables(self, product_link,
                             max_checkouts,
                             full_throttle,
                             enough_bad_cookies,
                             farm_points_session,
                             do_preload,
                             sizes_selected,
                             instances_for_atacking,
                             task_category):
        """Variables used in order to setup different modules settings"""
        self.bad_cookie_errors = 0
        self.enough_bad_cookies = enough_bad_cookies
        self.task_creates_preload = do_preload
        self.selected_sizes = sizes_selected
        self.store_name = f"SIZEER{self.cid}"
        self.instances_for_atacking = instances_for_atacking
        self.task_category = task_category
        self.farm_points_session = farm_points_session

        # Setting the max checkouts for bad products
        self.max_checkouts = max_checkouts

        if not do_preload:
            self.real_product_link = product_link

        # Setting the enp_cart value that tells us wether we've encountered or not that error as of yet
        self.enp_cart_error = False
        self.sizes_not_written_out = True

        # If this is set to True, it doesn't stop to enp.cart_error
        self.full_throttle = full_throttle

    def load_available_accounts_and_csv(self, task_category, create_preload):
        """

        Function used in order to load the information for each task.

        If we have a dunk, we will search how many available accounts we have by the task category:
            It can either be:
                ~ Dunk Low Adults
                ~ Dunk Low Kids
                ~ Dunk High Adults
                ~ Currently dunk high juniors not supported ~
        """
        try:
            profile = 'profiles.csv'
            if self.germany_region:
                profile = 'germany_profiles.csv'

            sizeer_profiles = LoadProfiles().get_profile_data(profile)

            if not self.is_dunk and not create_preload:
                task_category = 'simple_accounts.json'

            if self.germany_region:
                task_category = 'germany_simple_accounts.json'

            available_accounts = JsonClass().retrieve_dunks_accounts_by_category(task_category)
            if not available_accounts:
                logs = 'No available accounts!'
                self.tools.print_logs(logs, self.store_name, Fore.RED, task_mode='SYSTEM')

                return False

            no_of_accounts = len(available_accounts)
            self.number_of_profiles = no_of_accounts

            return sizeer_profiles, available_accounts

        except:
            logs = 'Error to retrieve profiles'
            self.tools.print_logs(logs, self.store_name, Fore.RED, task_mode='SYSTEM')
            traceback.print_exc()

            return False

    def reduce_number_of_tasks_to_profiles_number(self, number_of_tasks, profiles, accounts, mode):
        """Reducing the number of tasks prior to the number of profiles"""
        increment = 0
        profiles_copy = dict(profiles[0])

        while increment < number_of_tasks:
            if increment >= self.number_of_profiles:
                break
            else:
                accounts_dict = dict(accounts[increment])
                email = accounts_dict["email"]
                password = accounts_dict["password"]

                self.profiles_by_task_number[increment] = profiles_copy
                self.profiles_by_task_number[increment]["EMAIL"] = email
                self.profiles_by_task_number[increment]["PASSWORD"] = password
                self.accounts_used.append(accounts_dict)

            increment += 1

        lowest_number = number_of_tasks
        if self.number_of_profiles < number_of_tasks:
            lowest_number = self.number_of_profiles

        no_of_profiles = len(profiles)
        no_of_accounts = len(accounts)

        if no_of_profiles > 1:
            s = 's'
        else:
            s = ''

        logs = f'LOADED {no_of_profiles} profile{s} and {lowest_number} accounts. ' \
               f'Total accounts: {no_of_accounts}. [{mode} mode]'
        self.tools.print_logs(logs, self.store_name, Fore.LIGHTMAGENTA_EX, task_mode='SYSTEM')

        return lowest_number

    def assign_first_profile_to_all_tasks(self, number_of_tasks, profiles, accounts, mode):
        """If we are on a normal session"""
        increment = 0
        chosen_profile = dict(profiles[0])
        password = accounts[0]["password"]
        email = accounts[0]["email"]

        while increment < number_of_tasks:
            chosen_profile["EMAIL"] = email
            chosen_profile["PASSWORD"] = password

            self.profiles_by_task_number[increment] = chosen_profile

            increment += 1

        no_of_profiles = len(profiles)
        if no_of_profiles > 1:
            s = 's'
        else:
            s = ''

        logs = f'LOADED {no_of_profiles} profile{s} and {number_of_tasks} Tasks. [{mode} mode]'
        self.tools.print_logs(logs, self.store_name, Fore.LIGHTMAGENTA_EX, task_mode='SYSTEM')

    def load_another_avail_acc(self, avail_accs):
        """

        Takes a random account from the available accounts that is not used
        and that doesn't appear in self.accounts_used variable

        """

        i = len(avail_accs) - 1
        while i > 0:
            if avail_accs[i] not in self.accounts_used:
                acc_dict = avail_accs[i]
                self.accounts_used.append(acc_dict)

                return acc_dict

            i -= 1

        return None

    def count_error(self, task_number, atacking_instance=False):
        """
        Function used in order to announce the system when an error has been made
        If the task has hit the maximum numbers of retrys, task is being killed by the system
        """
        nr = 1
        if atacking_instance:
            nr = 1 / (int(self.instances_for_atacking) * 4)

        self.max_retries[task_number] += nr

        if self.max_retries[task_number] >= self.global_max_retries[task_number]:
            logs = f"MAXIMUM RETRIES REACHED!"
            self.tools.print_logs(logs, self.store_name, Fore.LIGHTRED_EX, task_number)

            return False

        return True

    # -------------------------------------------------

    # -----------------TASKS FUNCTIONS-----------------
    def set_tasks_variables(self, task_number,
                            do_preload,
                            continue_checkouts,
                            has_failed,
                            product_link,
                            max_retries_limit,
                            needs_new_cookie,
                            task_mode=""):
        """Setting each task variables"""
        self.mobile.set_beggining_variables(task_number)

        if not has_failed or needs_new_cookie:
            self.global_abck_cookie[task_number] = ""

        start_time = int(time())
        self.start_time_dict[str(task_number)] = start_time
        self.preload_mode[task_number] = do_preload
        self.has_failed_needs_restarting[task_number] = False
        self.has_failed_needs_restarting_with_new_cookie[task_number] = False
        self.has_succesfully_checked_out[task_number] = False
        self.prepare_session_early[task_number] = False
        self.has_failed_reloading[task_number] = False

        if task_mode:
            self.task_mode[task_number] = task_mode

        if continue_checkouts:
            self.continue_script[task_number] = True

        if not has_failed and do_preload:
            self.used_same_cookie[task_number] = 0

        if do_preload:
            self.lost_session[task_number] = False

        if self.is_dunk:
            self.checked_out[task_number] = False
            self.coupon_preserved[task_number] = False

        # Using everything as a dict cause multithreading likes to mess things up bad.
        # Each task has it's assigned value with the task number as dict key.

        if not has_failed:
            self.max_retries[task_number] = 0
            self.logged_in[task_number] = False

        if product_link:
            self.product_link[task_number] = product_link
        if max_retries_limit:
            self.global_max_retries[task_number] = max_retries_limit

    def login_app_client(self, task_number, email, password):
        """Function used in order to login the client on mobile app"""
        while True:
            try:
                self.mobile_client[task_number], self.app_access_token[task_number], \
                    self.app_unique_id[task_number] = self.mobile.login(email, password, task_number)

                return
            except:
                traceback.print_exc()
                logs = 'Error while passing in Mobile Client.'
                self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

                continue_module = self.count_error(task_number)
                if not continue_module:
                    return

                sleep(2)
                continue

    def randomize_link(self, task_number, link):
        """Function used in order to randomize the link by adding 2 different random strings"""
        S = 5  # number of characters in the string.
        # call random.choices() string module to find the string in Uppercase + numeric data.
        ran1 = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=S))
        ran2 = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=S))
        sizeer_link_uncached = f"{link}?{ran1}={ran2}"

        return sizeer_link_uncached

    def prepare_session_for_more_checkouts(self, task_number, email, max_retries_limit, get_new_cookie):
        """

        A function used in order to do continue running the script,
        getting rid of the etra steps in order to gain speed

        """
        logs = "Redoing the checkout proccess..."
        self.tools.print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX, task_number)

        self.entered_dead_zone[email] = False
        task_mode = self.task_mode[task_number] + " [in]"

        self.set_tasks_variables(task_number,
                                 do_preload=False,
                                 continue_checkouts=True,
                                 has_failed=True,
                                 product_link=self.real_product_link,
                                 max_retries_limit=max_retries_limit,
                                 needs_new_cookie=get_new_cookie,
                                 task_mode=task_mode)

        if get_new_cookie:
            threading.Thread(target=self.get_valid_akamai_cookie_api,
                             args=[self.proxy_akam[task_number], task_number]).start()

        return

    def prepare_login_credidentials(self, user_agent, email, password, login_token, referer, login_type):
        """Function used in order to prelucrate login infos"""
        data = f'enp_customer_form_login[username]={email}' \
               f'&enp_customer_form_login[password]={password}' \
               f'&_submit={login_type}' \
               f'&enp_customer_form_login[_token]={login_token}'
        adata = data.replace('"', '').replace(" ", '')
        content_length = len(str(adata))

        headers = [
            ['method', 'POST'],
            ['authority', self.authority],
            ['scheme', 'https'],
            ['cache-control', 'max-age=0'],
            ['upgrade-insecure-requests', '1'],
            ['origin', self.home_page],
            ['content-length', str(content_length)],
            ['content-type', 'application/x-www-form-urlencoded'],
            ['user-agent', str(user_agent)],
            ['accept',
             'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'],
            ['sec-gpc', '1'],
            ['sec-fetch-site', 'same-origin'],
            ['sec-fetch-mode', 'navigate'],
            ['sec-fetch-user', '?1'],
            ['sec-fetch-dest', 'document'],
            ['referer', referer],
            ['accept-encoding', 'gzip, deflate, br'],
            ['accept-language', 'en-US,en;q=0.9'],
            ['cookie', ''],
        ]

        return headers, data

    def check_client_logged_in(self, task_number):
        """Function used in order to check and see if the client has logged in"""
        try:
            self.mobile_client[task_number]
        except:
            # If we get this error means tasks still haven't logged in the app
            logs = f"Waiting for app tasks to login..."
            self.tools.print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX, task_number)

            retries = 0
            logged_in = False
            while retries < 2:
                # Waiting around 1.5 more seconds
                try:
                    self.mobile_client[task_number]
                    logged_in = True
                    break
                except:
                    sleep(0.5)
                    retries += 1

            if not logged_in:
                logs = f"Exceeded default time for logging in..."
                self.tools.print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX, task_number)

                profiles_number = task_number % (self.number_of_profiles)
                email = self.profiles_by_task_number[profiles_number]['EMAIL']
                password = self.profiles_by_task_number[profiles_number]['PASSWORD']

                try:
                    from multiprocessing.pool import ThreadPool
                    pool = ThreadPool(processes=1)

                    async_result = pool.apply_async(self.mobile.login,
                                                    (email, password, task_number))

                    self.mobile_client[task_number], self.app_access_token[task_number], \
                        self.app_unique_id[task_number] = async_result.get()

                except:
                    traceback.print_exc()
                    logs = f"Error while passing in Mobile Client."
                    self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

    def check_added_to_cart_times(self, retries, task_number):
        """Used in case we fail while adding to cart"""
        retries += 1
        max_retries = 3

        if retries % max_retries == 0:
            self.global_abck_cookie[task_number] = ""

            threading.Thread(target=self.get_valid_akamai_cookie_api,
                             args=[self.proxy_akam[task_number], task_number]).start()

        return retries

    def check_size_list(self, client, user_agent, task_number, size_list, sizes_pids_dict,
                        json_sizes_pids_list, from_monitor, filtered_sizes):
        """

        Function used in order to check wether the product has gone out of stock or not

        Returns ->
                 ~ size_list -> False if product is OOS
                 ~ sizes_pids_dict -> False if product is OOS
                 ~ json_sizes_pids_list -> False if product is OOS
                 ~ cp_challenge -> True or False:
                        if the session needs abck cookie before doing anymore requests
        """
        if not size_list:
            if filtered_sizes:
                logs = f"NO SIZE LEFT after filtering. Filters: {self.selected_sizes}"
                self.tools.print_logs(logs, self.store_name, Fore.LIGHTMAGENTA_EX, task_number)

                return False, False, False, False

            if self.preload_mode[task_number]:
                logs = f"Dummy sold out, please readjust."
                self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

                return False, False, False, False

            logs = f"Product OUT OF STOCK. Retrying..."
            self.tools.print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX, task_number)

            size_list, sizes_pids_dict, \
                json_sizes_pids_list, cp_challenge = self.reload_until_product_gets_instock(client, user_agent,
                                                                                            task_number, from_monitor)

            if cp_challenge:
                return False, False, False, True

            if not size_list:
                return False, False, False, False

        return size_list, sizes_pids_dict, json_sizes_pids_list, False

    def pick_size(self, task_number, prod_sku, size_list, json_size_variant_dict):
        """
        Function used in order to pick randomly the sizes

        In case one size goes Out of stock, we also modify a json file where
        we let the bot know that it has gone Out of Stock.
        """

        if self.preload_mode[task_number]:
            # If we just started preloading, it means that we don't have to filter the sizes
            # because we are carting an always in stock item
            random_size = random.choice(size_list)
            self.chosen_size_dict[str(task_number)] = random_size

        else:
            self.real_sku = prod_sku
            # If we are not in the preload mode, we will act normal
            if not self.enp_cart_error:
                if self.sizes_not_written_out:
                    self.prelucrate_sizes(task_number,
                                          prod_sku,
                                          json_size_variant_dict,
                                          size_list,
                                          fresh_product=True)

                    self.sizes_not_written_out = False

                random_size = random.choice(size_list)
                self.chosen_size_dict[str(task_number)] = random_size

                if len(size_list) == 1:
                    self.full_throttle = False

            else:
                new_size_list = self.prelucrate_sizes(task_number,
                                                      prod_sku,
                                                      json_size_variant_dict,
                                                      size_list,
                                                      size_went_oos=True,
                                                      size_list=self.sold_out_sizes)

                self.sold_out_sizes = []

                if not len(new_size_list):
                    print(f'[SIZEER{self.cid}] [TASK NUMBER {task_number}] [{datetime.datetime.now()}]\t'
                          f'NO SIZES LEFT.')

                    # Only if it's a dunk we're going to write the updated accounts availability
                    if self.is_dunk:
                        self.all_sizes_sold_out = True
                        JsonClass().update_each_account_general_information(
                            self.disabled_accounts_list_json[task_number])

                    return False

                random_size = random.choice(new_size_list)
                self.chosen_size_dict[str(task_number)] = random_size

        return random_size

    def prelucrate_sizes(self, task_number,
                         prod_pid,
                         json_size_variant_dict,
                         size_pids_dict,
                         size_went_oos=False,
                         fresh_product=False,
                         size_list=[]):
        """
        A function used in order to prelucrate the sizes json file

        size_went_oos = BOOL variable:
            True -> Update the size list saying it's out of stock

        fresh_product = Bool variable:
            True -> Create the Json File using the product pid and add the sizes.
        """
        string_today = timp.strftime("%Y_%m_%d_%H")
        filename = f"{prod_pid}_{string_today}.json"
        if fresh_product:
            main_dict = {
                "system": json_size_variant_dict,
                "bot": size_pids_dict
            }

            JsonClass().write_fresh_sizes_to_file(filename, main_dict)
            print(f'[SIZEER{self.cid}] [SYSTEM] [{datetime.datetime.now()}]\t'
                  f'Sizes succesfully written to the json file.')

        if size_went_oos:
            try:
                sizes_info = JsonClass().get_sizes(filename)
                sizes_info = self.remove_size_from_bot_availability(size_list, sizes_info)

                available_sizes = sizes_info['bot']

            except:
                traceback.print_exc()
                main_dict = {
                    "system": json_size_variant_dict,
                    "bot": size_pids_dict
                }
                # Means that we have a new hour
                JsonClass().write_fresh_sizes_to_file(filename, main_dict)

                print(f'[SIZEER{self.cid}] [SYSTEM] [{datetime.datetime.now()}]\t'
                      f'Sizes succesfully written to the json file.')

            else:
                JsonClass().write_fresh_sizes_to_file(filename, sizes_info)
                return available_sizes

    def check_sizes_already_stored(self, task_number):
        """

        A function used in order to retrieve the sizes from the json file

        It will:
            1. Try to remove a Sold Out size in case we have such
            2. Pick a random size out of all available sizes

        It returns the size variant and the size name
        """
        try:
            prod_sku = self.real_sku
            string_today = timp.strftime("%Y_%m_%d_%H")
            filename = f"{prod_sku}_{string_today}.json"
            initial_sizes_info = JsonClass().get_sizes(filename)

            sizes_info = self.remove_size_from_bot_availability(self.sold_out_sizes.copy(), initial_sizes_info)
            if len(sizes_info['bot']):
                random_size = random.choice(sizes_info['bot'])
                size_variant = ''

                if sizes_info != initial_sizes_info:
                    JsonClass().write_fresh_sizes_to_file(filename, sizes_info)

                for size_info in sizes_info["system"]:
                    if size_info['size'] == random_size:
                        size_variant = size_info["variant"]

                        break

                logs = f"Picked Size - {random_size}"
                self.tools.print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX, task_number)

                return size_variant, random_size
            else:
                logs = f"SIZES SOLD OUT. [{self.prod_title[task_number]}]"
                self.tools.print_logs(logs, self.store_name, Fore.LIGHTMAGENTA_EX, task_number)

                return False, False
        except:
            logs = "Error prelucrating sizes... [INDEX ERROR]"
            self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

            self.has_failed_needs_restarting[task_number] = True

            return False, False

    def remove_size_from_bot_availability(self, size_list, sizes_info):
        """A primary function used in order to remove the sizes that have gone out of stock"""
        system = sizes_info['system']

        for size_sold in size_list:
            iterator = 0

            for size_info in system:
                if str(size_info['size']) == str(size_sold):
                    system[iterator]["in stock"] = False
                    break

                iterator += 1

            try:
                sizes_info['bot'].remove(size_sold)
                print(f'[SIZEER{self.cid}] [SYSTEM] [{datetime.datetime.now()}]\t'
                      f'Size {size_sold} REMOVED from available sizes.')
            except:
                pass

        sizes_info['system'] = system
        for size in size_list:
            self.sold_out_sizes.remove(size)

        return sizes_info

    def check_response_shipping(self, client, user_agent, response, task_number):
        """

        A function used in order to check the response you get upon hitting the shipping page
        If you get redirected and not 403, means the product has gone out of stock.
        We have 2 cases:
            ~ We are checking out a dunk -> We clear the cart, reATC another size and continue
            ~ We are checking out a normal product -> reset session & start again without
                                                    requesting the product page.

        """
        get_shipping_url = 'https://sizeer.ro/cos/adresa'
        if self.germany_region:
            get_shipping_url = 'https://sizeer.de/warenkorb/adresse'

        simplified_response_list = response.url.split('sizeer')[1].split("/")
        simplified_response = "/"
        for simple_response in simplified_response_list:
            if '.' not in simple_response:
                simplified_response += f"{simple_response}/"

        if response.url != get_shipping_url:
            logs = f"Product OUT OF STOCK. [enp_cart_error] [{simplified_response}]"
            self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

            # We notice that the sizes have started to sell out
            self.announce_enp_error(task_number)

            # Instead of restarting the task, we are simply going
            # to remove the product and continue the checkout
            if self.is_dunk:
                client, out_of_stock = self.out_of_stock_handler_dunks(client, user_agent, task_number)
                if client:
                    return client, True

                if not client and out_of_stock:
                    return False, False

            else:
                proxy = f"http://{self.proxy_akam[task_number]}/"
                client = TLS_CLIENT({
                    "type": "chrome",
                    "proxy": proxy,
                    "cookieJar": True,
                    "enableCookieJar": True,
                    "timeout": 10

                })
                user_agent = BotTools().get_user_agents()

                self.checked_out_task_handler(client, user_agent, task_number, from_monitor=False,
                                              in_preload=False, email=self.email[task_number],
                                              max_retries_limit=None, uncaching_discount_task=False,
                                              get_new_cookie=False)

                return False, False

        return client, False

    def check_invalid_size_shipping(self, response, task_number):
        """A function used in order to check wether we have found what size we carted"""

        selected_size = self.chosen_size_dict[str(task_number)]
        if selected_size == 'N/A':
            my_size, good_size = self.get_size_from_shipping_page(response, task_number)

            if good_size and my_size != 'N/A':
                logs = f"Found size ~ {my_size}."
                self.tools.print_logs(logs, self.store_name, Fore.GREEN, task_number)

                self.chosen_size_dict[str(task_number)] = f"N/A ~ {my_size}"

            elif not good_size:
                logs = f"NO SIZE LEFT after filtering. Filters: {self.selected_sizes}"
                self.tools.print_logs(logs, self.store_name, Fore.LIGHTMAGENTA_EX, task_number)

                # We remove the size from the tasks because we don't need them to run anymore this size
                self.announce_enp_error(task_number)

                return False

        return True

    def check_if_discount_applied_shipping(self, client, user_agent, response, task_number, email):
        """A function used in order to check wether the discount has been applied or not"""
        if self.is_dunk:
            if 'Reducere' in response.body:
                logs = f"Discounted price Successfully applied!"
                self.tools.print_logs(logs, self.store_name, Fore.GREEN, task_number)

            else:
                logs = f"Discounted price failed to apply!"
                self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

                self.activated_discount[email] = False
                continue_module = self.count_error(task_number)
                if not continue_module:
                    return False

                discounted_succesfully = self.check_discounted(client, user_agent, task_number)
                if discounted_succesfully:
                    self.activated_discount[email] = True
                    return True

                self.has_failed_needs_restarting[task_number] = True

                return False

        return True

    def get_size_from_shipping_page(self, response, task_number):
        """Function used in order to check the size from the shipping page"""
        try:
            soup_response = BeautifulSoup(response.body, 'lxml')
            my_size = soup_response.find('meta', attrs={'property': 'product:size'})['content'].strip()

            return my_size, self.filter_sizes(my_size)

        except:
            traceback.print_exc()
            logs = f"Error filtering size. Check logs!"
            self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

            return 'N/A', True

    def set_formdata_and_headers_post_shipping(self, task_number, user_agent, get_shipping_url, cart_token, response):
        """

        A function used in order to set the headers and the formdata
        requested upon posting the shipping page

        """

        try:
            email, fn, ln, addy, house_number, city, zip, phone, province_id, new_phone = self.return_profile(
                task_number)
        except:
            logs = f"Error to retrieve profiles information"
            self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

            return False

        if 'de acord cu' in response.body:
            data = {
                'cart_flow_address_step[accountAddress][firstName]': fn,
                'cart_flow_address_step[accountAddress][lastName]': ln,
                'cart_flow_address_step[accountAddress][email]': email,
                'cart_flow_address_step[accountAddress][addressType]': 'person',
                'cart_flow_address_step[accountAddress][company]': '',
                'cart_flow_address_step[accountAddress][nip]': '',
                'cart_flow_address_step[accountAddress][phone]': new_phone,
                'cart_flow_address_step[accountAddress][province]': province_id,
                'cart_flow_address_step[accountAddress][postcode]': zip,
                'cart_flow_address_step[accountAddress][city]': city,
                'cart_flow_address_step[accountAddress][street]': addy,
                'cart_flow_address_step[accountAddress][houseNumber]': house_number,
                'cart_flow_address_step[accountAddress][apartmentNumber]': '',
                'cart_flow_address_step[sameTransportAddress]': '1',
                'cart_flow_address_step[transportAddress][company]': '',
                'cart_flow_address_step[transportAddress][firstName]': '',
                'cart_flow_address_step[transportAddress][lastName]': '',
                'cart_flow_address_step[transportAddress][phone]': '',
                'cart_flow_address_step[transportAddress][province]': '',
                'cart_flow_address_step[transportAddress][postcode]': '',
                'cart_flow_address_step[transportAddress][city]': '',
                'cart_flow_address_step[transportAddress][street]': '',
                'cart_flow_address_step[transportAddress][houseNumber]': '',
                'cart_flow_address_step[transportAddress][apartmentNumber]': '',
                'cart_flow_address_step[sameBillingAddress]': '1',
                'cart_flow_address_step[billingAddress][firstName]': '',
                'cart_flow_address_step[billingAddress][lastName]': '',
                'cart_flow_address_step[billingAddress][addressType]': 'person',
                'cart_flow_address_step[billingAddress][company]': '',
                'cart_flow_address_step[billingAddress][nip]': '',
                'cart_flow_address_step[billingAddress][phone]': '',
                'cart_flow_address_step[billingAddress][postcode]': '',
                'cart_flow_address_step[billingAddress][city]': '',
                'cart_flow_address_step[billingAddress][street]': '',
                'cart_flow_address_step[billingAddress][houseNumber]': '',
                'cart_flow_address_step[billingAddress][apartmentNumber]': '',
                'checkall': 'on',
                'cart_flow_address_step[consentForm][consent_2715][]': '2715',
                'cart_flow_address_step[consentForm][consent_2723][]': '2723',
                'cart_flow_address_step[consentForm][consent_2719][]': '2719',
                'cart_flow_address_step[consentForm][consent_1529][]': '1529',
                'cart_flow_address_step[transportAddress][addressType]': 'person',
                'cart_flow_address_step[billingAddress][province]': province_id,
                'cart_flow_address_step[customerComment]': '',
                'cart_flow_address_step[_token]': cart_token
            }

        else:
            data = {
                'cart_flow_address_step[accountAddress][firstName]': fn,
                'cart_flow_address_step[accountAddress][lastName]': ln,
                'cart_flow_address_step[accountAddress][email]': email,
                'cart_flow_address_step[accountAddress][addressType]': 'person',
                'cart_flow_address_step[accountAddress][company]': '',
                'cart_flow_address_step[accountAddress][nip]': '',
                'cart_flow_address_step[accountAddress][phone]': new_phone,
                'cart_flow_address_step[accountAddress][province]': province_id,
                'cart_flow_address_step[accountAddress][postcode]': zip,
                'cart_flow_address_step[accountAddress][city]': city,
                'cart_flow_address_step[accountAddress][street]': addy,
                'cart_flow_address_step[accountAddress][houseNumber]': house_number,
                'cart_flow_address_step[accountAddress][apartmentNumber]': '',
                'cart_flow_address_step[sameTransportAddress]': '1',
                'cart_flow_address_step[transportAddress][company]': '',
                'cart_flow_address_step[transportAddress][firstName]': '',
                'cart_flow_address_step[transportAddress][lastName]': '',
                'cart_flow_address_step[transportAddress][phone]': '',
                'cart_flow_address_step[transportAddress][province]': '',
                'cart_flow_address_step[transportAddress][postcode]': '',
                'cart_flow_address_step[transportAddress][city]': '',
                'cart_flow_address_step[transportAddress][street]': '',
                'cart_flow_address_step[transportAddress][houseNumber]': '',
                'cart_flow_address_step[transportAddress][apartmentNumber]': '',
                'cart_flow_address_step[sameBillingAddress]': '1',
                'cart_flow_address_step[billingAddress][firstName]': '',
                'cart_flow_address_step[billingAddress][lastName]': '',
                'cart_flow_address_step[billingAddress][addressType]': 'person',
                'cart_flow_address_step[billingAddress][company]': '',
                'cart_flow_address_step[billingAddress][nip]': '',
                'cart_flow_address_step[billingAddress][phone]': '',
                'cart_flow_address_step[billingAddress][postcode]': '',
                'cart_flow_address_step[billingAddress][city]': '',
                'cart_flow_address_step[billingAddress][street]': '',
                'cart_flow_address_step[billingAddress][houseNumber]': '',
                'cart_flow_address_step[billingAddress][apartmentNumber]': '',
                'cart_flow_address_step[transportAddress][addressType]': 'person',
                'cart_flow_address_step[billingAddress][province]': '',
                'cart_flow_address_step[customerComment]': '',
                'cart_flow_address_step[_token]': cart_token
            }

        if self.germany_region:
            if "Einschreiben" in response.body:
                data = {
                    'cart_flow_address_step[accountAddress][firstName]': fn,
                    'cart_flow_address_step[accountAddress][lastName]': ln,
                    'cart_flow_address_step[accountAddress][email]': email,
                    'cart_flow_address_step[accountAddress][addressType]': 'person',
                    'cart_flow_address_step[accountAddress][company]': '',
                    'cart_flow_address_step[accountAddress][nip]': '',
                    'cart_flow_address_step[accountAddress][phone]': phone,
                    'cart_flow_address_step[accountAddress][street]': addy,
                    'cart_flow_address_step[accountAddress][houseNumber]': house_number,
                    'cart_flow_address_step[accountAddress][apartmentNumber]': province_id,
                    'cart_flow_address_step[accountAddress][postcode]': zip,
                    'cart_flow_address_step[accountAddress][city]': city,
                    'cart_flow_address_step[sameTransportAddress]': '1',
                    'cart_flow_address_step[transportAddress][company]': '',
                    'cart_flow_address_step[transportAddress][firstName]': '',
                    'cart_flow_address_step[transportAddress][lastName]': '',
                    'cart_flow_address_step[transportAddress][phone]': '',
                    'cart_flow_address_step[transportAddress][street]': '',
                    'cart_flow_address_step[transportAddress][houseNumber]': '',
                    'cart_flow_address_step[transportAddress][apartmentNumber]': '',
                    'cart_flow_address_step[transportAddress][postcode]': '',
                    'cart_flow_address_step[transportAddress][city]': '',
                    'cart_flow_address_step[sameBillingAddress]': '1',
                    'cart_flow_address_step[billingAddress][firstName]': '',
                    'cart_flow_address_step[billingAddress][lastName]': '',
                    'cart_flow_address_step[billingAddress][addressType]': 'person',
                    'cart_flow_address_step[billingAddress][company]': '',
                    'cart_flow_address_step[billingAddress][nip]': '',
                    'cart_flow_address_step[billingAddress][phone]': '',
                    'cart_flow_address_step[billingAddress][street]': '',
                    'cart_flow_address_step[billingAddress][houseNumber]': '',
                    'cart_flow_address_step[billingAddress][apartmentNumber]': '',
                    'cart_flow_address_step[billingAddress][postcode]': '',
                    'cart_flow_address_step[billingAddress][city]': '',
                    'cart_flow_address_step[consentForm][consent_2178][]': '2178',
                    'cart_flow_address_step[transportAddress][addressType]': 'person',
                    'cart_flow_address_step[customerComment]': '',
                    'cart_flow_address_step[_token]': cart_token,
                }
            else:
                data = {
                    'cart_flow_address_step[accountAddress][firstName]': fn,
                    'cart_flow_address_step[accountAddress][lastName]': ln,
                    'cart_flow_address_step[accountAddress][email]': email,
                    'cart_flow_address_step[accountAddress][addressType]': 'person',
                    'cart_flow_address_step[accountAddress][company]': '',
                    'cart_flow_address_step[accountAddress][nip]': '',
                    'cart_flow_address_step[accountAddress][phone]': phone,
                    'cart_flow_address_step[accountAddress][street]': addy,
                    'cart_flow_address_step[accountAddress][houseNumber]': house_number,
                    'cart_flow_address_step[accountAddress][apartmentNumber]': province_id,
                    'cart_flow_address_step[accountAddress][postcode]': zip,
                    'cart_flow_address_step[accountAddress][city]': city,
                    'cart_flow_address_step[sameTransportAddress]': '1',
                    'cart_flow_address_step[transportAddress][company]': '',
                    'cart_flow_address_step[transportAddress][firstName]': '',
                    'cart_flow_address_step[transportAddress][lastName]': '',
                    'cart_flow_address_step[transportAddress][phone]': '',
                    'cart_flow_address_step[transportAddress][street]': '',
                    'cart_flow_address_step[transportAddress][houseNumber]': '',
                    'cart_flow_address_step[transportAddress][apartmentNumber]': '',
                    'cart_flow_address_step[transportAddress][postcode]': '',
                    'cart_flow_address_step[transportAddress][city]': '',
                    'cart_flow_address_step[sameBillingAddress]': '1',
                    'cart_flow_address_step[billingAddress][firstName]': '',
                    'cart_flow_address_step[billingAddress][lastName]': '',
                    'cart_flow_address_step[billingAddress][addressType]': 'person',
                    'cart_flow_address_step[billingAddress][company]': '',
                    'cart_flow_address_step[billingAddress][nip]': '',
                    'cart_flow_address_step[billingAddress][phone]': '',
                    'cart_flow_address_step[billingAddress][street]': '',
                    'cart_flow_address_step[billingAddress][houseNumber]': '',
                    'cart_flow_address_step[billingAddress][apartmentNumber]': '',
                    'cart_flow_address_step[billingAddress][postcode]': '',
                    'cart_flow_address_step[billingAddress][city]': '',
                    'checkall': 'on',
                    'cart_flow_address_step[consentForm][consent_2180][]': '2180',
                    'cart_flow_address_step[consentForm][consent_2190][]': '2190',
                    'cart_flow_address_step[consentForm][consent_2188][]': '2188',
                    'cart_flow_address_step[consentForm][consent_2178][]': '2178',
                    'cart_flow_address_step[transportAddress][addressType]': 'person',
                    'cart_flow_address_step[customerComment]': '',
                    'cart_flow_address_step[_token]': cart_token,
                }

        adata = json.dumps(data)
        content_length = len(str(adata).replace('"', '').replace(" ", '')) - 2

        headers = [
            ['method', 'POST'],
            ['authority', self.authority],
            ['scheme', 'https'],
            ['cache-control', 'no-cache'],
            ['upgrade-insecure-requests', '1'],
            ['origin', self.home_page],
            ['content-length', str(content_length)],
            ['content-type', 'application/x-www-form-urlencoded'],
            ['user-agent', str(user_agent)],
            ['accept',
             'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'],
            ['sec-gpc', '1'],
            ['sec-fetch-site', 'same-origin'],
            ['sec-fetch-mode', 'navigate'],
            ['sec-fetch-user', '?1'],
            ['sec-fetch-dest', 'document'],
            ['referer', get_shipping_url],
            ['accept-encoding', 'gzip, deflate, br'],
            ['accept-language', 'en-US,en;q=0.9'],
            ['cookie', '']
        ]

        return headers, data

    def check_response(self, task_number, response, step):
        """A function used in order to check wether the response is empty or not"""
        if response.status == 403:
            logs = f'Forbidden {step} [403]. Resetting Session...'
            self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

            self.has_failed_needs_restarting[task_number] = True

            return False

        return response

    def after_tasks_end_disable_dunks_accounts(self, task_number):
        """
        Possibly within the most important functions.

        ~it disables the accounts after they've been used
        ~if a task failed to do preload it will continue without changing the accounts availability

        """
        # If we have a dunk, we will check some conditions for it in order to disable accounts usage
        if self.is_dunk:
            profiles_number = task_number % (self.number_of_profiles)
            email = self.profiles_by_task_number[profiles_number]['EMAIL']

            JsonClass().update_each_account_general_information(self.disabled_accounts_list_json[task_number])

            if not self.preload_mode[task_number]:
                self.entered_dead_zone[email] = False

    def after_tasks_end_check_if_checked_out(self, task_number):
        """
        Possibly within the most important functions.

        ~it checks to see wether the bot has succesfully checked out
        ~if it did checkout, we check to see if we haven't checked out more than the amount of times specified
        ~if we are in preload we don't continue with the checkout flow
        """
        # Once we've passed the dunks conditions, we check wether the task has succesfully checked out or not
        if self.has_succesfully_checked_out[task_number]:
            try:
                if self.continue_script[task_number]:
                    if self.number_of_checkouts < self.max_checkouts:
                        return True

                    else:
                        logs = f"REACHED MAX CHECKOUTS."
                        self.tools.print_logs(logs, self.store_name, Fore.LIGHTMAGENTA_EX, task_number)
                        return False
            except:
                return False

    def limit_tasks_to_one_discount(self, task_number, email, uncaching_discount_task):
        """
        Function used in order to check which account has had the coupon activated

        Used right after adding to cart
        """
        if uncaching_discount_task:
            activated_account = self.apply_discount(task_number, email, uncaching_discount_task=uncaching_discount_task)
            if not activated_account:
                return False

        if self.is_dunk:
            try:
                if not self.activated_discount[email]:
                    activated_account = self.apply_discount(task_number, email)

                    if not activated_account:
                        return False

                    self.activated_discount[email] = True

            except:
                activated_account = self.apply_discount(task_number, email)

                if not activated_account:
                    return False

                self.activated_discount[email] = True

        return True

    def announce_enp_error(self, task_number):
        """Function used in order to announce the fact that 1 size has gone out of stock"""
        self.enp_cart_error = True
        if self.chosen_size_dict[str(task_number)] not in self.sold_out_sizes:
            self.sold_out_sizes.append(self.chosen_size_dict[str(task_number)])

    def return_profile(self, task_number):
        """Function used in order to return profiles from the csv based on the task_number"""
        profile_number = task_number % (self.number_of_profiles)

        email = self.profiles_by_task_number[profile_number]['EMAIL']
        fn = self.profiles_by_task_number[profile_number]['FIRST NAME']
        ln = self.profiles_by_task_number[profile_number]['LAST NAME']
        addy = self.profiles_by_task_number[profile_number]['ADDRESS LINE 1']
        house_number = self.profiles_by_task_number[profile_number]['HOUSE NUMBER']
        city = self.profiles_by_task_number[profile_number]['CITY']
        zip = self.profiles_by_task_number[profile_number]['POSTCODE/ZIP']
        phone = self.profiles_by_task_number[profile_number]['PHONE']
        province_id = self.profiles_by_task_number[profile_number]['PROVINCE ID']

        new_phone = ''
        iterator = 1
        for number in phone:
            if iterator % 10 == 4 or iterator % 10 == 7:
                new_phone += number
                new_phone += ' '
            else:
                new_phone += number
            iterator += 1

        return email, fn, ln, addy, house_number, city, zip, phone, province_id, new_phone

    def filter_sizes(self, size):
        """

        Function used in order to filter each sizes and see if it matches my criteria

        We have multiple cases:
                    1. `36 - 48`: It selects each size that happens to be between that interval
                    extra: `36 - 48; ~36.5, ~39, ~40`: The sizes that are mentioned with ~ will be ignored
                    2. `36.5, 37.5, 40.5, 45`: The sizes that are being looked up are the ones specified
                    3. `~36.5, ~38`: The bot picks every size except the ones specified

        """
        # We replace the size ',' with a '.' so we can convert it to float numbers
        size = size.replace(',', '.')

        try:
            # case 1
            if '-' in self.selected_sizes:
                return self.filter_first_case_sizes(size)
            # case 3
            elif '~' in self.selected_sizes:
                return self.filter_third_case_sizes(size)
            # case 2
            else:
                return self.filter_second_case_sizes(size)
        except:
            return True

    def filter_first_case_sizes(self, size):
        """

        We happen to be in the first case

        `36 - 48`: It selects each size that happens to be between that interval
        extra: `36 - 48; ~36.5, ~39, ~40`: The sizes that are mentioned with ~ will be ignored

        """
        exception_list = []
        min_max_size_list = self.selected_sizes.split('-')
        min_size = float(min_max_size_list[0].strip())
        max_size = float(min_max_size_list[1].split(';')[0].strip())

        if '~' in self.selected_sizes:
            # It means we must be carefull at what sizes we pick
            exception_sizes_list = self.selected_sizes.split(';')[1].split(',')

            for exception_size in exception_sizes_list:
                exception_size = exception_size.strip()

                # ~36.5 so we remove the ~
                exception_list.append(float(exception_size[1:]))

        if float(size) <= max_size and float(size) >= min_size and float(size) not in exception_list:
            return True

        return False

    def filter_second_case_sizes(self, size):
        """
        Means we are on the second case

        `36.5, 37.5, 40.5, 45`: The sizes that are being looked up are the ones specified

        """
        float_size = float(size)
        good_list = []
        good_sizes_list = self.selected_sizes.split(',')

        for good_size in good_sizes_list:
            good_size = good_size.strip()
            good_list.append(float(good_size))

        if float_size in good_list:
            return True

        return False

    def filter_third_case_sizes(self, size):
        """
        Means we are on the third case

        `~36.5, ~38`: The bot picks every size except the ones specified

        """
        float_size = float(size)
        exception_list = []
        exception_sizes_list = self.selected_sizes.split(',')

        for exception_size in exception_sizes_list:
            exception_size = exception_size.strip()

            # ~36.5 so we remove the ~
            exception_list.append(float(exception_size[1:]))

        if float_size not in exception_list:
            return True

        return False

    def get_cart_page(self, task_number, client, user_agent, shipping_url, cart_url):
        """

        Used when Cart Page needs to be accessed.

        Returns:
            client
            response
            continue_loop: True or False
            break_loop: True or False
        """
        headers = [
            ['method', 'GET'],
            ['authority', self.authority],
            ['scheme', 'https'],
            ['cache-control', 'max-age=0'],
            ['upgrade-insecure-requests', '1'],
            ['user-agent', str(user_agent)],
            ['accept',
             'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'],
            ['sec-fetch-site', 'same-origin'],
            ['sec-fetch-mode', 'navigate'],
            ['sec-fetch-user', '?1'],
            ['sec-fetch-dest', 'document'],
            ['sec-ch-ua-mobile', '?0'],
            ['referer', shipping_url],
            ['accept-encoding', 'gzip, deflate, br'],
            ['accept-language', 'en-US,en;q=0.9'],
            ['cookie', '']
        ]

        try:
            # GET Request
            response = client.makeRequest(cart_url, {
                "method": "GET",
                "headers": headers
            })
        except:
            logs = f"Error Getting Cart Token. [TIMED OUT]"
            self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

            continue_module = self.count_error(task_number)
            if not continue_module:
                return client, False, False, True

            return client, False, True, False

        return client, response, False, False

    def check_if_discount_applied_last_step(self, client, user_agent, task_number, response, email):
        """Function used in order to check if the discount has been applied before checking out"""
        if self.is_dunk:
            if self.discounted_price[task_number] not in response.body:
                logs = f"Discount Price not applied!"
                self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

                self.activated_discount[email] = False
                continue_module = self.count_error(task_number)
                if not continue_module:
                    return False

                discounted_succesfully = self.check_discounted(client, user_agent, task_number)
                if discounted_succesfully:
                    self.activated_discount[email] = True
                    return True

                self.has_failed_needs_restarting[task_number] = True

                return False

        return True

    def uncache_discount_coupon(self, client, user_agent, task_number, email):
        """
        Function used in order to make the coupon work and uncache de discount price.

        If we use this function, means that the coupons have bugged out.
        """
        try:
            self.uncached_succesfully[task_number] = False
            self.failed_uncaching[task_number] = False
            iterator = 0
            max_retries = 50
            dummy_link = BotTools().get_dummy_link()

            logs = 'Debugging price...'
            self.tools.print_logs(logs, self.store_name, Fore.LIGHTMAGENTA_EX, task_number)

            self.start_tasks_threading(task_number, product_link=dummy_link, uncache_discount_task=True)

            # We are waiting for the tasks to give back a result wether it was succesfull or not
            while not self.uncached_succesfully[task_number]:
                if self.failed_uncaching[task_number] or iterator > max_retries:
                    return False

                iterator += 1
                sleep(1)

            logs = 'Checking cart price...'
            self.tools.print_logs(logs, self.store_name, Fore.LIGHTMAGENTA_EX, task_number)

            # We reactivate our initial coupon
            coupon_activated = self.apply_discount(task_number, email)
            if not coupon_activated:
                return False

            # We check if the discount works now
            succesfully_discounted = self.check_discounted(client, user_agent, task_number)
            if not succesfully_discounted:
                return False

            return True

        except:
            traceback.print_exc()

            return False

    def send_webhook_dunks(self, task_number, response, email):
        """Webhook used in order to send the webhook for dunks"""
        region = 'RO'

        if response.url == 'https://sizeer.ro/cos/sumar/salva':
            logs = f"Successfully Placed Order! Coupon Preserved!"
            self.tools.print_logs(logs, self.store_name, Fore.LIGHTGREEN_EX, task_number)

            checkout_message = f'[{region}] Successful Checkout! :white_check_mark:'

            # Play the checkout sound
            threading.Thread(target=self.succesfull_checkout, args=[]).start()

            # We +1 the number of checkouts
            self.number_of_checkouts += 1

            # We reset the number of retries
            self.max_retries[task_number] = 0

            checkout_time = int(time() - self.start_time_dict[str(task_number)])
            BotTools().send_webhook(checkout_message, self.prod_image[task_number], self.product_link[task_number],
                                    self.prod_title[task_number],
                                    self.discounted_price[task_number], self.chosen_size_dict[str(task_number)],
                                    self.prod_sku[task_number],
                                    self.payment_method, self.task_mode[task_number], task_number, checkout_time,
                                    order_number="undefined", number_of_fails=self.max_retries[task_number],
                                    premature_cookie_bool=self.prepare_session_early[task_number],
                                    email=self.email[task_number])

            return True, True

        elif response.url == 'https://sizeer.ro/cos/lista' and not self.second_try_placing_order[task_number]:
            logs = f"Out Of Stock While Placing Order..."
            self.tools.print_logs(logs, self.store_name, Fore.LIGHTMAGENTA_EX, task_number)

            self.announce_enp_error(task_number)
            checkout_message = f'[{region}] Out Of Stock While Placing Order :confounded:'
            checkout_time = int(time() - self.start_time_dict[str(task_number)])
            BotTools().send_webhook(checkout_message, self.prod_image[task_number], self.product_link[task_number],
                                    self.prod_title[task_number],
                                    self.discounted_price[task_number], self.chosen_size_dict[str(task_number)],
                                    self.prod_sku[task_number],
                                    self.payment_method, self.task_mode[task_number], task_number, checkout_time,
                                    order_number="undefined", number_of_fails=self.max_retries[task_number],
                                    premature_cookie_bool=self.prepare_session_early[task_number],
                                    email=self.email[task_number])

            return False, False

        else:
            if str(response.url) == 'https://sizeer.ro/cos/confirmare':
                logs = f"Successfully Checked Out! Coupon Used!"
                self.tools.print_logs(logs, self.store_name, Fore.LIGHTGREEN_EX, task_number)

                checkout_message = f'[{region}] [Coupon Used] Successful Checkout! :white_check_mark:'
                checkout_time = int(time() - self.start_time_dict[str(task_number)])

                # We +1 the number of checkouts
                self.number_of_checkouts += 1

                # Play the checkout sound
                threading.Thread(target=self.succesfull_checkout, args=[]).start()
                order_nr = self.get_order_number_ro(response.body)

                # We reset the number of retries
                self.max_retries[task_number] = 0

                dunk_category = self.dunk_coupon_name[task_number]
                self.accounts_list_json[task_number]["coupons"][dunk_category] = False

                BotTools().send_webhook(checkout_message, self.prod_image[task_number], self.product_link[task_number],
                                        self.prod_title[task_number],
                                        self.discounted_price[task_number], self.chosen_size_dict[str(task_number)],
                                        self.prod_sku[task_number],
                                        self.payment_method, self.task_mode[task_number], task_number, checkout_time,
                                        order_number=order_nr, number_of_fails=self.max_retries[task_number],
                                        premature_cookie_bool=self.prepare_session_early[task_number],
                                        email=self.email[task_number])

                return True, False
            else:
                logs = f"Unknown response while Placing Order. Check account..."
                self.tools.print_logs(logs, self.store_name, Fore.LIGHTBLUE_EX, task_number)

                self.write_response_body(response)
                checkout_message = f'[{region}] Check account to see if the order has been logged. :frowning:'
                checkout_time = int(time() - self.start_time_dict[str(task_number)])
                # We +1 the number of checkouts
                self.number_of_checkouts += 1

                # We reset the number of retries
                self.max_retries[task_number] = 0

                # Attaching the link + the email to easily recognise the tasks
                order_number_text = f"{response.url}"

                BotTools().send_webhook(checkout_message, self.prod_image[task_number], self.product_link[task_number],
                                        self.prod_title[task_number],
                                        self.discounted_price[task_number], self.chosen_size_dict[str(task_number)],
                                        self.prod_sku[task_number],
                                        self.payment_method, self.task_mode[task_number], task_number, checkout_time,
                                        order_number=order_number_text, number_of_fails=self.max_retries[task_number],
                                        premature_cookie_bool=self.prepare_session_early[task_number],
                                        email=self.email[task_number])

                return False, True

    def send_webhook_guest(self, task_number, response, email):
        """Function used in order to send the webhooks in case the bot is in normal mode"""
        conf_page = 'https://sizeer.ro/cos/confirmare'
        region = 'RO'

        if self.germany_region:
            conf_page = 'https://sizeer.de/warenkorb/bestatigung'
            region = "DE"

        if response.url == conf_page:
            logs = f"Successfully Placed Order!"
            self.tools.print_logs(logs, self.store_name, Fore.LIGHTGREEN_EX, task_number)

            checkout_message = f'[{region}] Successful Checkout! :white_check_mark:'
            checkout_time = int(time() - self.start_time_dict[str(task_number)])
            order_nr = email

            # Retrieving the order number in case we are in germany
            if self.germany_region:
                order_nr = str(self.get_order_number(response.body))
            else:
                order_nr = str(self.get_order_number_ro(response.body))

            # Play the checkout sound
            threading.Thread(target=self.succesfull_checkout, args=[]).start()

            # We +1 the number of checkouts
            self.number_of_checkouts += 1

            # We reset the number of retries
            self.max_retries[task_number] = 0

            BotTools().send_webhook(checkout_message, self.prod_image[task_number],
                                    self.product_link[task_number],
                                    self.prod_title[task_number],
                                    self.discounted_price[task_number], self.chosen_size_dict[str(task_number)],
                                    self.prod_sku[task_number],
                                    self.payment_method, self.task_mode[task_number], task_number, checkout_time,
                                    order_number=order_nr, number_of_fails=self.max_retries[task_number],
                                    premature_cookie_bool=self.prepare_session_early[task_number],
                                    email=self.email[task_number])

        else:
            if response.url == 'https://sizeer.ro/cos/lista' and \
                    not self.second_try_placing_order[task_number] or \
                    response.url == 'https://sizeer.de/warenkorb/liste' and \
                    not self.second_try_placing_order[task_number]:

                logs = f"Out Of Stock While Placing Order..."
                self.tools.print_logs(logs, self.store_name, Fore.LIGHTMAGENTA_EX, task_number)

                self.announce_enp_error(task_number)
                checkout_message = f'[{region}] OOS While Placing Order :confounded:'
                checkout_time = int(time() - self.start_time_dict[str(task_number)])
                BotTools().send_webhook(checkout_message, self.prod_image[task_number],
                                        self.product_link[task_number],
                                        self.prod_title[task_number],
                                        self.discounted_price[task_number], self.chosen_size_dict[str(task_number)],
                                        self.prod_sku[task_number],
                                        self.payment_method, self.task_mode[task_number], task_number, checkout_time,
                                        order_number="undefined", number_of_fails=self.max_retries[task_number],
                                        premature_cookie_bool=self.prepare_session_early[task_number],
                                        email=self.email[task_number])
            else:
                logs = f"Unknown response while Placing Order. Check account..."
                self.tools.print_logs(logs, self.store_name, Fore.LIGHTBLUE_EX, task_number)
                checkout_message = f'[{region}] Check account to see if the order has been logged. :frowning:'

                self.write_response_body(response)
                checkout_time = int(time() - self.start_time_dict[str(task_number)])
                # We +1 the number of checkouts
                self.number_of_checkouts += 1

                # We reset the number of retries
                self.max_retries[task_number] = 0

                # Attaching the link + the email to easily recognise the tasks
                order_number_text = f"{response.url}"

                BotTools().send_webhook(checkout_message, self.prod_image[task_number],
                                        self.product_link[task_number],
                                        self.prod_title[task_number],
                                        self.discounted_price[task_number], self.chosen_size_dict[str(task_number)],
                                        self.prod_sku[task_number],
                                        self.payment_method, self.task_mode[task_number], task_number, checkout_time,
                                        order_number=order_number_text, number_of_fails=self.max_retries[task_number],
                                        premature_cookie_bool=self.prepare_session_early[task_number],
                                        email=self.email[task_number])

    def kill_task(self, task_number, step=''):
        """A function used in order to set variables accross files and folders before closing"""

        if step == "Just Disable":
            if self.is_dunk:
                JsonClass().update_each_account_general_information(self.disabled_accounts_list_json[task_number])

        elif step == "Manifest Step":
            if self.is_dunk:
                JsonClass().update_each_account_general_information(self.disabled_accounts_list_json[task_number])

        return False

    def change_coupon(self, task_number, email, password, from_monitor):
        """Function used in order to remove the used coupon from the available coupon's list"""
        if self.is_dunk:
            already_prelucrated = True
            if not self.coupon_preserved[task_number]:
                JsonClass().update_each_account_general_information(
                    self.disabled_accounts_list_json[task_number])

                acc_dict = {
                    "email": email,
                    "password": password
                }

                avail_accs = JsonClass().remove_account_from_category_class(self.task_category, acc_dict)
                self.accounts_used.remove(acc_dict)
                new_acc_dict = self.load_another_avail_acc(avail_accs)
                self.number_of_profiles -= 1

                if not new_acc_dict:
                    logs = f"No accounts left."
                    self.tools.print_logs(logs, self.store_name, Fore.LIGHTRED_EX, task_number)

                    return

                email = new_acc_dict["email"]
                password = new_acc_dict["password"]

                self.profiles_by_task_number[task_number]["EMAIL"] = email
                self.profiles_by_task_number[task_number]["PASSWORD"] = password
                already_prelucrated = False

                threading.Thread(target=self.login_app_client,
                                 args=[task_number, email, password]).start()

            # We update the clients account_list_json dict by the new email
            self.prelucrate_profiles(task_number, from_monitor,
                                     create_preloaded=False,
                                     uncache_discount_task=False,
                                     already_prelucrated=already_prelucrated)

    # -------------------------------------------------

    # -----------------PRELOAD MODE-----------------
    def sleep_and_refresh_preloaded(self, client, user_agent, task_number):
        """

        Checking each 25-28 minutes to see if the account is still logged in or not.

        """
        logs = f"Task Successfully Preloaded!"
        self.tools.print_logs(logs, self.store_name, Fore.LIGHTGREEN_EX, task_number)

        self.client[task_number] = client
        times = 1

        while not self.found_item:
            # random_sleeping_interval = random.randint(10, 15) * 60
            random_sleeping_interval = random.randint(3, 5)
            sleep(random_sleeping_interval)

            url = ""
            if times % 20 == 0:
                url = "https://sizeer.ro/profil"
                if self.germany_region:
                    url = "https://sizeer.de/profil"

            client, logged_in = self.check_if_still_logged_in(client, user_agent, task_number, url)
            self.client[task_number] = client

            times += 1
            if not logged_in:
                self.lost_session[task_number] = True
                return

    def check_if_still_logged_in(self, client, user_agent, task_number, url):
        """Function that check from period to period if the client is still loged in or not"""
        while True:
            extra_log = ""
            if url:
                extra_log = "[profile]"

            logs = f"Refreshing session... {extra_log}"
            self.tools.print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX, task_number)

            headers = [
                ['method', 'GET'],
                ['authority', self.authority],
                ['scheme', 'https'],
                ['cache-control', 'max-age=0'],
                ['upgrade-insecure-requests', '1'],
                ['user-agent', str(user_agent)],
                ['accept',
                 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'],
                ['sec-gpc', '1'],
                ['origin', self.home_page],
                ['sec-fetch-site', 'same-origin'],
                ['sec-fetch-mode', 'navigate'],
                ['sec-fetch-user', '?1'],
                ['sec-fetch-dest', 'document'],
                ['accept-encoding', 'gzip, deflate, br'],
                ['accept-language', 'en-US,en;q=0.9'],
                ['cookie', '']
            ]

            if not url:
                manifest = 'https://sizeer.ro/manifest.json'
                if self.germany_region:
                    manifest = 'https://sizeer.de/manifest.json'

                randomized_link = self.randomize_link(task_number, manifest)
            else:
                randomized_link = url

            try:
                # GET Request
                response = client.makeRequest(randomized_link, {
                    "method": "GET",
                    "headers": headers
                })
            except:
                logs = "Error while refreshing session... [TIMED OUT]"
                self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)
                sleep(0.5)

                continue

            else:
                if int(response.status) == 200:
                    logs = "Session Successfully refreshed"
                    self.tools.print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX, task_number)

                    return client, True
                else:
                    logs = f"Unknown Redirect. Most probably lost the session... [{response.status}] [{response.url}]"
                    self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

                    print(client.cookie)
                    print(response.body)

                    return client, False

    def kill_preload_task_start_new_one(self, task_number, preload_mode, from_monitor):
        """

        Used ONLY after the task has succesfully preloaded.
        Used when the session has been lost/ the client failed to successfully checkout.

        """

        self.start_tasks_threading(task_number,
                                   has_failed=True,
                                   needs_new_cookie=self.has_failed_needs_restarting_with_new_cookie[task_number],
                                   from_monitor=from_monitor,
                                   already_prelucrated=True,
                                   create_preload=preload_mode)

    def set_found_item_variables(self, task_number):
        """
        Checking to see wether the item is a dunk, in which case we update the json file availability
        We update: max_retries[task_number], product_link[task_number]
        """
        self.max_retries[task_number] = 0
        self.preload_mode[task_number] = False

        if 'dunk' in self.preload_mode_product_link:
            self.is_dunk = True
            JsonClass().update_each_account_general_information(self.accounts_list_json[task_number])
        else:
            self.is_dunk = False

        self.product_link[task_number] = self.preload_mode_product_link
        self.real_product_link = self.preload_mode_product_link

    def empty_cart(self, client, user_agent, task_number, redirected_from_last_step=False):
        """A function used to empty cart after preloading"""
        while True:
            try:
                logs = f"Clearing Cart..."
                self.tools.print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX, task_number)

                lista = "https://sizeer.ro/cos/lista"
                if self.germany_region:
                    lista = "https://sizeer.de/warenkorb/liste"

                headers = [
                    ['method', 'GET'],
                    ['authority', self.authority],
                    ['scheme', 'https'],
                    ['cache-control', 'no-cache'],
                    ['sec-ch-ua-platform', '"Windows"'],
                    ['upgrade-insecure-requests', '1'],
                    ['user-agent', user_agent],
                    ['accept',
                     'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'],
                    ['sec-fetch-site', 'same-origin'],
                    ['sec-fetch-mode', 'navigate'],
                    ['sec-fetch-user', '?1'],
                    ['sec-fetch-dest', 'document'],
                    ['accept-encoding', 'gzip, deflate, br'],
                    ['accept-language', 'en-US,en;q=0.9'],
                    ['cookie', '']
                ]

                try:
                    # GET Request
                    response = client.makeRequest(lista, {
                        "method": "GET",
                        "headers": headers
                    })
                except:
                    logs = f"Error while getting cart hash... [TIMED OUT]"
                    self.tools.print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX, task_number)

                    continue_module = self.count_error(task_number)
                    if not continue_module:
                        return False, False

                    continue

                response = self.check_response(task_number, response, step="Getting Cart")
                if not response:
                    return False, False

                soup = BeautifulSoup(response.body, 'lxml')
                cart_hash = soup.find('input', attrs={'data-qty': '1'})['data-item-hash']

                data = {
                    'hash': cart_hash
                }

                adata = json.dumps(data)
                content_length = len(str(adata).replace('"', '').replace(" ", '')) - 2

                headers = [
                    ['method', 'POST'],
                    ['authority', self.authority],
                    ['scheme', 'https'],
                    ['cache-control', 'no-cache'],
                    ['accept', 'application/json, text/javascript, */*; q=0.01'],
                    ['content-length', str(content_length)],
                    ['content-type', 'application/x-www-form-urlencoded; charset=UTF-8'],
                    ['x-requested-with', 'XMLHttpRequest'],
                    ['sec-ch-ua-mobile', '?0'],
                    ['user-agent', user_agent],
                    ['sec-ch-ua-platform', '"Windows"'],
                    ['origin', self.home_page],
                    ['sec-fetch-site', 'same-origin'],
                    ['sec-fetch-mode', 'cors'],
                    ['sec-fetch-dest', 'empty'],
                    ['referer', lista],
                    ['accept-encoding', 'gzip, deflate, br'],
                    ['accept-language', 'en-US,en;q=0.9'],
                    ['cookie', ''],
                ]

                del_cart_link = "https://sizeer.ro/koszyk/list-item/del"
                if self.germany_region:
                    del_cart_link = "https://sizeer.de/koszyk/list-item/del"

                try:
                    # POST Request
                    response = client.makeRequest(del_cart_link, {
                        "method": "POST",
                        "headers": headers,
                        "applicationData": data
                    })
                except:
                    logs = f"Error while clearing cart [TIMED OUT]"
                    self.tools.print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX, task_number)

                    continue_module = self.count_error(task_number)
                    if not continue_module:
                        return False, False

                    continue
                else:
                    response = self.check_response(task_number, response, step="Clearing Cart")
                    if not response:
                        return False, False

                    if '"success":true' in response.body:
                        logs = f"Cart Cleared!"
                        self.tools.print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX, task_number)

                        return client, True
                    else:
                        logs = f"Error Clearing Cart... [UNKNOWN RESPONSE] {response.body}"
                        self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

                        continue_module = self.count_error(task_number)
                        if not continue_module:
                            return False, False

                        continue
            except:
                if redirected_from_last_step:
                    logs = f"Cart already empty..."
                    self.tools.print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX, task_number)
                    return client, True

                logs = f"Error Clearing Cart... [INDEX ERROR]"
                self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)
                traceback.print_exc()

                continue_module = self.count_error(task_number)
                if not continue_module:
                    break

    # ----------------------------------------------

    # -----------USEFULL FUNCTIONS-----------
    def succesfull_checkout(self):
        """Play the checkout sound"""
        playsound.playsound(f"{cur_path}\Tools\succes.mp3")

    def write_response_body(self, response):
        """Write in a txt File, the Response.Body"""
        filename = f"{path_for_tools}\\weird_response.txt"
        with open(filename, 'a', encoding='utf-8') as f:
            f.write("\n\n\n\n\n\n")
            f.write(str(response.body))

    def deactivate_coupon_before_checkout(self, task_number):
        """A function used in order to deactivate the coupon before checking out"""
        sleep(0.3)
        try:
            self.dunk_coupon_id[task_number]

        except:
            # In case these haven't been set for some weird reason, we set them
            prod_price = self.product_price[task_number]
            price_dict = {
                '1039': 'Dunk High Adults',
                '989': 'Dunk Low Adults',
                '879': 'Dunk Low Kids',

            }
            dunk_info = price_dict[str(prod_price)]
            self.dunk_coupon_id[task_number] = self.accounts_list_json[task_number]["coupons"][dunk_info]
            self.dunk_coupon_name[task_number] = dunk_info

        logs = f"Deactivating Coupon Before Logging Order..."
        self.tools.print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX, task_number)

        success_action = self.mobile.deactivate_coupon_dunks(self.mobile_client[task_number],
                                                             self.app_access_token[task_number],
                                                             self.app_unique_id[task_number],
                                                             self.dunk_coupon_id[task_number],
                                                             self.dunk_coupon_name[task_number],
                                                             task_number)

        if success_action:
            self.activated_discount[self.email[task_number]] = False

        return success_action

    def apply_discount(self, task_number, email, checked_out=False, uncaching_discount_task=False):
        """Prelucrating the data to see what type of dunks we have"""
        if not checked_out:
            logs = f"Applying discount to the account ~ {email}..."
            self.tools.print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX, task_number)

        else:
            logs = f"Reactivating discount for the account..."
            self.tools.print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX, task_number)

        if uncaching_discount_task:
            # If we are uncaching the coupon, we are doing on a random product
            dunk_info = 'Uncaching coupon'

        else:
            prod_price = self.product_price[task_number]
            price_dict = {
                '1039': 'Dunk High Adults',
                '989': 'Dunk Low Adults',
                '879': 'Dunk Low Kids',
            }

            dunk_info = price_dict[str(prod_price)]

        self.dunk_coupon_id[task_number] = self.accounts_list_json[task_number]["coupons"][dunk_info]
        self.dunk_coupon_name[task_number] = dunk_info

        # Checking to see wether the email has entered or not deadzone
        profile_increment = task_number % (self.number_of_profiles)
        email = self.profiles_by_task_number[profile_increment]['EMAIL']
        while True:
            try:
                if not self.entered_dead_zone[email]:
                    break
                else:
                    sleep(0.5)
                    continue
            except:
                break

        threading.Thread(target=self.check_client_logged_in,
                         args=[task_number]).start()
        retries = 0
        logged_in = False
        while retries < 1000:
            try:
                self.mobile_client[task_number]
                logged_in = True
                break
            except:
                sleep(0.1)
                retries += 1

        if not logged_in:
            logs = f"Failed to login in the app during the awaited timeframe. Killing task..."
            self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

            return False

        coupon_activated = self.mobile.activate_coupon_dunks(self.mobile_client[task_number],
                                                             self.app_access_token[task_number],
                                                             self.app_unique_id[task_number],
                                                             self.dunk_coupon_id[task_number],
                                                             self.dunk_coupon_name[task_number],
                                                             task_number)
        if checked_out:
            self.activated_discount[email] = coupon_activated

        return coupon_activated

    def prelucrate_profiles(self, task_number, from_monitor, create_preloaded,
                            uncache_discount_task, already_prelucrated):
        while True:
            # If we have 5 profiles, we will have the rest up to 5, so we need +1 to the number of profiles
            # So we guide using the rest of the division.
            profiles_number = task_number % self.number_of_profiles

            email = self.profiles_by_task_number[profiles_number]['EMAIL']
            password = self.profiles_by_task_number[profiles_number]['PASSWORD']
            self.email[task_number] = email
            self.password[task_number] = password

            if uncache_discount_task or already_prelucrated or not self.is_dunk:
                return email, password

            # if not has_failed or not second_attempt:
            try:
                # Currently not a list
                self.accounts_list_json[task_number] = JsonClass().get_accounts_info(email)
            except:
                self.accounts_list_json[task_number] = {}
                traceback.print_exc()

            try:
                self.accounts_list_json[task_number]["last_used"] = str(datetime.datetime.now())

                if not self.accounts_list_json[task_number]['in use']:
                    self.disabled_accounts_list_json[task_number] = dict(self.accounts_list_json[task_number])
                    self.accounts_list_json[task_number]['in use'] = True

                    if not create_preloaded:
                        JsonClass().update_each_account_general_information(self.accounts_list_json[task_number])

                else:
                    if from_monitor:
                        logs = f"Waiting for the account with email {email} to be available"
                        self.tools.print_logs(logs, self.store_name, Fore.WHITE, task_number)

                        sleep(5)
                        continue

                    self.disabled_accounts_list_json[task_number] = dict(self.accounts_list_json[task_number])
                    self.disabled_accounts_list_json[task_number]["in use"] = False

            except:
                traceback.print_exc()
                logs = f"Error reading the Json File. Retrying..."
                self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

                continue_module = self.count_error(task_number)
                if not continue_module:
                    return False, False

                # Otherwise we continue

            return email, password

    def check_discounted(self, client, user_agent, task_number,
                         from_monitor=False, uncaching_discount_task=False,
                         normal_product=False):
        """A function used in order to check if the product has been discounted"""
        for i in range(0, 3):
            headers = [
                ['method', 'POST'],
                ['authority', self.authority],
                ['scheme', 'https'],
                ['content-length', '0'],
                ['cache-control', 'no-cache'],
                ['accept', '*/*'],
                ['user-agent', user_agent],
                ['x-requested-with', 'XMLHttpRequest'],
                ['sec-gpc', '1'],
                ['origin', self.home_page],
                ['sec-fetch-site', 'same-origin'],
                ['sec-fetch-mode', 'cors'],
                ['sec-fetch-dest', 'empty'],
                ['referer', self.product_link[task_number]],
                ['accept-encoding', 'gzip, deflate, br'],
                ['accept-language', 'en-US,en;q=0.9'],
                ['cookie', '']
            ]

            cart_link = "https://sizeer.ro/ajax/cart/mini/display"
            if self.germany_region:
                cart_link = "https://sizeer.de/ajax/cart/mini/display"

            try:
                # POST Request
                response = client.makeRequest(cart_link, {
                    "method": "POST",
                    "headers": headers
                })
            except:
                logs = f"Error While Checking cart! [TIMED OUT]"
                self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

                continue_module = self.count_error(task_number)
                if not continue_module:
                    break

                if uncaching_discount_task:
                    if i == 2:
                        self.failed_uncaching[task_number] = True

                continue

            else:
                if normal_product:
                    return client

                if "Reducere" in response.body:
                    logs = f"Discounted price Succesfully applied!"
                    self.tools.print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX, task_number)

                    if uncaching_discount_task:
                        self.uncached_succesfully[task_number] = True

                    return True
                else:
                    logs = f"Discounted price failed to apply!"
                    self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

                    continue_module = self.count_error(task_number)
                    if not continue_module:
                        break

                    if uncaching_discount_task:
                        if i == 2:
                            self.failed_uncaching[task_number] = True

                    self.uncached_succesfully[task_number] = self.recalculate_price(client, user_agent, task_number)

                    return self.uncached_succesfully[task_number]

        return self.kill_task(task_number, step="Just Disable")

    def recalculate_price(self, client, user_agent, task_number):
        while True:
            logs = f"Recalculating price..."
            self.tools.print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX, task_number)

            headers = [
                ['method', 'POST'],
                ['authority', self.authority],
                ['scheme', 'https'],
                ['content-length', '0'],
                ['cache-control', 'no-cache'],
                ['accept', 'application/json, text/javascript, */*; q=0.01'],
                ['user-agent', user_agent],
                ['x-requested-with', 'XMLHttpRequest'],
                ['sec-gpc', '1'],
                ['origin', self.home_page],
                ['sec-fetch-site', 'same-origin'],
                ['sec-fetch-mode', 'cors'],
                ['sec-fetch-dest', 'empty'],
                ['referer', self.product_link[task_number]],
                ['accept-encoding', 'gzip, deflate, br'],
                ['accept-language', 'en-US,en;q=0.9'],
                ['cookie', ''],
            ]
            try:
                # POST Request
                response = client.makeRequest('https://sizeer.ro/cart/promotion/recalculate', {
                    "method": "POST",
                    "headers": headers
                })
                if '549' in response.body or '599' in response.body or '659' in response.body:
                    logs = f"Discounted price applied!"
                    self.tools.print_logs(logs, self.store_name, Fore.LIGHTGREEN_EX, task_number)

                    return True
                else:
                    logs = f"Price cached! Retrying to apply discount..."
                    self.tools.print_logs(logs, self.store_name, Fore.RED, task_number, task_mode="PRELOAD")

                    continue_module = self.count_error(task_number)
                    if not continue_module:
                        break

                    continue

            except:
                logs = f"Error recalculating price. [INDEX ERROR]"
                self.tools.print_logs(logs, self.store_name, Fore.RED, task_number, task_mode="PRELOAD")

                continue_module = self.count_error(task_number)
                if not continue_module:
                    break

                continue

        return self.kill_task(task_number, step="Just Disable")

    def get_starting_cookies(self, client, user_agent, task_number):
        """Starting function to be able to set the manifest cookies"""
        while True:
            if self.prepare_session_early[task_number]:
                client.clearCookies()

            headers = [
                ['method', 'GET'],
                ['authority', self.authority],
                ['scheme', 'https'],
                ['cache-control', 'no-cache'],
                ['upgrade-insecure-requests', '1'],
                ['user-agent', user_agent],
                ['accept',
                 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'],
                ['sec-gpc', '1'],
                ['sec-fetch-site', 'same-origin'],
                ['sec-fetch-mode', 'navigate'],
                ['sec-fetch-user', '?1'],
                ['sec-fetch-dest', 'document'],
                ['accept-encoding', 'gzip, deflate, br'],
                ['accept-language', 'en-US,en;q=0.9'],
                ['cookie', ''],
            ]

            manifest = 'https://sizeer.ro/manifest.json'
            if self.germany_region:
                manifest = 'https://sizeer.de/manifest.json'

            randomized_link = self.randomize_link(task_number, manifest)
            try:
                # GET Request
                response = client.makeRequest(randomized_link, {
                    "method": "GET",
                    "headers": headers
                })

            except:
                logs = f'Error setting session cookies... [TIMED OUT]'
                self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

                continue_module = self.count_error(task_number)
                if not continue_module:
                    return False

            else:

                if self.prepare_session_early[task_number]:
                    self.prepare_session_early[task_number] = False

                    logs = f"Attribuing cookie to premature session..."
                    self.tools.print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX, task_number)

                    site = "https://sizeer.ro/"
                    if self.germany_region:
                        site = "https://sizeer.de/"

                    try:
                        while not self.global_abck_cookie[task_number]:
                            sleep(0.2)

                        client.addCookie({
                            "url": site,
                            "name": "_abck",
                            "value": self.global_abck_cookie[task_number]
                        })

                    except:
                        logs = f"Failed setting Akamai Cookie to session."
                        self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)
                        traceback.print_exc()
                        return False

                return client

    # ----------------------------------------

    # ---------------CURRENTLY NOT IN USE---------------
    def get_home_page(self, client, user_agent, task_number):
        """A function used in order to get to home page"""
        while True:
            logs = "Refreshing session..."
            self.tools.print_logs(logs, self.store_name, Fore.LIGHTYELLOW_EX, task_number)

            manifest = "https://sizeer.ro/manifest.json"
            if self.germany_region:
                manifest = "https://sizeer.de/manifest.json"

            headers = [
                ['method', 'GET'],
                ['authority', self.authority],
                ['scheme', 'https'],
                ['cache-control', 'no-cache'],
                ['upgrade-insecure-requests', '1'],
                ['user-agent', str(user_agent)],
                ['accept',
                 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'],
                ['sec-gpc', '1'],
                ['sec-fetch-site', 'same-origin'],
                ['sec-fetch-mode', 'navigate'],
                ['sec-fetch-user', '?1'],
                ['sec-fetch-dest', 'document'],
                ['referer', manifest],
                ['accept-encoding', 'gzip, deflate, br'],
                ['accept-language', 'en-US,en;q=0.9'],
                ['cookie', '']
            ]

            region = "https://sizeer.ro/"
            if self.germany_region:
                region = "'https://sizeer.de/"

            try:
                response = client.makeRequest(region, {
                    "method": "GET",
                    "headers": headers
                })

            except Exception:
                logs = f"Error getting home page. [TIMED OUT]"
                self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

                sleep(0.5)
                continue
            else:
                if int(response.status) != 200:
                    logs = f"Unkown Redirect. Most probably lost the session... [{response.status}] [{response.url}]"
                    self.tools.print_logs(logs, self.store_name, Fore.RED, task_number)

                    return False

                else:
                    return client
