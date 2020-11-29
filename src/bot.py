import random
import time
import warnings
import sys

warnings.filterwarnings("ignore")

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from loguru import logger

# from bs4 import BeautifulSoup
from . import settings
from .utils import loadUserAgents, getproxies, create_proxyauth_extension

logger.remove()
logger.add(
    "youtube_subscriber.log",
    enqueue=True,
    backtrace=True,
)
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time}</green> <level>{message}</level>",
    level="INFO",
)
# loading useragents
# calling shuffled user agents
UserAgents = loadUserAgents(settings.UAPATH)

# # calling shuffled proxies
proxies = getproxies(file_path=settings.PROXYPATH)  # (file_path=settings.PROXYPATH)

sigin_url = settings.SIGNIN

# opts.headless = settings.HEADLESS


def try_credentials(first_name, last_name, username, password):

    logger.info("Engined initiated!")

    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = True
    proxy = random.choice(proxies)
    p_proxy = proxy.split(":")
    logger.info("Using proxies!")
    if len(p_proxy) == 4:
        proxyauth_plugin_path = create_proxyauth_extension(
            proxy_host=p_proxy[0],
            proxy_port=p_proxy[1],
            proxy_username=p_proxy[2],
            proxy_password=p_proxy[3],
        )
        logger.info("viewing from ip {}", p_proxy[0])
        chrome_options.add_extension(proxyauth_plugin_path)
    else:
        if settings.SOCKS:
            chrome_options.add_argument("--proxy-server=socks5://%s" % proxy)
        else:
            chrome_options.add_argument("--proxy-server=%s" % proxy)

    logger.info("Initiating browser!")

    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
    )
    browser = webdriver.Chrome(
        executable_path="./drivers/chromedriver.exe", options=chrome_options
    )
    browser.maximize_window()
    # browser.minimize_window()

    # browser.set_window_position(0, 0)
    # browser.set_window_size(100, 500)

    try:
        logger.info("Launching URL!")
        browser.get(sigin_url)

        time.sleep(3)
        # google_elem = browser.find_element_by_xpath(
        #     '//*[@id="openid-buttons"]/button[1]'
        # )

        # google_elem.click()
        # time.sleep(5)
        logger.info("Authentication initiated!")

        browser.find_element_by_xpath('//input[@type="email"]').send_keys(username)
        time.sleep(3)

        browser.find_element_by_css_selector("#identifierNext > div > button").click()

        time.sleep(3)

        browser.find_element_by_xpath('//input[@type="password"]').send_keys(password)

        time.sleep(3)

        # try:
        #     try:
        #         browser.find_element_by_xpath('//*[@id="accept"]').click()
        #         time.sleep(5)
        #         browser.find_element_by_xpath('//*[@id="Password"]').send_keys(
        #             settings.TMP_PWD
        #         )
        #         time.sleep(5)

        #         browser.find_element_by_xpath('//*[@id="ConfirmPassword"]').send_keys(
        #             settings.TMP_PWD
        #         )
        #         time.sleep(5)
        #         browser.find_element_by_xpath("//*[@id='submit']").click()

        #     except Exception as e:
        #         logger.info("No need to accept: ", e)
        #         time.sleep(5)
        #         pwd1 = browser.find_elements_by_xpath('//input[@type="password"]')
        #         time.sleep(2)
        #         pwd1[0].send_keys(settings.TMP_PWD)

        #         time.sleep(5)
        #         browser.find_element_by_xpath(
        #             '//input[@name="ConfirmPasswd"]'
        #         ).send_keys(settings.TMP_PWD)
        #         time.sleep(5)
        #         browser.find_element_by_xpath(
        #             '//*[@id="changepasswordNext"]/div/button'
        #         ).click()

        #         time.sleep(5)

        # except Exception as e:
        #     logger.info("Failed on password change", e)
        #     pass
        # with open(settings.NEW_CRED, "a") as f:
        #     f.write(f"{username}:{settings.TMP_PWD}" + "\n")
        browser.find_element_by_xpath('//*[@id="passwordNext"]').click()
        logger.info("Authentication complete! waiting for next page")

        time.sleep(3)

        try:
            logger.info("Checking agreement page!")
            browser.find_element_by_xpath('//*[@id="accept"]').click()
            time.sleep(3)
        except:
            logger.info("No agreement page! moving on.")
            pass

        time.sleep(3)
        logger.info("Launching YouTube")
        browser.get("https://www.youtube.com/")

        host = browser.title
        logger.info("We are currently at {} page!", host)

        fail_cnt = 0
        is_failed = False if "youtube" in host.lower() else True

        while is_failed:
            logger.info("Youtube not loaded! loading.. .")
            browser.get("https://www.youtube.com/")
            time.sleep(2)
            fail_cnt += 1
            if fail_cnt >= 5:
                logger.error("You have an error {}", e)
                with open(settings.FAILED_CRED, "a") as f:
                    f.write(f"{first_name}:{last_name}:{username}:{password}" + "\n")
                browser.quit()

        time.sleep(2)
        logger.info("Everything is good! reloading the browser")

        browser.refresh()
        time.sleep(2)

        browser.find_element_by_xpath('//img[@id="img"]').click()
        time.sleep(2)
        logger.info("Find user's channel link")
        channel_link = browser.find_element_by_xpath('//paper-item[@role="link"]')
        channel_link.find_element_by_xpath('//yt-formatted-string[@id="label"]').click()

        time.sleep(2)

        if (
            not settings.UNSUBSCRIBE
            and not first_name.lower() in str(browser.title).lower()
        ):

            logger.info("Finding 'GET STARTED' button.. .")

            browser.find_element_by_xpath('//div[@id="next-button"]').click()

            logger.info("GET STARTED button clicked")

            time.sleep(2)

            select_button = browser.find_element_by_xpath(
                '//span[@id="personal-account-tile-select-button"]'
            ).click()
            # logger.info(select_button)
            time.sleep(5)
            while not "studio" in str(browser.title).lower():
                time.sleep(1)
            logger.info("User's channel created!")

        logger.info("Moving on to target channel!")
        browser.get(settings.TARGET_CHANNEL)
        time.sleep(5)

        # btn = browser.find_element_by_xpath('//yt-formatted-string[@id="text"]')

        # logger.info("BN", btn.text)
        # if str(btn.text).lower() == "subscribed":
        #     logger.info(f"{username} is already subscribed to {host.split(' ')[0]}!!")
        # else:
        browser.find_element_by_xpath('//*[@id="subscribe-button"]').click()
        logger.info("Subscribe button clicked!")

        time.sleep(2)

        if settings.UNSUBSCRIBE:
            try:
                unsubscribe_dialog = browser.find_element_by_xpath(
                    '//paper-dialog[@role="dialog"]'
                )
                browser.find_element_by_xpath(
                    '//yt-button-renderer[@id="confirm-button"]'
                ).click()
                logger.info("{} unsubscribed to {}!!", username, host.split(" ")[0])
            except Exception as e:
                logger.warning("Not subscribed: ", e)

        else:

            logger.info("{} subscribed to {}!!", username, host.split(" ")[0])

        time.sleep(2)
        button_contents = browser.find_elements_by_css_selector("#subscriber-count")
        num_subs = button_contents[0].text.split(" ")[0]

        logger.info("Total number of subscribers: {}", num_subs)
        time.sleep(1)

        browser.quit()

    except Exception as e:
        logger.error("You have an error {}", e)
        with open(settings.FAILED_CRED, "a") as f:
            f.write(f"{first_name}:{last_name}:{username}:{password}" + "\n")
        browser.quit()
        # pass


if __name__ == "__main__":
    failed_creds = []

    with open(settings.CRD_PATH, "r") as f:
        credentials = f.readlines()

        n_batch = len(credentials) * 0.5

        if type(n_batch) == float:
            import math

            tmp = math.floor(n_batch)
            logger.info("remaining: {} ", n_batch - tmp)
            n_batch = tmp

        batch_1 = credentials[:n_batch]
        batch_2 = credentials[n_batch:]

        for cred in credentials:
            first_name, last_name, username, password = cred.split(",")[:4]
            try_credentials(first_name, last_name, username, password)
    logger.info("Operation completed!!!")

    logger.info("Trying failed creds!")
    with open(settings.FAILED_CRED, "r") as f:
        for cred in f.readlines():
            first_name, last_name, username, password = cred.split(":")
            try_credentials(first_name, last_name, username, password)
