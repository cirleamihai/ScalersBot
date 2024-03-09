import random, js2py, datetime, traceback, hashlib
from time import time
from pymongo import MongoClient

gpus = [
    "ANGLE (NVIDIA GeForce GTX 1080 Ti Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce GTX 1080 Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce GTX 1070 Ti Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce GTX 1070 Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce GTX 1060 6GB Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce GTX 1060 3GB Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce RTX 2080 Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce RTX 2070 Direct3D11 vs_5_0 ps_5_0)"
]
global constant_akam_version, rCFP
constant_akam_version = '7a74G7m23Vrp0o5c9271291.7'

class Abck:
    def __init__(self):
        # Global vars, in order of use (kinda)
        self.xagg = "12147"  # Xagg, related to Bmak.xagg
        self.product_sub = "20030107"  # Psub, related to Bmak.psub which is related to native navigator.productSub
        self.language = "en-US"  # Lang, related to Bmak.lang which is related to native navigator.Language
        self.engine = "Gecko"  # Prod, related to Bmak.prod which is related to native navigator.product
        self.plugin_count = "2"  # Plen, related to Bmak.plen which is amount of plugins
        self.headless = "0"  # Pen, related to Bmak.pen which is if browser is headless (native window._phantom)
        self.window = "0"  # Wen, related to Bmak.wen which is looking for a new window. (Detecting selenium)
        self.spam_bot = "0"  # Den, related to Bmak.den which is looking if you are a spam bot (Detecting domAutomation)
        self.callPhantom = "0"  # BD Function cpen
        self.is_ie = "0"  # . i1
        self.docMode = "0"  # . dm
        self.chromeWS = "0"  # . cwen
        self.onLine = "1"  # . non
        self.opera = "0"  # . opc
        self.firefox = "0"  # . fc
        self.safari = "0"  # . sc
        self.rtcSupport = "1"  # . wrc
        self.windowTop = "0"  # . isc
        self.vibration = "1"  # . vib
        self.battery = "1"  # . bat
        self.forEach = "0"  # . x11
        self.filereader = "1"  # . x12

    # Get_cf_date Function
    def get_cf_date(self):
        return int(time() * 1000)

    # AB Function (Akamais 'hashing' method)
    def ab(self, string):
        if string == None:
            return -1
        sum = 0
        for i in range(len(string)):
            # print(ord(string[i]))
            if ord(string[i]) < 128:
                sum += ord(string[i])

        return sum

    # BD Function (Only to build as string)
    def bd(self):
        bd_string = ""
        bd_string += "cpen:" + self.callPhantom + ","
        bd_string += "i1:" + self.is_ie + ","
        bd_string += "dm:" + self.docMode + ","
        bd_string += "cwen:" + self.chromeWS + ","
        bd_string += "non:" + self.onLine + ","
        bd_string += "opc:" + self.opera + ","
        bd_string += "fc:" + self.firefox + ","
        bd_string += "sc:" + self.safari + ","
        bd_string += "wrc:" + self.rtcSupport + ","
        bd_string += "isc:" + self.windowTop + ","
        bd_string += "vib:" + self.vibration + ","
        bd_string += "bat:" + self.battery + ","
        bd_string += "x11:" + self.forEach + ","
        bd_string += "x12:" + self.filereader
        return bd_string

    def gd(self,
           availWidth, availHeight, width, height, clientWidth, clientHeight, outerWidth,
           user_agent,
           start_ts,
           has_challenge,
           d3=""):
        # Vars
        z1 = int(start_ts / (2016 * 2016))  # z1
        if not d3:
            d3 = self.get_cf_date() % 10000000  # d3, current timestamp divided by  1e7 (7 zeros)
        else:
            d3 = d3
        screen_string = str(availWidth) + "," + str(availHeight) + "," + str(width) + "," + str(height) + "," + str(
            clientWidth) + "," + str(clientHeight) + "," + str(outerWidth)  # Screen sizes
        bd_string = self.bd()
        ua_hash = self.ab(user_agent)
        rnd_seed = str(random.random())[0:14]
        ts_2 = start_ts / 2

        if int(ts_2) == ts_2:
            ts_2 = int(ts_2)

        # Build string
        gd_string = ""
        gd_string += user_agent + ",uaend,"  # User-agent
        gd_string += self.xagg + ","  # Xagg, related to Bmak.xagg
        gd_string += self.product_sub + ","  # Psub, related to Bmak.psub
        gd_string += self.language + ","  # Lang, related to Bmak.lang
        gd_string += self.engine + ","  # Prod, related to Bmak.prod
        gd_string += self.plugin_count + ","  # Plen, related to Bmak.plen
        gd_string += self.headless + ","  # Pen, related to Bmak.pen
        gd_string += self.window + ","  # Wen, related to Bmak.wen
        gd_string += self.spam_bot + ","  # Den, related to Bmak.den
        gd_string += str(z1) + ","  # z1, related to Bmak.z1
        gd_string += str(d3) + ","  # d3, related to Bmak.d3
        gd_string += screen_string + ","  # Screen info
        gd_string += "," + bd_string + ","  # BD, various info about the browser
        gd_string += str(ua_hash) + ","  # User-Agent Hash
        gd_string += str(rnd_seed) + ","  # Random seed number
        gd_string += str(ts_2)  # Start timestamp divided by 2

        if has_challenge:
            gd_string += ",1,loc:"  # Loc, related to bmak.loc which is empty

        else:
            gd_string += ",0,loc:"  # Loc, related to bmak.loc which is empty

        return gd_string, d3

    def sed(self):
        return "0,0,0,0,1,0,0"

    def fas(self):
        return "30261693"

    def np(self):
        return "11133333331333333333"

    def calc_o9(self, d3):
        t = e = d3
        for c in range(0, 5):
            n = int(t / 10 ** c) % 10
            a = n + 1
            mn = n % 4
            if mn == 0:
                e = e * a
            elif mn == 1:
                e = e + a
            else:
                e = e - a
        return e

class Akamai:
    """

    A class used in order to generate Akamai Shitty Cookies

    ---------LOW + MEDIUM SECURITY ONLY---------

    """

    def __init__(self):
        """Stable Values"""
        self.start_ts = int(time())

    def toString(self, number):
        """The number is float and less then 0 so we will deal with that"""
        hex_string = '0.'
        hex_dict = [
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'
        ]
        is_right_length = True

        while number:
            number = number * 16
            hexa_nr = int(number)
            number = number - hexa_nr
            hex_string += str(hex_dict[hexa_nr])

        return hex_string

    def bdm(self, t, a):
        """bmak.bdm function with js2py"""

        js_commands = 'function bdm(t, a) { for (var e = 0, n = 0; n < t.length; ++n) e = (e << 8 | t[n]) >>> 0, e %= a; return e; }'
        bdm_value = js2py.eval_js(js_commands)

        return bdm_value(t, a)

    # Get_cf_date Function
    def get_cf_date(self):
        return int(time() * 1000)

    def updatet(self, start_ts):
        actual_time = int(time() * 1000)
        return actual_time - start_ts

    def mn_s(self, first_abck_part, challenge_part, start_ts, random_number, mn_mc):
        # Tranforming the string to its sha256 value
        challenge_string = f'{first_abck_part}{start_ts}{challenge_part}{mn_mc}{random_number}'
        challenge_string_bytes = bytes(challenge_string, 'utf-8')
        hash_object = hashlib.sha256(challenge_string_bytes)

        # Then converting from hexa to decimal value
        sha256_string = hash_object.hexdigest()
        chars_list = []
        char_str = ''
        iterator = 0

        for character in sha256_string:
            if iterator % 2 == 0:
                char_str += character
            else:
                char_str += character
                chars_list.append(char_str)
                char_str = ''

            iterator += 1

        # Then adding each value to an array
        decimal_representation_list = []

        for hexa_encoded in chars_list:
            decimal_nr = int(hexa_encoded, 16)
            decimal_representation_list.append(decimal_nr)

        return decimal_representation_list

    def bpd(self, task_number, abck_cookie="",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.115 Safari/537.36",
            sizeer_link="https://sizeer.ro",
            has_challenge=False,
            is_second_challenge=False,
            ran_fpcf_td="",
            start_ts=0,
            o9_value="",
            d3="",
            doact="",
            device_data="",
            same_last_shit="",
            random_decimal_number=""):
        """MAIN FUNCTION"""
        sensor_data = constant_akam_version

        if not device_data:
            device_data = self.get_database(task_number)

        # The same for every sensor
        getforminfo = "0,0,0,1,1890,1979,0;0,-1,0,1,4619,4708,0;0,-1,0,1,5801,5979,0;"
        site_url = sizeer_link
        i = "-1,2,-94,-101,do_en,dm_en,t_en-1,2,-94,-105,"
        if not same_last_shit:
            same_last_shit = random.randint(10, 20)

        y1_value = 4064256

        screen_info = device_data['screen']
        availHeight = screen_info['availHeight']
        availWidth = screen_info['availWidth']
        width = screen_info['width']
        height = screen_info['height']
        client_width = screen_info['clientWidth']
        client_height = screen_info['clientHeight']
        outerWidth = screen_info['outerWidth']

        bmak_mr = device_data['mr']
        fpcf_val_str_and_ab = device_data['fpValstr']
        rval = device_data['rVal']
        rcfp = device_data['rCFP']

        if is_second_challenge:
            device_info_string = device_data['device_info']['challenge']
        else:
            device_info_string = device_data['device_info']['normal']

        try:
            # Your starting timestamp
            if not start_ts:
                start_ts = self.get_cf_date()

            z1 = int(start_ts / y1_value)
            d2 = int((z1 / 23))
            f = int(d2 / 6)

            device_info_gd, d3 = Abck().gd(
                availHeight, availWidth, width, height, client_width, client_height, outerWidth,  # Screen sizes
                user_agent,
                # User-Agent
                start_ts,  # Your starting timestamp
                has_challenge,
                d3=d3
            )

            static_data_1 = '-1,2,-94,-100,'
            sensor_data += static_data_1
            sensor_data += device_info_gd
            sensor_data += i
            sensor_data += getforminfo
            static_data_2 = '-1,2,-94,-102,'
            sensor_data += static_data_2
            sensor_data += getforminfo
            static_data_3 = '-1,2,-94,-108,'
            sensor_data += static_data_3

            # Sensor data after kakt
            static_data_4 = '-1,2,-94,-110,'
            sensor_data += static_data_4

            # Sensor data after mact
            static_data_5 = '-1,2,-94,-117,'
            sensor_data += static_data_5

            # Sensor data after tact
            static_data_6 = '-1,2,-94,-111,'
            sensor_data += static_data_6

            if not doact:
                doact = self.updatet(start_ts)
            if has_challenge:
                # The same for first and second challenge
                new_data = f'0,{doact},-1,-1,-1;'
                sensor_data += new_data

            # Sensor data after doact
            static_data_7 = '-1,2,-94,-109,'
            sensor_data += static_data_7

            if has_challenge:
                new_data = f"0,{doact},-1,-1,-1,-1,-1,-1,-1,-1,-1;"
                sensor_data += new_data

            # Sensor data after dmact
            static_data_8 = '-1,2,-94,-114,'
            sensor_data += static_data_8

            # Sensor data after pact
            static_data_9 = '-1,2,-94,-103,'
            sensor_data += static_data_9

            # Sensor data after vcact
            static_data_10 = '-1,2,-94,-112,'
            sensor_data += static_data_10

            sensor_data += site_url
            static_data_11 = '-1,2,-94,-115,'
            sensor_data += static_data_11

            # For the first one always the same
            ke_me_te_values = '1,32,32,'
            sensor_data += ke_me_te_values

            if has_challenge:
                doe_dme_values = f'{doact},{doact},0,{doact * 2},'
                sensor_data += doe_dme_values

                # if it is the first challenge
                if not is_second_challenge:
                    updatet_ran_ts = self.updatet(start_ts)

                # if it is the second one
                else:
                    updatet_ran_ts = self.updatet(start_ts)

                sensor_data = sensor_data + f'{updatet_ran_ts},'

            else:
                # Device motion values
                motion_values = '0,0,0,0,'
                sensor_data += motion_values

                # updatet = bmak.get_cf_date() - bmak.start_ts
                updatet = f'{random.randint(1, 10)},'
                sensor_data += updatet

            started_time = '0,' + str(start_ts) + ','
            sensor_data += started_time

            if has_challenge:
                if not ran_fpcf_td:
                    ran_fpcf_td = str(random.randint(20, 40))
                sensor_data = sensor_data + f'{ran_fpcf_td},'

            else:
                fpcf_td = '-999999,'
                sensor_data += fpcf_td

            if has_challenge:
                sensor_data = sensor_data + str(d2) + ',0,0,' + str(f) + ',0,0,'
            else:
                sensor_data = sensor_data + str(d2) + ',0,0,' + str(f) + ',0,0,'

            if has_challenge:
                sensor_data = sensor_data + f'{updatet_ran_ts},'
            else:
                fixed_ts = f'{random.randint(5, 8)},'
                sensor_data += fixed_ts

            if has_challenge:
                sensor_data += f'{doact * 2 + random.randint(0, 1)},0,'
            else:
                # updatet = int(time() * 1000) - start_ts
                sensor_data += '0,0,'

            # abck_cookie = 'A02599E8A93A8B0FEA42385291B043B4~-1~YAAQLUx1aI0ovx97AQAAZU8HPAZ7lBh3+kdfanFk4Y3cH3Bcn7gpfk0A0rhJwvWSSKDV9/CRCBsHRKnij9QoH7VSMTrNXhmANIL/unhn3Jm8f5SKPtPT9PQl24++TJaotDvTdkkMNcpzf+PjDPiUKm9R8VdXQU3h3xPOt9v9+h3Xh8b7fAOdzqcDXxmCsKH4MoCMaBgEIBlU8bgRK2icbtmVx/I/Me3pXkwNSRth4DtKMlnAsIz5ViTFrlqdpc7vIr36kuxV6ZHR8kEwumZfEmLsTgfMqKoPu+HxuIqGbZkr9s9xU5iUTraMtj2nNrJQq9GjKpr85XlEvPejmMv76fIZ/Y3OUV1fttIgkan5o8mg5SeO6NCbdrUHzc+aecEyJeZ7PxJ1r5QV~-1~-1~-1'
            sensor_data += abck_cookie

            ab_abck = Abck().ab(abck_cookie)
            sensor_data = sensor_data + ',' + str(ab_abck)

            if has_challenge:
                rVal_rCFP = f',{rval},{rcfp},'
                sensor_data += rVal_rCFP
            else:
                first_post_values = ',-1,-1,'
                sensor_data += first_post_values

            fas_value = Abck().fas()
            sensor_data = sensor_data + fas_value + ',PiZtE,'

            jrs_number = 10000 + random.randint(0, 99999)
            if not random_decimal_number:
                random_decimal_number = random.randint(10, 99)
            sensor_data += f'{jrs_number},{random_decimal_number},0,-1'

            static_data_12 = '-1,2,-94,-106,'
            sensor_data += static_data_12

            # Here depends on what post we are
            # If we are on the first post then we are completing with '0,0'
            if has_challenge:
                if not is_second_challenge:
                    sensor_data += '9,1'
                else:
                    sensor_data += '8,2'
            else:
                sensor_data += '0,0'

            static_data_13 = '-1,2,-94,-119,'
            sensor_data += static_data_13

            if has_challenge:
                sensor_data += bmak_mr
            else:
                sensor_data += '-1'

            static_data_14 = '-1,2,-94,-122,'
            sensor_data += static_data_14

            if is_second_challenge:
                sensor_data += '0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,'

                first_abck_part = abck_cookie.split('~')[0]
                challenge_part = abck_cookie.split('||1-')[1].split('-')[0]
                random_nr = random.random()
                first_random_number = self.toString(random_nr)
                first_decimal_representation_list = self.mn_s(first_abck_part, challenge_part, start_ts,
                                                              first_random_number, mn_mc=1)

                # The hexadecimal string of numbers
                radix_numbers_string = f'{first_random_number},'

                good_numbers = 1
                mn_mc_indx = 2
                retry_times_list = []
                retry_times = 0
                while good_numbers <= 9:
                    # Extracting the hexa-decimal number
                    random_nr = random.random()
                    random_number = self.toString(random_nr)

                    decimal_representation_list = self.mn_s(first_abck_part, challenge_part, start_ts, random_number,
                                                            mn_mc=mn_mc_indx)
                    if 0 == self.bdm(decimal_representation_list, mn_mc_indx):
                        radix_numbers_string += f"{random_number},"
                        retry_times_list.append(retry_times)
                        retry_times = 0
                        mn_mc_indx += 1

                    else:
                        retry_times += 1
                        good_numbers -= 1
                    good_numbers += 1

                random_numbers_string = radix_numbers_string[:-1]
                random_numbers_string += ';'
                sensor_data += random_numbers_string

                # The number of retries are corellated to the time
                number_of_retries = '0,'
                time_of_retries = '2,'

                for retry_number in retry_times_list:
                    if retry_number == 0:
                        time_of_retries += '2,'

                    elif retry_number == 1:
                        time_of_retries += '1,'

                    elif retry_number > 1 and retry_number < 5:
                        time_of_retries += '2,'

                    else:
                        time_of_retries += f'{random.randint(3, 7)},'

                    number_of_retries += f"{retry_number},"

                number_of_retries = number_of_retries[:-1] + ';'
                time_of_retries = time_of_retries[:-1] + ';'
                sensor_data = sensor_data + time_of_retries + number_of_retries

                second_part = f'{first_abck_part},{start_ts},{challenge_part},{first_abck_part}{start_ts}{challenge_part},' \
                              f'1,1,{first_random_number},{first_abck_part}{start_ts}{challenge_part}1{first_random_number},'
                sensor_data += second_part

                string_sha = ''
                for decimal_number in first_decimal_representation_list:
                    string_sha += f'{decimal_number},'

                string_sha += f'0,{start_ts + updatet_ran_ts};'
                sensor_data += string_sha
                sensor_data += '-1,2,-94,-126,-1,2,-94,-127,'
            else:
                static_data_15 = '0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,'
                sensor_data += static_data_15

            if has_challenge:
                site_perms = '10321144041300043122'
                sensor_data += site_perms

            else:
                static_data_16 = '8'
                sensor_data += static_data_16

            sensor_data_without_version = sensor_data.split('1.7')[1]
            pow_ab = Abck().ab(sensor_data_without_version)
            # Version 1.7 counts as 150 in ascii value.
            # If the version changes, change the ascii value aswell
            mega_power = 24 + pow_ab + 150

            if has_challenge:
                static_data_dont_know = \
                    f'-1,2,-94,-70,{fpcf_val_str_and_ab}-1,2,-94,-116,'
                sensor_data += static_data_dont_know
            else:
                some_static_data = '-1,2,-94,-70,-1-1,2,-94,-80,'
                sensor_data += some_static_data

                # In the first post the value is always equal to -1
                ab_fpValstr = Abck().ab("-1")
                sensor_data = sensor_data + str(ab_fpValstr) + '-1,2,-94,-116,'

            if not o9_value:
                o9_value = Abck().calc_o9(d3)

            sensor_data = sensor_data + str(o9_value) + '-1,2,-94,-118,'
            sensor_data = sensor_data + str(mega_power) + f'-1,2,-94,-129,'

            if has_challenge:
                # if it's first challenge we do this
                if not is_second_challenge:
                    device_info = f'{device_info_string}-1,2,-94,-121,' \
                                  f';{random.randint(10, 20)};{same_last_shit};0'
                    sensor_data += device_info

                # if second we do this
                else:
                    device_info = f'{device_info_string}-1,2,-94,-121,' \
                                  f';{random.randint(3, 10)};{same_last_shit};0'
                    sensor_data += device_info

            else:
                sensor_data += f'-1,2,-94,-121,;{random.randint(3, 8)};-1;0'

            # print(sensor_data)

            # -----THE END-----
            if has_challenge:
                if not is_second_challenge:
                    return sensor_data, ran_fpcf_td, \
                           start_ts, same_last_shit, random_decimal_number
                else:
                    return sensor_data
            else:
                return sensor_data, start_ts, o9_value, d3, device_data, doact


        except:
            traceback.print_exc()
            pass

    def get_database(self, task_number):

        print(
            f"[SIZEER] [TASK NUMBER {task_number}] [AKAMAI SOLVER] [{datetime.datetime.now()}]\t Fetching Device Data")
        # Provide the mongodb atlas url to connect python to mongodb using pymongo
        CONNECTION_STRING = ""

        # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
        client = MongoClient(CONNECTION_STRING)

        # Create the database for our example (we will use the same database throughout the tutorial
        db_name = client['collector']

        collection_name = db_name['rawsensors']

        item_details = collection_name.find()

        random_item = item_details[random.randint(0, 9795)]

        fmh = random_item['fmh']
        fmh_bytes = bytes(fmh, 'utf-8')
        fmh_hashed = hashlib.sha256(fmh_bytes).hexdigest()

        ssh_string = random_item['ssh']
        ssh_bytes = bytes(ssh_string, 'utf-8')
        ssh_hashed = hashlib.sha256(ssh_bytes).hexdigest()

        wv_wr = ',' + random_item['wv'] + ',' + random_item['wr'] + ','

        weh_list = random_item['weh']
        str_list = '['
        for item in weh_list:
            str_list += f'"{item}", '

        str_list = str_list[:-2] + ']'
        weh_bytes = bytes(str_list, 'utf-8')
        weh_hashed = hashlib.sha256(weh_bytes).hexdigest()

        wl = str(random_item['wl'])
        pixel_ratio = random_item['window']['devicePixelRatio']

        computed_string_challenge = f"{fmh_hashed},{pixel_ratio},{ssh_hashed}{wv_wr}{weh_hashed},{wl}"
        computed_string = f"{fmh_hashed},{pixel_ratio},0{wv_wr}{weh_hashed},{wl}"

        canvas = random.choice(random_item['rCanvas'])
        rval = canvas['rVal']
        rcfp = canvas['rCFP']

        user_agent = random_item['navigator']['userAgent']

        screen_info = random_item['screen']

        availHeight = screen_info['availHeight']
        availWidth = screen_info['availWidth']
        width = screen_info['width']
        height = screen_info['height']
        client_width = random_item['document']['clientWidth']
        client_height = random_item['document']['clientHeight']
        outerWidth = random_item['window']['outerWidth']

        bmak_mr = random_item['mr']

        fpcf_val_str = random_item['fpValstr']
        fpcf_val_str_and_ab = fpcf_val_str + '-1,2,-94,-80,' + str(Abck().ab(fpcf_val_str))

        device_data_dict = {
            'screen': {
                'availHeight': availHeight,
                'availWidth': availWidth,
                'width': width,
                'height': height,
                'clientWidth': client_width,
                'clientHeight': client_height,
                'outerWidth': outerWidth,
            },
            'mr': bmak_mr,
            'fpValstr': fpcf_val_str_and_ab,
            'user-agent': user_agent,
            'rVal': rval,
            'rCFP': rcfp,
            'device_info': {
                'challenge': computed_string_challenge,
                'normal': computed_string
            }
        }
        print(f"[SIZEER] [TASK NUMBER {task_number}] [AKAMAI SOLVER] [{datetime.datetime.now()}]\t "
              f"Succesfully Retrieved Device Data!")

        return device_data_dict



if __name__ == "__main__":
    #Akamai().get_database()

    abck = Abck()

    #Your starting timestamp
    #start_ts = int(time()*1000)

    #print(gd)

    ab = abck.ab("-1")
    #print(ab)
    # Output => 500

    # Sed function
    sed = abck.sed()
    #print(sed)
    # Output => 0,0,0,0,1,0,0

    # Fas function
    fas = abck.fas()
    #print(fas)
    # Output => 26067385

    # Np function
    np = abck.np()
    #print(np)
    # Output => 11133333331333333333

    # o9
    o9 = abck.calc_o9()
    #print(o9)
    # Output (Is diff each time genned) => 75155232

    #d3
    d3 = abck.calc_d3()
    #print(d3)
    # Output (Is diff each time genned) => 8350580

    #Akamai().bpd(abck_cookie='4A8C24CA1D93450F0052827478673C6F~0~YAAQlgoQArukg7F6AQAA0LSzVAY0eN5LF59vC2kV8gDriRpc2EPOU40yhs7zXFQIiJrLp8COksxwrkSBVXzneN1oFbpRO5CZOMOhDIaurPLHq6YyVqiaZIklRShC1Z81/2VyJiiUlX+F24VjJalmLszVlCQEgK+9cRY4YAB+C6GwGTmcejPjU4NriVlZu6HpaqkX/6uXpP3G1D8qLaM6vjy6b31P+4mdCw2tiVS3Cukwn1ah6Ed2kAOcLbyIDNWEaUGYb/ZVnyhJyEVP3DIRRY3ADq8/2j0J4/7Ug/Eq0RzuOA4E48msdSTlLNyy2CBGy6UOuNLgmCddLGfUgngdl+xmeLISTDN9e/hYvAuL2DqERpZCQoF/OWjHvNQgdFew+EHwYs+rp0f9zzF6Uz8wZo2aV6CjSNM=~-1~||1-RmFTKvpqij-1-10-1000-2||~-1'
    #             ,has_challenge=True, is_second_challenge=True)
