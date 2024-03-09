import json, os
cur_path = os.path.dirname(os.path.realpath(__file__))

class Json_kws:
    """Class representing site changes written in json format"""
    def __init__(self, filename):
        self.filename = f"{cur_path}\\Json Folder\\{filename}"

    def write_new_items(self, products_list):
        """Writing all the new items that appear on the website search page"""
        # Setting the items dict that will be written inside Json file
        items_dict = {}
        items_dict['items'] = products_list

        with open(self.filename, 'w') as f:
            json.dump(items_dict, f, indent=4)

    def load_old_items(self):
        """Loading already found items"""
        old_prods = ""
        with open(self.filename) as f:
            each_line_string = f.readlines()
            for line in each_line_string:
                old_prods += line.strip()

        if '}}' in str(old_prods):
            account = str(old_prods)[:-1]

        old_products_list = json.loads(old_prods)
        items = list(old_products_list["items"])

        return items

    def write_new_size_lngth(self, length):
        """Writing the new lenght of sizes each time"""

        with open(self.filename, 'w') as f:
            json.dump(length, f, indent=4)

    def load_old_size_lngth(self):
        """Loading already found sizes"""
        with open(self.filename) as f:
            old_sizes_dict = json.load(f)
            old_sizes_lngth = old_sizes_dict

        return  old_sizes_lngth

    def load_keywords(self):
        """Loading the keywords"""
        keywords_folder = 'Json Folder\keywords.json'
        with open(keywords_folder) as f:
            keywords_list = json.load(f)

        return keywords_list

    def dump_keywords(self, keywords_list):
        """Dumping the new set of keywords"""
        keywords_folder = 'Json Folder\keywords.json'

        with open(keywords_folder, 'w') as f:
            json.dump(keywords_list, f, indent=4)