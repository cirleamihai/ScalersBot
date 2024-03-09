import os, json, traceback, sys, datetime
from unipath import Path

import colorama
from colorama import Fore
colorama.init(autoreset=True)

global cur_path
cur_path = os.path.dirname(os.path.realpath(__file__))
p = Path(cur_path)
cur_path = p.parent

path_for_tools = cur_path + '\\Tools'
sys.path.append(path_for_tools)

# noinspection PyUnresolvedReferences
from bot_tools import BotTools

class JsonClass():
    """

    A class used in order to write to json files different types of information

    """
    def __init__(self):
        self.folder_name = f'{cur_path}\\Json Related\\'
        self.accounts_folder = f'{cur_path}\\Json Related\\Accounts'
        self.sizes_folder = f'{cur_path}\\Json Related\\Sizes\\'

    def get_accounts_info(self, email):
        """We check wether"""
        name = email.split("@")[0]
        filename = f"{self.accounts_folder}\\{name}.json"

        account = ""
        with open(filename) as f:
            each_line_string = f.readlines()
            for line in each_line_string:
                account += line.strip()

        account = self.debug_json(account, category="particular")
        if not account:
            return False

        account = json.loads(account)

        return account

    def write_fresh_sizes_to_file(self, filename, json_size_variant_dict):
        """A function used in order to write the sizes into a file"""
        filename = self.sizes_folder + filename
        with open(filename, 'w') as f:
            json.dump(json_size_variant_dict, f, indent=4)

    def get_sizes(self, filename):
        """A function used in order to retrieve the sizes from the json dict"""
        filename = self.sizes_folder + filename
        with open(filename) as f:
            sizes_info = json.load(f)

        return sizes_info

    def tool_write_list_of_accounts(self, list_of_accounts, filename="dev_sizeer_accounts_under_work.json"):
        """A function used in order to append the lists of accounts"""
        filename = self.folder_name + filename

        with open(filename, 'w') as f:
            json.dump(list_of_accounts, f, indent=4)

    def store_new_account(self, email, password, points):
        """
        A function used in order to store the account information once successfully created

        ~Works ONLY FOR NEW ACCOUNTS~
        """
        tools = BotTools()

        logs = f"Storing account... Email: {email}"
        tools.print_logs(logs, f'SIZEER', Fore.LIGHTMAGENTA_EX, task_mode='SYSTEM')

        try:
            succes = self.store_fresh_account_accounts_list(email, password, points)
            if not succes:
                return False

            name = email.split('@')[0]
            filename = f"{self.folder_name}\\Accounts\\{name}.json"
            time_now = datetime.datetime.now()

            new_account_data = {
                  "email": email,
                  "password": password,
                  "in use": False,
                  "last_used": str(time_now),
                  "placed orders": 0,
                  "points": points,
                  "coupons": {
                        "Dunk Low Adults": False,
                        "Dunk High Adults": False,
                        "Dunk Low Kids": False,
                        "Uncaching coupon": False
                  }
            }

            with open(filename, "w") as json_file:
                json.dump(new_account_data, json_file, indent=4)

            logs = f"Account successfully stored! Email: {email}"
            tools.print_logs(logs, f'SIZEER', Fore.LIGHTGREEN_EX, task_mode='SYSTEM')

            return True

        except:
            logs = f"Unknown Error. [{logs}]"
            tools.print_logs(logs, f'SIZEER', Fore.RED, task_mode='SYSTEM')

            traceback.print_exc()

            return False

    def store_fresh_account_accounts_list(self, email, password, points):
        """Function used in order to store the freshly generated account"""
        folder_path = f"{self.folder_name}\\Accounts\\Accounts List"
        email_pass_list = {
            "email": email,
            "password": password
        }

        if int(points) == 250:
            files_to_be_edited_list = ['fresh_accounts.json']

        else:
            # In case we have created it with 500 points
            files_to_be_edited_list = ['good_accounts.json', 'dunk_low_adults.json',
                                       'dunk_high_adults.json', 'dunk_low_kids.json']

        for file in files_to_be_edited_list:
            # We are iterating through each file from the list
            filename = f"{folder_path}\\{file}"
            accounts_list = ""

            with open(filename) as f:
                each_line_string = f.readlines()
                for line in each_line_string:
                    accounts_list += line.strip()

            accounts_list = self.debug_json(accounts_list, category="bulk")
            if not accounts_list:
                return False

            accounts_list = json.loads(accounts_list)
            accounts_list.append(email_pass_list)

            with open(filename, 'w') as f:
                json.dump(accounts_list, f, indent=4)

        return True

    def retrieve_dunks_accounts_by_category(self, task_category):
        """A function used in order to retrieve information about each account from a given category"""
        filename = f"{self.folder_name}\\Accounts\\Accounts List\\{task_category}"
        accounts_list = ""

        if not task_category:
            return 0

        with open(filename) as f:
            each_line_string = f.readlines()
            for line in each_line_string:
                accounts_list += line.strip()

        accounts_list = self.debug_json(accounts_list, category="bulk")
        if not accounts_list:
            return []

        accounts_list = json.loads(accounts_list)

        return accounts_list

    def remove_account_from_category_class(self, task_category, acc_dict):
        accounts_list = self.retrieve_dunks_accounts_by_category(task_category)
        if not accounts_list:
            return []

        accounts_list.remove(acc_dict)

        filename = f"{self.folder_name}\\Accounts\\Accounts List\\{task_category}"
        with open(filename, 'w') as f:
            json.dump(accounts_list, f, indent=4)

        return accounts_list

    def update_each_account_general_information(self, updated_values):
        """
        A function used in order to update each account information regarding the number of:

        ~points
        ~last_used
        ~in use
        ~coupons information

        """
        email = updated_values["email"]
        name = email.split('@')[0]
        account_dict = ""
        filename = f"{self.folder_name}\\Accounts\\{name}.json"

        with open(filename) as f:
            each_line_string = f.readlines()
            for line in each_line_string:
                account_dict += line.strip()

        account_dict = self.debug_json(account_dict, category="particular")
        if not account_dict:
            return False

        account_dict = json.loads(account_dict)
        account_dict["points"] = updated_values["points"]
        account_dict["last_used"] = str(datetime.datetime.now())
        account_dict["in use"] = updated_values["in use"]

        #Accessing the coupons dict
        account_coupons = account_dict["coupons"]
        for key, value in account_coupons.items():
            try:
                account_coupons[key] = updated_values["coupons"][key]
            except:
                pass

        with open(filename, 'w') as f:
            json.dump(account_dict, f, indent=4)

    def get_account_information(self, email):
        """Getting the stored account information"""
        name = email.split("@")[0]
        filename = f"{self.folder_name}\\Accounts\\{name}.json"
        account_dict = ""
        try:
            with open(filename) as f:
                each_line_string = f.readlines()
                for line in each_line_string:
                    account_dict += line.strip()

            account_dict = self.debug_json(account_dict, category="particular")
            if not account_dict:
                return False

            return account_dict
        except:
            traceback.print_exc()
            return False

    def write_corrupted_account(self, updated_data):
        """

        Function used for the accounts that haven't been
        successfully stored during the account generation

        """
        email = updated_data["email"]
        name = email.split("@")[0]

        filename = f"{self.folder_name}\\Accounts\\{name}.json"
        with open(filename, 'w') as f:
            json.dump(updated_data, f, indent=4)

        return True

    def debug_json(self, my_bugged_json, category="bulk"):
        """Used in order to debug the json function"""
        try:
            iterator = len(my_bugged_json) - 1
        except:
            iterator = 0

        number_of_skips = 0

        while (my_bugged_json[iterator] != '"' and my_bugged_json[iterator] != 'e') and iterator > 0:
            iterator -= 1
            number_of_skips += 1

        if iterator == 0:
            return ""

        else:
            my_bugged_json = my_bugged_json[:-number_of_skips]

        if category == "bulk":
            my_bugged_json += "}]"
        else:
            my_bugged_json += "}}"

        return my_bugged_json

if __name__ == "__main__":
    p = Path(cur_path)

    updated_account = {
        "email": "@catchall",
        "password": "",
        "in use": False,
        "last_used": "2022-01-26 15:53:24.548640",
        "placed orders": 0,
        "points": 500,
        "coupons": {
            "Dunk Low Adults": "SIRODUNKL500",
            "Dunk High Adults": "SIRODUNKH500",
            "Dunk Low Kids": "SIRODUNK5",
            "Uncaching coupon": False
        }
    }

    JsonClass().write_updated_account(updated_account)

    #print(p.parent.parent.parent)