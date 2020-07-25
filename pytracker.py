from subprocess import Popen
import datetime
from bs4 import BeautifulSoup
import requests
from time import sleep
import smtplib
from params import HEADERS, URLS, EMAIL, PASSWORD, EMAIL2, Bcolors


def send_mail(url):
    print(f"{Bcolors.WARNING}Trying to send an email{Bcolors.ENDC}")
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(EMAIL, PASSWORD)
    subject = "Price fell down!"
    body = f"Check the amazon link {url}"
    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        EMAIL,
        EMAIL2,
        msg
    )
    print(f"{Bcolors.OKGREEN}EMAIL HAS BEEN SENT!{Bcolors.ENDC}")
    server.quit()


def title_handler(text):
    text = text.split(" ")
    new_title = ""
    for t in text:
        if len(new_title) + len(t) < 40:
            new_title = new_title + " " + t
        else:
            new_title = new_title + "..."
            return new_title.strip()
    return new_title.strip()


def check():
    for s in URLS:
        page = requests.get(s[0], headers=HEADERS)
        sleep(60)
        soup = BeautifulSoup(page.content, "html.parser")
        price = float(str(soup.find(id="newBuyBoxPrice").text).split("$")[1])
        title = str(soup.find(id='productTitle').text).strip()
        if price and title:
            print(f"{Bcolors.HEADER}{title_handler(title)}{Bcolors.ENDC}\n"
                  f"{Bcolors.OKBLUE}Date: {datetime.datetime.now()}{Bcolors.ENDC}"
                  f"{Bcolors.OKBLUE}\nCurrent price: {Bcolors.BOLD}${price}{Bcolors.ENDC}{Bcolors.ENDC}"
                  f"{Bcolors.OKBLUE} vs desirable price: {Bcolors.BOLD}${s[1]}{Bcolors.ENDC}{Bcolors.ENDC}"
                  f"{Bcolors.OKBLUE} \n{Bcolors.UNDERLINE}{s[0]}{Bcolors.ENDC}{Bcolors.ENDC}\n")
        if price <= s[1]:
            send_mail(s[0])


def run_script():
    while True:
        try:
            check()
        except AttributeError as e:
            print(f"{Bcolors.FAIL}{e}{Bcolors.ENDC}")
            print(f"{Bcolors.WARNING}Probably, you will need to reduce the number of requests to Amazon, "
                  f"in order not to be blocked as a bot.{Bcolors.ENDC}\n")
            sleep(30)
            continue
        sleep(3600)


if __name__ == "__main__":
    print(f"{Bcolors.OKGREEN}The program has been started!{Bcolors.ENDC}")
    while True:
        sleep(15)
        try:
            run_script()
        except Exception as e:
            print(f"{Bcolors.FAIL}The program is crashed!\n {e}{Bcolors.ENDC}")
        finally:
            print(f"{Bcolors.WARNING}Restarting...{Bcolors.ENDC}")
            p = Popen(f"python3 " + "pytracker.py", shell=True)
            p.wait()
