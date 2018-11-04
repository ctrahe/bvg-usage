import imaplib
import email
import re
import getpass
from datetime import datetime

FROM_EMAIL = input('Email: ')
FROM_PWD = getpass.getpass('Password: ')
BVG_MAIL_DIRECTORY = 'BVG'
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993


class BvgTicketOverview():

    def __init__(self):
        self.mail = self.initialize_email_client()
        mail_ids = self.get_emails_from_directory(BVG_MAIL_DIRECTORY)
        ticket_details = self.parse_bvg_emails(mail_ids)
        print(ticket_details)

    def initialize_email_client(self):
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL, FROM_PWD)
        return mail

    def get_emails_from_directory(self, dir):
        self.mail.select(dir)
        typ, data = self.mail.search(None, 'ALL')
        return data[0].split()

    def parse_bvg_emails(self, mail_ids):
        try:
            bvg_ticket_details = {}
            for id in mail_ids:
                typ, data = self.mail.fetch(id, '(RFC822)' )
                for response_part in data:
                    try:
                        message = str(email.message_from_string(str(response_part[1])))
                        date = self.get_bvg_ticket_date(message)
                        price = self.get_bvg_ticket_price(message)
                        if date in bvg_ticket_details:
                            bvg_ticket_details[date] = str(float(bvg_ticket_details[date]) + float(price))
                        else:
                            bvg_ticket_details[date] = price
                    except Exception as e:
                        pass # response_part not always tuple
            return bvg_ticket_details

        except Exception as e:
            print("Error: {}".format(str(e)))

    def get_bvg_ticket_date(self, message):
        valid_date_patterns = ['Date:(.+?)\+']
        date = self.match_pattern(valid_date_patterns, message)
        if date:
            return self.format_date(date, ' %a, %d %b %Y %H:%M:%S ', '%d/%m/%y')

    def get_bvg_ticket_price(self, message):
        valid_price_patterns = ['Gesamtpreis:(.+?)=', 'Order total: =E2=82=AC(.+?)=', 'Total: =E2=82=AC(.+?)=']
        price = self.match_pattern(valid_price_patterns, message)
        if price:
            return self.normalise_price(price)

    def match_pattern(self, valid_patterns, string):
        for pattern in valid_patterns:
            try:
                match = re.search(pattern, string)
                if match:
                    return match.group(1)
            except AttributeError:
                pass    
        if not match:
            print("No match for '{}' in {}".format(pattern, string))
        pass

    def normalise_price(self, price):
        return price.replace(',', '.')

    def format_date(self, date, format, output):
        return datetime.strptime(date, format).strftime(output)

BvgTicketOverview = BvgTicketOverview()
