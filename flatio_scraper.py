'''
requests==2.27.1
beautifulsoup4==4.11.1
lxml==4.8.0
'''

'''This project was done to notify me by email if there are any good deals on flatio.co.uk
        for the time i would want to move in to the time i would like to move out in any given 
            city. I then will use Windows Task Scheduler to run this script once or twice a day with 
                my desired parameters.'''


# Emailing imports.
import os
import smtplib
from email.message import EmailMessage

# Flatio scraping imports.
import requests
from bs4 import BeautifulSoup
import re
from datetime import date
from typing import Optional

# Constants stored in the environment variables to prevent exposure of sensitive information.
GOOGLE_EMAIL_ADDRESS = os.environ.get("gmail_email")
GOOGLE_APP_PASSWORD = os.environ.get("Python (Google Accounts App Password)")
ICLOUD_EMAIL_ADDRESS = os.environ.get("icloud_email")


# The class of the scraper.
class Flatio:

    def __init__(self, city: str, move_in: str, move_out:str, convert_currency: Optional[str] = None) -> None:
        self.city = city
        self.move_in = move_in
        self.move_out = move_out
        self.convert_currency = convert_currency
        self.header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36"
        }

        # Formating the city name.
        if len(city.split()) >= 2:
            self.city = city.title().replace(' ', '_')
        else:
            self.city = city.title()
        
        # Formating the move in dates to 'YEAR-MONTH-DAY' from using different seperators.
        separators = ['-', '_', '.', '\\', '/']
        for separator in separators:
            if separator in move_in:
                year = int(move_in.split(separator)[0])
                month = int(move_in.split(separator)[1])
                day = int(move_in.split(separator)[2])
                self.move_in = date(year, month, day)

            if separator in move_out:
                year = int(move_out.split(separator)[0])
                month = int(move_out.split(separator)[1])
                day = int(move_out.split(separator)[2])
                self.move_out = date(year, month, day)

    def get_content(self):
        # Searching with the required parameters.
        r = requests.get(f"https://www.flatio.co.uk/s/{self.city}?f[from]={self.move_in}&f[to]={self.move_out}&f[order]=cheapest&f[fullApartment]=1&f[oneRoom]=1&f[twoRooms]=1", headers=self.header)
        return r.content

    def script_with_offers(self):
        # Extracting the script with the offer prices.
        soup = BeautifulSoup(self.get_content(), 'lxml')
        scripts = soup.find_all('script')
        offers = None

        for script in scripts:
            pattern = re.compile(r'var offers =')
            match = pattern.search(str(script))
            if match:
                offers = str(script)
                break
        
        return offers
    
    def price_list(self):
        # Creating a list of the prices.
        pattern = re.compile(r'"price":"\d{3,7}"')
        matches = pattern.findall(self.script_with_offers())
        price_list = []

        for match in matches:
            remove_before_number = str(match).partition(':"')[2]
            price = remove_before_number.partition('"')[0]
            price = " ".join([price,'GBP'])
            price_list.append(price)
        
        return price_list

    def converted_currency_price_list(self, to_currency: str) -> list:

        converted_price_list = []
        # Iterate over the prices in the list to convert all the prices to the desired currency.
        for price_GBP in self.price_list():
            
            price_GBP = price_GBP.split(" ")[0]

            source = requests.get(f'https://www.x-rates.com/calculator/?from=GBP&to={to_currency}&amount={price_GBP}', headers=self.header).text
            soup = BeautifulSoup(source, 'lxml')
            
            # Getting the preformatted price and currency.
            price_currency = soup.find("span", class_ = 'ccOutputRslt').text

            # Formatting the converted price-currency representation.
            price = price_currency.split(" ")[0]
            currency = price_currency.split(" ")[1]

            # Formatting the converted price to be more readable.
            if ',' in price:
                price = price.replace(",", "")
            price = round(float(price))
            price = f'{price:,d}'

            # The formatted price-currency representation.
            formated_price_currency = ' '.join([price, currency])

            converted_price_list.append(formated_price_currency)
        
        return converted_price_list



    def good_price_alert(self, max_price_limit):
        
        # Conditional to decide the working price list according to the optional argument convert_currency.
        if self.convert_currency:
            price_list = self.converted_currency_price_list(self.convert_currency)
        else:
            price_list = self.price_list()

        # Populating the list of good prices.
        good_prices = []

        for price in price_list:
            price = str(price)
            price_int = int(price.split(" ")[0].replace(",", ""))
            if price_int <= int(max_price_limit):
                good_prices.append(price)
        
        # Sending an email with the good prices if the good_prices list was populated.
        if good_prices:
            # Creating the message.
            msg = EmailMessage()
            msg['Subject'] = f"Found potential good deals in {self.city}!"
            msg['From'] = GOOGLE_EMAIL_ADDRESS
            msg["To"] = ICLOUD_EMAIL_ADDRESS
            msg.set_content(f"Here is a list of good prices in {self.city} moving in on '{self.move_in}' and moving out '{self.move_out}':\n{good_prices}")

            # Setting a SSL connection with Gmail.
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                # Logging in.
                smtp.login(GOOGLE_EMAIL_ADDRESS, GOOGLE_APP_PASSWORD)
                # Sending the message.
                smtp.send_message(msg)
        else:
            print("There were no offers that fall under the maximum price limit!")


if __name__ == "__main__":
    # Base requirements input.
    city = input("Please enter the name of the city you would like to stay in: ")
    move_in = input("Please enter the date you would like to move in (in the format of YEAR-MONTH-DAY): ")
    move_out = input("Please enter the date you would like to move out (in the format of YEAR-MONTH-DAY): ")
    if_currency_desired = input("Would you like to convert the prices from GBP to another currency? (Yes/No): ")

    # Conditional to check if the user would like to convert the GBP price to a differenct currency.
    if if_currency_desired.upper() == 'YES':
        desired_currency = input("What currency would you like to convert it to?: ")
        max_price = input("What maximum price limit would be considered a good price for you?: ")
        Flat = Flatio(city, move_in, move_out, desired_currency)
        Flat.good_price_alert(max_price)
    else:
        max_price = input("What maximum price limit would be considered a good price for you?: ")
        Flat = Flatio(city, move_in, move_out)
        Flat.good_price_alert(max_price)