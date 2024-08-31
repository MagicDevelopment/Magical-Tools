import requests
import json
import os
from datetime import datetime, timezone
from colorama import Fore, Style, init

languages = {
    'da'    : 'Danish, Denmark',
    'de'    : 'German, Germany',
    'en-GB' : 'English, United Kingdom',
    'en-US' : 'English, United States',
    'es-ES' : 'Spanish, Spain',
    'fr'    : 'French, France',
    'hr'    : 'Croatian, Croatia',
    'lt'    : 'Lithuanian, Lithuania',
    'hu'    : 'Hungarian, Hungary',
    'nl'    : 'Dutch, Netherlands',
    'no'    : 'Norwegian, Norway',
    'pl'    : 'Polish, Poland',
    'pt-BR' : 'Portuguese, Brazilian, Brazil',
    'ro'    : 'Romanian, Romania',
    'fi'    : 'Finnish, Finland',
    'sv-SE' : 'Swedish, Sweden',
    'vi'    : 'Vietnamese, Vietnam',
    'tr'    : 'Turkish, Turkey',
    'cs'    : 'Czech, Czechia, Czech Republic',
    'el'    : 'Greek, Greece',
    'bg'    : 'Bulgarian, Bulgaria',
    'ru'    : 'Russian, Russia',
    'uk'    : 'Ukrainian, Ukraine',
    'th'    : 'Thai, Thailand',
    'zh-CN' : 'Chinese, China',
    'ja'    : 'Japanese',
    'zh-TW' : 'Chinese, Taiwan',
    'ko'    : 'Korean, Korea'
}

cc_digits = {
    'american express': '3',
    'visa': '4',
    'mastercard': '5'
}

def gradient_purple(step, total_steps):
    base_r, base_g, base_b = 186, 85, 211  
    factor = 1 - (step / total_steps)  
    r = int(base_r * factor)
    g = int(base_g * factor)
    b = int(base_b * factor)
    return f'\033[38;2;{r};{g};{b}m'

total_lines = 9
purple_intense = '\033[38;2;164;106;232m'
purple_dust = '\033[38;2;181;111;206m'
highlight = '\033[38;2;255;223;0m'

def print_ascii_art():
    pc_username = os.getlogin()
    width = os.get_terminal_size().columns
    art = f"""
{gradient_purple(0, total_lines)}{' ' * ((width - 48) // 2)} ███▄ ▄███▓    ▄▄▄           ▄████     ██▓    ▄████▄      ▄▄▄          ██▓
{gradient_purple(1, total_lines)}{' ' * ((width - 48) // 2)}▓██▒▀█▀ ██▒   ▒████▄        ██▒ ▀█▒   ▓██▒   ▒██▀ ▀█     ▒████▄       ▓██▒     ├─────────────
{gradient_purple(2, total_lines)}{' ' * ((width - 48) // 2)}▓██    ▓██░   ▒██  ▀█▄     ▒██░▄▄▄░   ▒██▒   ▒▓█    ▄    ▒██  ▀█▄     ▒██░     │ Running on:
{gradient_purple(3, total_lines)}{' ' * ((width - 48) // 2)}▒██    ▒██    ░██▄▄▄▄██    ░▓█  ██▓   ░██░   ▒▓▓▄ ▄██▒   ░██▄▄▄▄██    ▒██░     │ {pc_username}’s PC
{gradient_purple(4, total_lines)}{' ' * ((width - 48) // 2)}▒██▒   ░██▒    ▓█   ▓██▒   ░▒▓███▀▒   ░██░   ▒ ▓███▀ ░    ▓█   ▓██▒   ░██████▒ ├─────────────
{gradient_purple(5, total_lines)}{' ' * ((width - 48) // 2)}░ ▒░   ░  ░    ▒▒   ▓▒█░    ░▒   ▒    ░▓     ░ ░▒ ▒  ░    ▒▒   ▓▒█░   ░ ▒░▓  ░ │ Discord link:
{gradient_purple(6, total_lines)}{' ' * ((width - 48) // 2)}░  ░      ░     ▒   ▒▒ ░     ░   ░     ▒ ░     ░  ▒        ▒   ▒▒ ░   ░ ░ ▒  ░ │ dsc.gg/magicservices
{gradient_purple(7, total_lines)}{' ' * ((width - 48) // 2)}░      ░        ░   ▒      ░ ░   ░     ▒ ░   ░             ░   ▒        ░ ░
{gradient_purple(8, total_lines)}{' ' * ((width - 48) // 2)}       ░            ░  ░         ░     ░     ░ ░               ░  ░       ░  ░
{Style.RESET_ALL}{' ' * ((width - 48) // 2)}
    """
    print(art)

def get_discord_info(token):
    try:
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }

        res = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers)

        if res.status_code == 200:  
            res_json = res.json()

            user_name = f'{res_json["username"]}#{res_json["discriminator"]}'
            user_id = res_json['id']
            avatar_id = res_json['avatar']
            avatar_url = f'https://cdn.discordapp.com/avatars/{user_id}/{avatar_id}.gif'
            phone_number = res_json['phone']
            email = res_json['email']
            mfa_enabled = res_json['mfa_enabled']
            flags = res_json['flags']
            locale = res_json['locale']
            verified = res_json['verified']
            
            language = languages.get(locale)

            timestamp = ((int(user_id) >> 22) + 1420070400000) / 1000
            creation_date = datetime.fromtimestamp(timestamp, timezone.utc).strftime('%d-%m-%Y %H:%M:%S UTC')

            has_nitro = False
            res = requests.get('https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers=headers)
            nitro_data = res.json()
            has_nitro = bool(len(nitro_data) > 0)
            if has_nitro:
                d1 = datetime.strptime(nitro_data[0]["current_period_end"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                d2 = datetime.strptime(nitro_data[0]["current_period_start"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                days_left = abs((d2 - d1).days)

            billing_info = []
            for x in requests.get('https://discordapp.com/api/v6/users/@me/billing/payment-sources', headers=headers).json():
                y = x['billing_address']
                name = y['name']
                address_1 = y['line_1']
                address_2 = y['line_2']
                city = y['city']
                postal_code = y['postal_code']
                state = y['state']
                country = y['country']

                if x['type'] == 1:
                    cc_brand = x['brand']
                    cc_first = cc_digits.get(cc_brand)
                    cc_last = x['last_4']
                    cc_month = str(x['expires_month'])
                    cc_year = str(x['expires_year'])
                    
                    data = {
                        'Payment Type': 'Credit Card',
                        'Valid': not x['invalid'],
                        'CC Holder Name': name,
                        'CC Brand': cc_brand.title(),
                        'CC Number': ''.join(z if (i + 1) % 2 else z + '*' for i, z in enumerate(cc_first + '****' + cc_last)),
                        'CC Expiry': f'{cc_month}/{cc_year}',
                        'Address 1': address_1,
                        'Address 2': address_2 if address_2 else '',
                        'City': city,
                        'Postal Code': postal_code,
                        'State': state,
                        'Country': country
                    }
                    billing_info.append(data)

                elif x['type'] == 2:
                    billing_info.append({
                        'Payment Type': 'PayPal',
                        'Valid': not x['invalid'],
                        'PayPal Email': x['email'],
                        'Country': x['country']
                    })
    except Exception as e:
        print(f"Error: {e}")
        return None

    print(f"{highlight}Discord Info{Style.RESET_ALL}")
    print(f"{purple_dust}💻 User Name: {user_name}")
    print(f"{purple_dust}🆔 User ID: {user_id}")
    print(f"{purple_dust}🖼  Avatar URL: {avatar_url}")
    print(f"{purple_dust}📞 Phone Number: {phone_number}")
    print(f"{purple_dust}📧 Email: {email}")
    print(f"{purple_dust}🔐 MFA Enabled: {mfa_enabled}")
    print(f"{purple_dust}🎌 Flags: {flags}")
    print(f"{purple_dust}🌍 Locale: {language}")
    print(f"{purple_dust}✅ Verified: {verified}")
    print(f"{purple_dust}📅 Creation Date: {creation_date}")
    
    if has_nitro:
        print(f"{purple_dust}🚀 Nitro Subscription: {days_left} days left")
    else:
        print(f"{purple_dust}🚀 Nitro Subscription: Not subscribed")
    
    if billing_info:
        for info in billing_info:
            print(f"{purple_dust}💳 Payment Info: {info['Payment Type']}")
            for key, value in info.items():
                if key != 'Payment Type':
                    print(f"{purple_dust}  {key}: {value}")

def main():
    init()
    print_ascii_art()
    
    token = input(f"{highlight}Enter Discord Token: {Style.RESET_ALL}")
    print(f"{highlight}Fetching information...{Style.RESET_ALL}")
    
    get_discord_info(token)
    
    input(f"\n{highlight}Press Enter to exit...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
