import requests, json, sys, colorama, uuid, os, time, traceback
from unipath import Path
from random import randint
from datetime import datetime

from colorama import Fore

colorama.init(autoreset=True)

cur_path = os.path.dirname(os.path.realpath(__file__))
cur_path = Path(cur_path).parent.parent

path_for_tools = cur_path + '\\Tools'

sys.path.append(path_for_tools)

# noinspection PyUnresolvedReferences
from bot_tools import BotTools


class SizeerMobileAPK:
    """A class used in order to deal with the Sizeer Mobile APK"""

    def __init__(self):
        self.tools = BotTools()
        self.max_retries = {}
        self.global_max_retries = 25

    def set_beggining_variables(self, task_number, max_retries=25):
        """

        A function mainly used in order to set the initial variables

        !! Should only be accessed upon calling the class

        """
        self.max_retries[task_number] = 0
        self.global_max_retries = max_retries

    def get_anonymous_token(self, task_number, filename=""):
        """A function that sets the client an anonymous token"""
        while True:
            client = BotTools().create_client(filename=filename)
            unique_id = str(uuid.uuid4())

            logs = f"Tokenizing Session..."
            self.tools.print_logs(logs, f'SIZEER', Fore.LIGHTCYAN_EX, task_number, task_mode='APP')

            headers = {
                'user-agent': 'Dart/2.10 (dart:io)',
                'synerise-uuid': unique_id,
                'platform': 'Android',
                'host': 'ro.sizeer.mcom.appchance.shop',
            }

            try:
                response = client.get('https://ro.sizeer.mcom.appchance.shop/api/users/token/anonymous/',
                                      headers=headers, timeout=10)

            except:
                logs = f"Timed Out while Tokenizing session..."
                self.tools.print_logs(logs, f'SIZEER', Fore.RED, task_number, task_mode='APP')

                continue_module = self.count_error(task_number)
                if not continue_module:
                    return False, False, False

                continue
            else:
                if int(response.status_code) == 200:
                    anonymous_token = response.json()

                    return client, anonymous_token, unique_id

                logs = f"Bad response. [{logs}] [{response.status_code}]"
                self.tools.print_logs(logs, f'SIZEER', Fore.RED, task_number, task_mode='APP')

                continue_module = self.count_error(task_number)
                if not continue_module:
                    return False, False, False

                continue

    def login(self, email, password, task_number, filename=""):
        """A function used in order to login into the app"""
        while True:
            client, anonymous_token, unique_id = self.get_anonymous_token(task_number, filename)
            if not client:
                return False, False, False

            logs = f"Logging in..."
            self.tools.print_logs(logs, f'SIZEER', Fore.LIGHTCYAN_EX, task_number, task_mode='APP')

            data, headers = self.set_login_variables(email, password, unique_id, anonymous_token)

            self.max_retries[task_number] += 1

            try:
                response = client.post('https://ro.sizeer.mcom.appchance.shop/api/users/token/',
                                       headers=headers, data=data, timeout=10)

            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError,
                    requests.exceptions.ProxyError) as err:
                logs = f"Error Logging into the APP. [TIMED OUT]"
                self.tools.print_logs(logs, f'SIZEER', Fore.RED, task_number, task_mode='APP')

                continue_module = self.count_error(task_number)
                if not continue_module:
                    return False, False, False

                continue

            except Exception:
                logs = f"Error Logging into the APP. [UNKNOWN]"
                self.tools.print_logs(logs, f'SIZEER', Fore.RED, task_number, task_mode='APP')

                continue_module = self.count_error(task_number)
                if not continue_module:
                    return False, False, False

                # traceback.print_exc()
                continue

            else:
                if "access_token" in response.text:
                    bearer_token = response.json()['access_token']

                    logs = f"Logged in the APP!"
                    self.tools.print_logs(logs, f'SIZEER', Fore.LIGHTCYAN_EX, task_number, task_mode='APP')

                    return client, bearer_token, unique_id

                elif 'nevalid' in response.text:
                    logs = f"Invalid Login Credidentials."
                    self.tools.print_logs(logs, f'SIZEER', Fore.RED, task_number, task_mode='APP')

                    return False, False, False

                else:
                    if response.status_code == 502:
                        secs = 5
                        logs = f"Site's backend fried. Waiting {secs} seconds before takin any other actions!"
                        self.tools.print_logs(logs, f'SIZEER', Fore.RED, task_number, task_mode='APP')
                        time.sleep(secs)
                        continue

                    logs = f"Unknown response while logging in the app. [{response.status_code}]"
                    self.tools.print_logs(logs, f'SIZEER', Fore.RED, task_number, task_mode='APP')

                    print(response.text)

                    continue_module = self.count_error(task_number)
                    if not continue_module:
                        return False, False, False

                    continue

    def set_login_variables(self, email, password, unique_id, anonymous_token):
        """A function used in order to set login variables like headers and data"""
        headers = {
            'user-agent': 'Dart/2.10 (dart:io)',
            'host': 'ro.sizeer.mcom.appchance.shop',
            'authorization': f'Anonymous {anonymous_token}',
            'content-type': 'application/json; charset=utf-8',
            'synerise-uuid': unique_id,
            'platform': 'Android',
        }

        data = {
            "email": email,
            "password": password
        }

        dumped_data = str(json.dumps(data))

        return dumped_data, headers

    def deactivate_active_coupons(self, client, access_token, unique_id, task_number):
        """A function used in order to deactivate the active coupons"""
        coupons_response = self.get_coupons_information(client, access_token, unique_id, task_number)
        deactivated_bool = False

        for coupon in coupons_response:
            if coupon['active'] == True:
                deactivated_bool = self.deactivate_coupon_dunks(client, access_token, unique_id, coupon['id'],
                                                                coupon['name'], task_number)

        return deactivated_bool

    def change_coupons_id(self, client, access_token, unique_id, coupon_name, activate, task_number):
        """A function used in order to change the coupons ID"""
        coupons_response = self.get_coupons_information(client, access_token, unique_id, task_number)
        changed_bool = False

        for coupon in coupons_response:
            try:
                if coupon['name'] == coupon_name:
                    if activate:
                        changed_bool = self.activate_coupon_dunks(client, access_token, unique_id, coupon['id'],
                                                                  coupon_name, task_number)
                    else:
                        changed_bool = self.deactivate_coupon_dunks(client, access_token, unique_id, coupon['id'],
                                                                    coupon_name, task_number)
            except:
                continue

        return changed_bool

    def get_coupons_information(self, client, access_token, unique_id, task_number):
        """A function used in order to get the information about the live coupons"""
        while True:
            logs = f"Retrieving Coupons Information!"
            self.tools.print_logs(logs, f'SIZEER', Fore.LIGHTCYAN_EX, task_number, task_mode='APP')

            dunks_coupons_dict = [
                {
                    "name": "Dunk Low Adults",
                    "abreviation": "NIKE DUNK LOW",
                    "price": '599',
                    "id": "SIRODUNKL500",
                    "status": False
                },
                {
                    "name": "Dunk High Adults",
                    "abreviation": "NIKE DUNK HIGH",
                    "price": '659',
                    "id": "SIRODUNKH500",
                    "status": False
                },
                {
                    "name": "Dunk High Kids",
                    "abreviation": "NIKE DUNK HIGH JUNIOR",
                    "price": '599',
                    "id": "SIRODUNKJ500",
                    "status": False
                },
                {
                    "name": "Dunk Low Kids",
                    "abreviation": "NIKE DUNK JUNIOR",
                    "price": '549',
                    "id": "SIRODUNK5",
                    "status": False
                },
                {
                    "name": "Uncaching coupon",
                    "abreviation": "Reducerea",
                    "price": "25 RON",
                    "id": "SIRO25022022",
                    "status": False
                }
            ]

            headers = {
                'user-agent': 'Dart/2.10 (dart:io)',
                'host': 'ro.sizeer.mcom.appchance.shop',
                'authorization': f'Bearer {access_token}',
                'synerise-uuid': unique_id,
                'platform': 'Android',
            }

            try:
                response = client.get('https://ro.sizeer.mcom.appchance.shop/api/pages/coupons/',
                                      headers=headers, timeout=20)

            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError,
                    requests.exceptions.ProxyError) as err:
                logs = f"Error getting coupons information. [TIMED OUT]"
                self.tools.print_logs(logs, f'SIZEER', Fore.RED, task_number, task_mode='APP')

                continue_module = self.count_error(task_number)
                if not continue_module:
                    return False

                continue

            except Exception:
                logs = f"Error getting coupons information. [UNKNOWN]"
                self.tools.print_logs(logs, f'SIZEER', Fore.RED, task_number, task_mode='APP')

                continue_module = self.count_error(task_number)
                if not continue_module:
                    return False

                continue
            else:
                if response.status_code == 200:
                    # Iterating through each coupon to see which one is active
                    iterator = 0
                    for dunk_coupon in dunks_coupons_dict:
                        for coupon in response.json():
                            # We are checking tho see wether it's the correct dunk coupon
                            coupon_name = dunk_coupon["id"]

                            if str(coupon_name) == str(coupon["code"]):
                                # We check to see wether the coupon is active or not
                                is_active = coupon['is_active']

                                dunks_coupons_dict[iterator]['status'] = True
                                dunks_coupons_dict[iterator]['active'] = is_active

                                break

                        iterator += 1

                    return dunks_coupons_dict
                else:
                    logs = f"Weird response while retrieving coupons. [{response.status_code}]"
                    self.tools.print_logs(logs, f'SIZEER', Fore.RED, task_number, task_mode='APP')

                    continue_module = self.count_error(task_number)
                    if not continue_module:
                        return False

                    continue

    def retrieve_user_points(self, client, access_token, unique_id, task_number):
        """A function used in order to fetch user's points"""
        while True:
            logs = f"Fetching points..."
            self.tools.print_logs(logs, f'SIZEER', Fore.LIGHTCYAN_EX, task_number, task_mode='APP')

            headers = {
                'user-agent': 'Dart/2.10 (dart:io)',
                'host': 'ro.sizeer.mcom.appchance.shop',
                'authorization': f'Bearer {access_token}',
                'synerise-uuid': unique_id,
                'platform': 'Android',
            }

            try:
                response = client.get('https://ro.sizeer.mcom.appchance.shop/api/users/profile/points/',
                                      headers=headers, timeout=10)

            except:
                logs = f"Timed Out Fetching points..."
                self.tools.print_logs(logs, f'SIZEER', Fore.RED, task_number, task_mode='APP')

                continue_module = self.count_error(task_number)
                if not continue_module:
                    return False

                continue

            else:
                if response.status_code == 200:
                    points = response.json()["points"]

                    return points

                else:
                    logs = f"Weird response while fetching points. [{response.status_code}]"
                    self.tools.print_logs(logs, f'SIZEER', Fore.RED, task_number, task_mode='APP')

                    continue_module = self.count_error(task_number)
                    if not continue_module:
                        return False

                    continue

    def deactivate_coupon_dunks(self, client, access_token, unique_id, coupon_id, coupon_name, task_number):
        """A function used in order to deactivate the dunks coupon"""
        while True:
            headers = {
                'user-agent': 'Dart/2.10 (dart:io)',
                'host': 'ro.sizeer.mcom.appchance.shop',
                'authorization': f'Bearer {access_token}',
                'content-type': 'application/json; charset=utf-8',
                'synerise-uuid': unique_id,
                'platform': 'Android',
            }
            string_data = '{"code":"' + str(coupon_id) + '"}'

            try:
                response = client.post('https://ro.sizeer.mcom.appchance.shop/api/pages/coupons/deactivate/',
                                       headers=headers, data=string_data, timeout=10)

            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError,
                    requests.exceptions.ProxyError) as err:
                logs = f"Error Deactivating {coupon_name} Coupon... [TIMED OUT]"
                self.tools.print_logs(logs, f'SIZEER', Fore.RED, task_number, task_mode='APP')

                continue_module = self.count_error(task_number)
                if not continue_module:
                    return False

                continue

            except Exception:
                logs = f"Error Deactivating {coupon_name} Coupon... [UNKNOWN]"
                self.tools.print_logs(logs, f'SIZEER', Fore.RED, task_number, task_mode='APP')

                # traceback.print_exc()
                continue_module = self.count_error(task_number)
                if not continue_module:
                    return False

                continue

            else:
                if 'ASSIGNED' in response.text:
                    logs = f"Deactivated {coupon_name} Coupon!"
                    self.tools.print_logs(logs, f'SIZEER', Fore.LIGHTCYAN_EX, task_number, task_mode='APP')

                    return True

                else:
                    logs = f"COULDN'T DEACTIVATE {coupon_name} Coupon!!!!"
                    self.tools.print_logs(logs, f'SIZEER', Fore.RED, task_number, task_mode='APP')

                    if 'Nu a fost' in response.text:
                        activate = False
                        succes_action = self.change_coupons_id(client, access_token, unique_id, coupon_name,
                                                               activate, task_number)
                        return succes_action

                    return False

    def activate_coupon_dunks(self, client, access_token, unique_id, coupon_id, coupon_name, task_number):
        """A function used in order to activate the coupon dunks"""
        while True:
            headers = {
                'user-agent': 'Dart/2.10 (dart:io)',
                'host': 'ro.sizeer.mcom.appchance.shop',
                'authorization': f'Bearer {access_token}',
                'content-type': 'application/json; charset=utf-8',
                'synerise-uuid': unique_id,
                'platform': 'Android',
            }
            string_data = '{"code":"' + str(coupon_id) + '"}'

            try:
                response = client.post('https://ro.sizeer.mcom.appchance.shop/api/pages/coupons/activate/',
                                       headers=headers, data=string_data, timeout=10)

            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError,
                    requests.exceptions.ProxyError) as err:
                logs = f"Error Activating {coupon_name} Coupon... [TIMED OUT]"
                self.tools.print_logs(logs, f'SIZEER', Fore.RED, task_number, task_mode='APP')

                continue_module = self.count_error(task_number)
                if not continue_module:
                    return False

                continue

            except Exception:
                logs = f"Error Activating {coupon_name} Coupon... [UNKNOWN]"
                self.tools.print_logs(logs, f'SIZEER', Fore.RED, task_number, task_mode='APP')

                # traceback.print_exc()
                continue_module = self.count_error(task_number)
                if not continue_module:
                    return False

                continue

            else:
                if 'ACTIVE' in response.text or 'already activated' in response.text:
                    logs = f"Activated {coupon_name} Coupon Sucessfully!!"
                    self.tools.print_logs(logs, f'SIZEER', Fore.LIGHTCYAN_EX, task_number, task_mode='APP')

                    return True

                else:
                    logs = f"COULDN'T ACTIVATE {coupon_name} Coupon!!!! Error: {response.json()}"
                    self.tools.print_logs(logs, f'SIZEER', Fore.RED, task_number, task_mode='APP')

                    continue_module = self.count_error(task_number)
                    if not continue_module:
                        return False

                    if 'deja un voucher activ' in response.text:
                        activated_bool = self.deactivate_active_coupons(client, access_token, unique_id, task_number)

                        continue

                    elif 'Nu a fost' in response.text:
                        activate = True
                        succes_action = self.change_coupons_id(client, access_token, unique_id, coupon_name,
                                                               activate, task_number)

                        return succes_action

                    else:
                        return False

    def count_error(self, task_number):
        """
        Function used in order to announce the system when an error has been made
        If the task has hit the maximum numbers of retrys, task is being killed by the system
        """

        self.max_retries[task_number] += 1

        if self.max_retries[task_number] >= self.global_max_retries:
            logs = f"MAXIMUM RETRIES REACHED!"
            self.tools.print_logs(logs, f'SIZEER', Fore.LIGHTRED_EX, task_number, task_mode='APP')

            return False

        return True


class NewSizeerMobileAPK_AccGen:
    """A class used in order to communicate with the new application in order to generate accounts"""

    def __init__(self):
        self.tools = BotTools()

    def get_anonymous_token(self, client, task_number, unique_id):
        """Function used in order to create the anonymous token"""
        logs = f"Tokenizing Session..."
        self.tools.print_logs(logs, f'SIZEER', Fore.LIGHTCYAN_EX, task_number, task_mode='APP')

        headers = {
            'user-agent': 'Dart/2.10 (dart:io)',
            'synerise-uuid': unique_id,
            'platform': 'Android',
            'host': 'ro.sizeer.mcom.appchance.shop',
        }

        try:
            response = client.get('https://ro.sizeer.mcom.appchance.shop/api/users/token/anonymous/',
                                  headers=headers, timeout=10)

        except:
            logs = f"Timed Out while Tokenizing session..."
            self.tools.print_logs(logs, f'SIZEER', Fore.RED, task_number, task_mode='APP')

            return False, False, False

        else:
            anonymous_token = response.json()

            headers = {
                'Host': 'api.snrapi.com',
                'api-version': '4.4',
                'application-id': 'Sizeer',
                'user-agent': 'Synerise Android SDK 3.8.8',
                'accept': 'application/json',
                'mobile-info': 'android;31;G985FXXSCEUL7;12;SM-A300FU;samsung;3.8.8',
                'content-type': 'application/json; charset=UTF-8',
            }

            data = {
                "apiKey": "",  # USE YOUR OWN API KEY
                "uuid": unique_id,
                "deviceId": ""  # USE YOUR OWN DEVICE ID
            }

            json_dumped = json.dumps(data)

            try:
                response = client.post('https://api.snrapi.com/v4/auth/login/client/anonymous',
                                       headers=headers, data=str(json_dumped))
            except:
                logs = f"Failed Fetching API..."
                self.tools.print_logs(logs, f'SIZEER', Fore.RED, task_number, task_mode='APP')

                return False, False, False

            if response.status_code == 200:
                snrapi_anonymous_token = response.json()["token"]

                return client, anonymous_token, snrapi_anonymous_token

            else:
                logs = f"Wrong response while Fetching API..."
                self.tools.print_logs(logs, f'SIZEER', Fore.RED, task_number, task_mode='APP')

                return False, False, False

    def create_new_account(self, client, anonymous_token, snrapi_anonymous_token,
                           task_number, unique_id, email, password, fn, ln):
        """Function used in order to create the account"""
        tries = 1
        api_logs = []
        task_failed = False
        while True:
            if not task_failed:
                stage = "register"
                api_logs = self.add_to_api_logs(api_logs, stage, unique_id, email)

            logs = f"Generating Account..."
            self.tools.print_logs(logs, f'SIZEER', Fore.LIGHTCYAN_EX, task_number, task_mode='APP')

            data, headers, \
            raw_data, phone_number = self.set_new_acc_variables(email, password, fn, ln,
                                                                unique_id, anonymous_token)

            try:
                response = client.post('https://ro.sizeer.mcom.appchance.shop/api/users/register/register/',
                                       headers=headers, data=data, timeout=10)

            except:
                tries += 1
                logs = f"Timed Out while creating account..."
                self.tools.print_logs(logs, f'SIZEER', Fore.RED, task_number, task_mode='APP')

                if tries <= 5:
                    continue

                else:
                    logs = f"Too many timeouts!"
                    self.tools.print_logs(logs, f'SIZEER', Fore.RED, task_number, task_mode='APP')
                    return False, False, False

            else:
                if "enabled" in response.text:
                    other_info_dict = {
                        "fn": fn,
                        "ln": ln,
                        "phone": phone_number
                    }

                    stage = "generated"
                    api_logs = self.add_to_api_logs(api_logs, stage, unique_id, email, other_info_dict=other_info_dict)

                    logs = f"Account Successfully Created! Email: {email}."
                    self.tools.print_logs(logs, f'SIZEER', Fore.LIGHTGREEN_EX, task_number, task_mode='APP')

                    client = self.update_api(api_logs, snrapi_anonymous_token, client, task_number)

                    return "success", api_logs, phone_number

                else:
                    if "de telefon valid" in response.text:
                        logs = f"Bad phone number, retrying... {raw_data['phone_number']}"
                        self.tools.print_logs(logs, f'SIZEER', Fore.RED, task_number, task_mode='APP')
                        task_failed = True

                        continue
                    elif "este ocupat" in response.text:
                        logs = f"Account already created! Email: {email}"
                        self.tools.print_logs(logs, f'SIZEER', Fore.RED, task_number, task_mode='APP')

                        return "duplicate", False, False

                    logs = f"Failed generating the account! Email: {email}."
                    self.tools.print_logs(logs, f'SIZEER', Fore.RED, task_number, task_mode='APP')

                    print(response.text)

                    return "fail", False, False

    def set_new_acc_variables(self, email, password, fn, ln, unique_id, anonymous_token):
        """Function used in order to return data and header"""
        phone_number = self.create_random_number()

        data = {
            "consent_form": {
                "ids": [
                    2679,
                    2685,
                    2687,
                    2681,
                    2683
                ]
            },
            "email": email,
            "first_name": fn,
            "last_name": ln,
            "password": password,
            "phone_number": phone_number,
        }

        headers = {
            'user-agent': 'Dart/2.10 (dart:io)',
            'host': 'ro.sizeer.mcom.appchance.shop',
            'authorization': f'Anonymous {anonymous_token}',
            'content-type': 'application/json; charset=utf-8',
            'synerise-uuid': unique_id,
            'platform': 'Android',
        }
        dumped_data = str(json.dumps(data))

        return dumped_data, headers, data, phone_number

    def create_random_number(self):
        """Function used in order to generate a random phone number"""
        phone = '7'
        increment = 0

        while increment < 8:
            random_nr = randint(0, 9)
            phone += str(random_nr)

            increment += 1

        return phone

    def login(self, client, task_number, email, password, unique_id, anonymous_token, api_logs, snrapi_anonymous_token):
        """Function used in order to Login right after creating the account"""
        while True:
            logs = f"Logging in..."
            self.tools.print_logs(logs, f'SIZEER', Fore.LIGHTCYAN_EX, task_number, task_mode='APP')

            data, headers = self.set_login_variables(email, password, unique_id, anonymous_token)

            try:
                response = client.post('https://ro.sizeer.mcom.appchance.shop/api/users/token/',
                                       headers=headers, data=data, timeout=10)
            except:
                logs = f"Error Logging in..."
                self.tools.print_logs(logs, f'SIZEER', Fore.LIGHTCYAN_EX, task_number, task_mode='APP')
                time.sleep(0.1)

                continue
            else:
                if "access_token" in response.text:
                    bearer_token = response.json()['access_token']
                    stage = "login"
                    api_logs = self.add_to_api_logs(api_logs, stage, unique_id, email)

                    logs = f"Logged in!"
                    self.tools.print_logs(logs, f'SIZEER', Fore.LIGHTCYAN_EX, task_number, task_mode='APP')

                    client = self.update_api(api_logs, snrapi_anonymous_token, client, task_number)

                    return client, bearer_token, api_logs
                else:
                    timeout = 20
                    logs = f"Account not verified yet! Waiting {timeout} seconds... [{email}]"
                    self.tools.print_logs(logs, f'SIZEER', Fore.LIGHTCYAN_EX, task_number, task_mode='APP')

                    time.sleep(timeout)
                    continue

    def set_login_variables(self, email, password, unique_id, anonymous_token):
        """A function used in order to set login variables like headers and data"""
        headers = {
            'user-agent': 'Dart/2.10 (dart:io)',
            'host': 'ro.sizeer.mcom.appchance.shop',
            'authorization': f'Anonymous {anonymous_token}',
            'content-type': 'application/json; charset=utf-8',
            'synerise-uuid': unique_id,
            'platform': 'Android',
        }

        data = {
            "email": email,
            "password": password
        }

        dumped_data = str(json.dumps(data))

        return dumped_data, headers

    def retrieve_user_points(self, client, task_number, bearer_token, email, unique_id,
                             api_logs, snrapi_anonymous_token, fn, ln, phone_number):
        """A function used in order to retrieve the users Points"""
        tries = 1
        retries = 1
        max_retries = 1
        stage = "points"

        api_logs = self.add_to_api_logs(api_logs, stage, unique_id, email)
        client = self.update_api(api_logs, snrapi_anonymous_token, client, task_number)

        time.sleep(2)

        logs = f"Fetching points..."
        self.tools.print_logs(logs, f'SIZEER', Fore.LIGHTCYAN_EX, task_number, task_mode='APP')

        while True:
            headers = {
                'user-agent': 'Dart/2.10 (dart:io)',
                'host': 'ro.sizeer.mcom.appchance.shop',
                'authorization': f'Bearer {bearer_token}',
                'synerise-uuid': unique_id,
                'platform': 'Android',
            }

            try:
                response = client.get('https://ro.sizeer.mcom.appchance.shop/api/users/profile/points/',
                                      headers=headers, timeout=10)

            except:
                logs = f"Timed Out Fetching points..."
                self.tools.print_logs(logs, f'SIZEER', Fore.RED, task_number, task_mode='APP')

                tries += 1

                if tries <= 5:
                    continue

                else:
                    logs = f"Too many timeouts!"
                    self.tools.print_logs(logs, f'SIZEER', Fore.RED, task_number, task_mode='APP')

                    return False, False

            else:
                try:
                    stage = "points"
                    api_logs = self.add_to_api_logs(api_logs, stage, unique_id, email)

                    points = response.json()["points"]
                    points = int(points)

                    retries += 1
                    max_retries += 1

                    if max_retries == 25:
                        logs = f"Points Crafting Failed. Account created but not enough points stored!"
                        self.tools.print_logs(logs, f'SIZEER', Fore.RED, task_number, task_mode='APP')

                        return False, False

                    if retries == 10 and points != 500:
                        logs = f"Still fetching points... Crafting takes longer than usual... [{points} points]"
                        self.tools.print_logs(logs, f'SIZEER', Fore.LIGHTCYAN_EX, task_number, task_mode='APP')

                        retries = 1

                    if points != 500:
                        client = self.update_api(api_logs, snrapi_anonymous_token, client, task_number)

                        time.sleep(2)
                        continue

                    logs = f"Points successfully fetched! {points} points."
                    self.tools.print_logs(logs, f'SIZEER', Fore.LIGHTCYAN_EX, task_number, task_mode='APP')

                    return client, points
                except:
                    logs = f"Unknown Error! [{logs}]"
                    self.tools.print_logs(logs, f'SIZEER', Fore.RED, task_number, task_mode='APP')

                    traceback.print_exc()

                    print(response.text)
                    return False, False

    def add_to_api_logs(self, api_logs, stage, unique_id, email, time_iso=None, other_info_dict=None):
        """
        A function used in order to communicate with SIZEER SNRAPI

        `time_iso` represents the date when the last request took place
        """
        if stage == "register":
            my_iso_date = datetime.utcnow().isoformat()
            my_iso_date = my_iso_date[:-3] + 'Z'

            api_dict = {
                "time": str(my_iso_date),
                "type": "visited-screen",
                "label": "More",
                "client": {
                    "uuid": unique_id
                },
                "params": {
                    "appVersion": "1.2.2",
                    "os": "Android",
                    "appBuildVersion": "2363",
                    "screenName": "More",
                    "source": "MOBILE_APP",
                    "email": email
                }
            }
            api_logs.append(api_dict)

            time.sleep(1.981)

            my_iso_date = datetime.utcnow().isoformat()
            my_iso_date = my_iso_date[:-3] + 'Z'
            api_dict = {
                "time": str(my_iso_date),
                "type": "visited-screen",
                "label": "Consents",
                "client": {
                    "uuid": unique_id
                },
                "params": {
                    "appVersion": "1.2.2",
                    "os": "Android",
                    "appBuildVersion": "2363",
                    "screenName": "Consents",
                    "source": "MOBILE_APP",
                    "email": email
                }
            }
            api_logs.append(api_dict)

            time.sleep(5.38149)

            my_iso_date = datetime.utcnow().isoformat()
            my_iso_date = my_iso_date[:-3] + 'Z'
            consents_dict = {
                "time": str(my_iso_date),
                "type": "custom",
                "action": "form.submit.update",
                "label": "Consents Update",
                "client": {
                    "uuid": unique_id
                },
                "params": {
                    "Mkt_SMS_MIG_tresc": "Sunt de acord ca MIG Marketing Investment Group Ro S.R.L. să-mi trimită informații comerciale și promoționale, inclusiv newslettere pe telefon.",
                    "appVersion": "1.2.2",
                    "formType": "appchance_customer_consents_form_type",
                    "os": "Android",
                    "Mkt_Email_MIG_Partners_wersja": "2687",
                    "store_regulations_wersja": "2679",
                    "Mkt_SMS_MIG_Partners_wersja": "2683",
                    "Mkt_SMS_MIG_wersja": "2681",
                    "Mkt_Email_MIG_tresc": "Sunt de acord ca MIG Marketing Investment Group Ro S.R.L. să-mi trimită informații comerciale și promoționale, inclusiv newslettere prin e-mail.",
                    "Mkt_SMS_MIG": "1",
                    "source": "MOBILE_APP",
                    "privacy_policy_tresc": "Sunt de acord cu&nbsp;regulamentul&nbsp;și&nbsp;politica de confidențialitate a magazinului.",
                    "Mkt_Email_MIG_Partners_tresc": "Doresc să primesc pe e-mail noutăți, promoții și informații comerciale de la partenerii MIG Marketing Investment Group Ro S.R.L.",
                    "Mkt_SMS_MIG_Partners": "1",
                    "Mkt_SMS_MIG_Partners_tresc": "Doresc să primesc pe telefon noutăți, promoții și informații comerciale de la partenerii MIG Marketing Investment Group Ro S.R.L",
                    "Mkt_Email_MIG_wersja": "2685",
                    "store_regulations_tresc": "Sunt de acord cu&nbsp;regulamentul&nbsp;și&nbsp;politica de confidențialitate a magazinului.",
                    "Mkt_Email_MIG_Partners": "1",
                    "appBuildVersion": "2363",
                    "privacy_policy_wersja": "2679",
                    "Mkt_Email_MIG": "1",
                    "email": email
                }
            }
            api_logs.append(consents_dict)

        elif stage == "generated":
            my_iso_date = datetime.utcnow().isoformat()
            my_iso_date = my_iso_date[:-3] + 'Z'

            api_dict = {
                "time": my_iso_date,
                "type": "registered",
                "label": "Client Data Update",
                "client": {
                    "uuid": unique_id
                },
                "params": {
                    "appVersion": "1.2.2",
                    "formType": "appchance_customer_registration_form_type",
                    "os": "Android",
                    "appBuildVersion": "2363",
                    "source": "MOBILE_APP",
                    "email": email
                }
            }
            api_logs.append(api_dict)
            time.sleep(0.004)

            my_iso_date = datetime.utcnow().isoformat()
            my_iso_date = my_iso_date[:-3] + 'Z'

            registered_dict = {
                "time": str(my_iso_date),
                "type": "custom",
                "action": "account.status",
                "label": "Account active",
                "client": {
                    "uuid": unique_id
                },
                "params": {
                    "accountStatus": "Active",
                    "appVersion": "1.2.2",
                    "os": "Android",
                    "appBuildVersion": "2363",
                    "source": "MOBILE_APP",
                    "email": email
                }
            }
            api_logs.append(registered_dict)

            time.sleep(0.0005)
            my_iso_date = datetime.utcnow().isoformat()
            my_iso_date = my_iso_date[:-3] + 'Z'

            api_dict = {
                "time": str(my_iso_date),
                "type": "custom",
                "action": "form.submit.update",
                "label": "Client Data Update",
                "client": {
                    "uuid": unique_id
                },
                "params": {
                    "zipCode": "",
                    "appVersion": "1.2.2",
                    "formType": "appchance_customer_registration_form_type",
                    "custom_name": other_info_dict["fn"],
                    "address": "",
                    "os": "Android",
                    "phone": other_info_dict["phone"],
                    "appBuildVersion": "2363",
                    "custom_lastname": other_info_dict["ln"],
                    "source": "MOBILE_APP",
                    "email": email
                }
            }
            api_logs.append(api_dict)

            time.sleep(0.0005)
            my_iso_date = datetime.utcnow().isoformat()
            my_iso_date = my_iso_date[:-3] + 'Z'

            api_dict = {
                "time": str(my_iso_date),
                "type": "custom",
                "action": "form.submit.update",
                "label": "Consents Update",
                "client": {
                    "uuid": unique_id
                },
                "params": {
                    "Mkt_SMS_MIG_tresc": "Sunt de acord ca MIG Marketing Investment Group Ro S.R.L. să-mi trimită informații comerciale și promoționale, inclusiv newslettere pe telefon.",
                    "appVersion": "1.2.2",
                    "formType": "appchance_customer_consents_form_type",
                    "os": "Android",
                    "Mkt_Email_MIG_Partners_wersja": "2687",
                    "store_regulations_wersja": "2679",
                    "Mkt_SMS_MIG_Partners_wersja": "2683",
                    "Mkt_SMS_MIG_wersja": "2681",
                    "Mkt_Email_MIG_tresc": "Sunt de acord ca MIG Marketing Investment Group Ro S.R.L. să-mi trimită informații comerciale și promoționale, inclusiv newslettere prin e-mail.",
                    "Mkt_SMS_MIG": "1",
                    "source": "MOBILE_APP",
                    "privacy_policy_tresc": "Sunt de acord cu&nbsp;regulamentul&nbsp;și&nbsp;politica de confidențialitate a magazinului.",
                    "Mkt_Email_MIG_Partners_tresc": "Doresc să primesc pe e-mail noutăți, promoții și informații comerciale de la partenerii MIG Marketing Investment Group Ro S.R.L.",
                    "Mkt_SMS_MIG_Partners": "1",
                    "Mkt_SMS_MIG_Partners_tresc": "Doresc să primesc pe telefon noutăți, promoții și informații comerciale de la partenerii MIG Marketing Investment Group Ro S.R.L",
                    "Mkt_Email_MIG_wersja": "2685",
                    "store_regulations_tresc": "Sunt de acord cu&nbsp;regulamentul&nbsp;și&nbsp;politica de confidențialitate a magazinului.",
                    "Mkt_Email_MIG_Partners": "1",
                    "appBuildVersion": "2363",
                    "privacy_policy_wersja": "2679",
                    "Mkt_Email_MIG": "1",
                    "email": email
                }
            }
            api_logs.append(api_dict)

        elif stage == "login":
            my_iso_date = datetime.utcnow().isoformat()
            my_iso_date = my_iso_date[:-3] + 'Z'

            api_dict = {
                "time": str(my_iso_date),
                "type": "custom",
                "action": "client.login",
                "label": "User logged in",
                "client": {
                    "uuid": unique_id
                },
                "params": {
                    "appBuildVersion": "2363",
                    "appVersion": "1.2.2",
                    "source": "MOBILE_APP",
                    "os": "Android",
                    "email": email
                }
            }
            api_logs.append(api_dict)

        elif stage == "points":
            my_iso_date = datetime.utcnow().isoformat()
            my_iso_date = my_iso_date[:-3] + 'Z'

            api_dict = {
                "time": str(my_iso_date),
                "type": "visited-screen",
                "label": "Your Card",
                "client": {
                    "uuid": unique_id
                },
                "params": {
                    "appVersion": "1.2.2",
                    "os": "Android",
                    "appBuildVersion": "2363",
                    "screenName": "YourCard",
                    "source": "MOBILE_APP",
                    "email": email
                }
            }
            api_logs.append(api_dict)

        return api_logs

    def update_api(self, api_logs, snrapi_anonymous_token, client, task_number):
        """
        Function used in order to keep the SNRapi updated and
        to trigger it in order to double the points
        """
        no_of_requests = randint(30, 40)
        dumped_json_data = json.dumps(api_logs)
        headers = {
            'Host': 'api.snrapi.com',
            'authorization': f'Bearer {snrapi_anonymous_token}',
            'api-version': '4.4',
            'application-id': 'Sizeer',
            'user-agent': 'Synerise Android SDK 3.8.8',
            'accept': 'application/json',
            'mobile-info': 'android;31;G985FXXSCEUL7;12;SM-A300FU;samsung;3.8.8',
            'content-type': 'application/json; charset=UTF-8',
        }

        try:
            for i in range(0, no_of_requests):
                response = client.post('https://api.snrapi.com/v4/events/batch',
                                       headers=headers, data=str(dumped_json_data))
        except:
            logs = f"Timed Out fetching api!"
            self.tools.print_logs(logs, f'SIZEER', Fore.RED, task_number, task_mode='APP')

        return client
