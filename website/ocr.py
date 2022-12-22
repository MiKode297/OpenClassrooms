"""Module."""

import os
import sys
from enum import Enum, auto
from typing import Optional

import logging
from datetime import date, datetime

# import unittest
# import pytest
from pathlib import Path

import requests

# import urllib.request
from urllib.parse import urljoin
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver

# from selenium.webdriver.firefox.service import Service as FirefoxService
# from selenium.webdriver.chrome.webdriver import WebDriver
# from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By

# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.common.exceptions import TimeoutException, NoSuchElementException


from . import Website

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(BASE_DIR)


# # Get an instance of a logger
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)

# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)

# # create formatter
# formatter = logging.Formatter("%(levelname)s - %(asctime)s - %(name)s - %(message)s")
# # add formatter to ch
# ch.setFormatter(formatter)

# logger.addHandler(ch)


LOCAL_FR = "fr"
LOCAL_EN = "en"
SEARCH_TIMEOUT_S = 7
DISABLE_TEST = True


# def create_webdriver():
#     """
#     Create browser webdriver
#     """

#     chromeOptions = Options()
#     chromeOptions.headless = True

#     # base = os.path.dirname(settings.BASE_DIR)
#     # with webdriver.Chrome(executable_path=os.path.join(base, 'chromedriver.exe')) as driver:
#     browser = webdriver.Chrome(executable_path='/home/travis/virtualenv/python3.8/bin/chromedriver', options=chromeOptions)
#     browser.get("http://linuxhint.com")
#     print("Title: %s" % browser.title)
#     # browser.quit()
#     # browser.implicitly_wait(10)
#     # time.sleep(1)

#     return browser


class OpenClassrooms(Website):
    """Self-explanatory"""

    URL_BASE = "https://openclassrooms.com"
    SEARCH_URI = "fr/search?page="

    TIMEOUT_DEFAULT_S = 12

    def __init__(self, base_url: str = URL_BASE) -> None:

        super().__init__(base_url)
        self.post_lst = []
        self.driver = None
        self.title = ""

    def get_posts(self, page_start_idx: int = 0, n_page_max: int = 0) -> None:
        """
        Get all website articles/posts.

        Args:
            page_start_idx: . Defaults to 0.
            n_page_max: . Defaults to 0.
        """
        # Init. webdriver
        # driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        driver = webdriver.Firefox()
        driver.implicitly_wait(self.TIMEOUT_DEFAULT_S)

        driver.get(self.base_url)
        self.title = driver.title
        print(self.title)

        if page_start_idx < 0:
            page_start_idx = 0

        page_idx = page_start_idx
        post_idx = 1
        enable = True

        while enable:

            # Get posts from page
            # url_cur = __build_url(uri=SEARCH_URL + str(page_idx))
            search_url = f"{self.base_url}/{self.SEARCH_URI}{page_idx}"

            driver.get(search_url)
            # handle = driver.current_window_handle
            # print(f"Handle: {handle}, Title: {driver.title}, URL: {driver.current_url}")

            ul_el = WebDriverWait(driver, timeout=self.TIMEOUT_DEFAULT_S).until(
                lambda d: d.find_element(
                    By.XPATH,
                    "//div[@id='mainSearchLegacy']/div[1]/div[1]/div[1]/ul[1]",
                )
            )

            post_lst = ul_el.find_elements(
                By.XPATH,
                ".//child::li",
            )

            # Get list of paths / courses
            for idx, post in enumerate(post_lst):
                print(f"Idx: {post_idx}, p{page_idx}.{idx+1}")
                print("post:", post)

                link = None
                try:
                    link = post.find_element(By.TAG_NAME, "a")
                except NoSuchElementException:
                    pass

                # Get post details
                if link:

                    url = link.get_attribute("href")
                    element_lst = url.split("/")
                    content_type = element_lst[-2]
                    content = element_lst[-1].split("-", 1)
                    content_id = content[0]
                    content_label = content[1]
                    print(
                        f"Content URL: {url}, Type: {content_type}, ID: {content_id}, label: {content_label}"
                    )

                #             # block_type = link.find_element_by_xpath('//self::div[1]')
                #             div_cur = link.find_element(By.XPATH, "./div")
                #             # print('First div', div_cur.get_attribute('class'))

                #             figure = div_cur.find_element(By.TAG_NAME, "figure")
                #             figure_url = figure.get_attribute("style")
                #             print("Figure URL", figure_url)

                #             # block_type = div_cur.find_element_by_xpath('//span[contains(@class, MuiTypography-root)]')
                #             block_type = div_cur.find_element(By.XPATH, "./div/span")
                #             content_type_lst = block_type.text.split(" - ")
                #             content_category = content_type_lst[0].lower()
                #             logger.debug("Category: {}".format(content_category))

                #             title = div_cur.find_element(By.XPATH, "./div/h6")
                #             content_title = title.text
                #             print("Title", content_title)

                #             if content_type == "paths":
                #                 desc = div_cur.find_element(By.XPATH, "./div/div[2]")
                #                 content_description = desc.text
                #                 print("Description", content_description)

                #             # content_lst.append(
                #             #     {
                #             #         "url": url,
                #             #         "type": content_type,
                #             #         "category": content_category,
                #             #         "identifier": content_id,
                #             #         "label": content_label,
                #             #         "title": content_title,
                #             #         "description": content_description,
                #             #         # "figure_url": figure_url,
                #             #     }
                #             # )

                self.post_lst.append((content_type, content_id, content_label))
                post_idx += 1

            page_idx += 1

            # check page empty or max page reached
            if not post_lst or (
                n_page_max > 0 and (page_idx - page_start_idx) >= n_page_max
            ):
                enable = False

        driver.quit()


class WebsitePost(Website):
    """Web site post."""

    class PostType(Enum):
        """Self-explanatory"""

        COURSE = auto()
        PATH = auto()

    def __init__(self, uri: str = "", parent: Optional[OpenClassrooms] = None) -> None:

        super().__init__()

        self.parent = parent
        self.uri = uri
        self.identifier = ""
        self.type = None
        self.theme = ""
        self.title = ""
        self.level = ""
        self.period = ""
        self.period_unit = ""
        self.description = ""
        self.category = ""


class Path(WebsitePost):
    """Web site post."""

    def __init__(self, base_url: str = "") -> None:
        super().__init__(base_url)
        self.website = base_url


class Course(WebsitePost):
    """Web site post."""

    def __init__(self, base_url: str = "") -> None:
        super().__init__(base_url)
        self.website = base_url


def import_source_content_dependency(driver, content_url):

    dependency_dct = {"objective_lst": [], "dependency_lst": []}

    logger.debug("update data for url {}".format(content_url))

    driver.get(content_url)
    handle = driver.current_window_handle
    logger.debug(
        "Handle: {}, Title: {}, URL: {}".format(
            handle, driver.title, driver.current_url
        )
    )

    # Get list of paths / courses
    asides = WebDriverWait(driver, timeout=SEARCH_TIMEOUT_S).until(
        lambda d: d.find_elements_by_tag_name("aside")
    )

    for aside_item in asides:

        attribute_item = aside_item.get_attribute("data-claire-semantic")
        if attribute_item:

            if "information" in attribute_item:

                items = aside_item.find_elements_by_tag_name("li")
                for item_idx, item in enumerate(items):
                    txt = item.find_element_by_tag_name("p").text.rstrip(" .,;")
                    logger.debug("Objective #{}: {}".format(item_idx, txt))
                    dependency_dct["objective_lst"].append(txt)

                __get_content_dependency(content_url, aside_item, dependency_dct)
                # logger.debug(dependency_dct)

            if "warning" in attribute_item:

                __get_content_dependency(content_url, aside_item, dependency_dct)
                # logger.debug(dependency_dct)

    return dependency_dct


def __get_content_dependency(content_url, element, dependency_dct):

    links = element.find_elements_by_tag_name("a")
    if not links:
        logger.debug("No link in block")

    for dependency_idx, dependency_lnk in enumerate(links):

        dependency_url = dependency_lnk.get_attribute("href")
        logger.debug("Dependency URL #{} - {}".format(dependency_idx, dependency_url))

        if dependency_url.startswith(BASE_URL):

            resp = requests.get(dependency_url, allow_redirects=True)
            try:
                resp.raise_for_status()
            except:
                logger.error("Request GET: {}".format(resp.reason))
            else:
                resp_url = resp.url
                logger.debug("Dependency URL Redirected: {}".format(resp_url))

                if resp_url.startswith(__build_url(uri="courses")):

                    # Check archived [TODO]: get archived element, save into db
                    uri_last_elt = resp_url.split("/")[-1]
                    if "archived-source" in uri_last_elt:

                        url_el_lst = uri_last_elt.split("=")
                        archived_content_id = url_el_lst[-1]

                        archived_url = __build_url(uri="courses/" + archived_content_id)
                        logger.warning("Archive: {}".format(archived_url))
                        # resp = requests.get(archived_url, allow_redirects=True)
                        # resp.raise_for_status()
                        # archived_url = resp.url
                        # logger.debug("Archive redirected: {}".format(archived_url))

                        #     content_id_tup = __get_content_id(archived_url)
                        #     logger.debug("Archived content ID: {}".format(content_id_tup))

                        #     if content_id_tup:
                        #         dependency_dct["dependency_lst"].append(content_id_tup)
                        #         logger.debug(
                        #             "Dependency #{} - {}".format(dependency_idx, content_id_tup)
                        #         )

                        logger.debug("URL last part {}".format(uri_last_elt))
                        url_el_lst = uri_last_elt.split("?")
                        resp_url = resp_url.replace("?" + url_el_lst[-1], "")
                        logger.debug("Dependency URL cleaned: {}".format(resp_url))

                    content_id_tup = __get_content_id(resp_url)
                    logger.debug("Content ID: {}".format(content_id_tup))

                    if (
                        content_id_tup
                        and content_id_tup not in dependency_dct["dependency_lst"]
                        and content_id_tup[0] not in content_url
                    ):
                        dependency_dct["dependency_lst"].append(content_id_tup)
                        logger.debug(
                            "Add Dependency #{} - {}".format(
                                dependency_idx, content_id_tup
                            )
                        )
                else:
                    logger.warning(
                        "Internal URL not for dependency: {}".format(resp_url)
                    )

        else:
            logger.warning("External URL for dependency: {}".format(dependency_url))

    # items = element.find_elements_by_tag_name('li')
    # for item in items:
    #     link = item.find_element_by_tag_name('a')
    #     if link:
    #         content_uri = link.get_attribute('href')
    #         print(content_uri)


def __get_content_id(url):

    content_id_tup = ()

    # logger.debug("URL: {}".format(url))

    # content_uri = url.removeprefix(__build_url())     # [TODO]: Introduced with Python 3.9
    content_uri = url[len(__build_url()) + 1 :]
    # logger.debug("Content URI: {}".format(content_uri))

    uri_el_lst = content_uri.split("/")
    # logger.debug("URI elts: {}".format(uri_el_lst))

    content_type = uri_el_lst[0]
    # logger.debug("Content type: {}".format(content_type))

    content = uri_el_lst[1].split("-")
    content_id = content.pop(0)
    # content_label = "_".join(content)
    content_label = uri_el_lst[1].replace(content_id + "-", "")
    # logger.debug("Content ID: {}, Label: {}".format(content_id, content_label))

    if content_type == "courses":
        content_id_tup = (content_id, content_label)

    # elif content_type == "paths":
    #     logger.info("Path ID: {}, Label: {}".format(content_id, content_label))

    else:
        logger.error(
            "Bad content type ID: {}, Label: {}".format(content_id, content_label)
        )

    return content_id_tup


def __build_url(local=LOCAL_FR, uri=""):

    # url = urljoin(BASE_URL, local, uri)
    url = "/".join([BASE_URL, local])
    if uri:
        url = "/".join([url, uri])
        logger.debug("Build URL: {}".format(url))

    return url


if __name__ == "__main__":

    #     user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36"

    #     ua = UserAgent()
    #     user_agent = str(ua.chrome)
    #     print(ua.chrome)

    #     user_agent = str(ua.firefox)
    #     print(ua.firefox)

    #     # header variable
    #     headers = {"User-Agent": user_agent}
    #     print(headers)

    #     payload = "{}"
    #     response = requests.get(url_cur, headers=headers)
    #     print(response)

    #     # response = requests.request("GET", url_cur, data=payload)
    #     # response = requests.get(url_cur, headers=headers, data=payload)
    #     print(response.url)
    #     print(response.headers)
    #     print(response.status_code)
    #     # print(response.text)
    #     # print(response.json())

    #     html_doc = response.text
    #     soup = BeautifulSoup(html_doc, "html.parser")  # html.parser / html5lib
    #     # print(soup.prettify())
    #     # print(soup.get_text())

    #     with requests.Session() as session:
    #         response = session.get(url_cur, headers=headers)

    #     # response = urllib.request.urlopen(url_cur, headers=headers)
    #     # req = urllib.request.Request(
    #     #                     url_cur,
    #     #                     data=None
    #     #                 )
    #     # response = urllib.request.urlopen(req)
    #     # page = response.read().decode('utf-8')
    #     # print(page)

    #     html_doc = response.text
    #     soup = BeautifulSoup(html_doc, "html.parser")  # html.parser / html5lib
    #     # print(soup.prettify())
    #     # print(soup.get_text())

    #     if True:

    #         # with webdriver.Chrome(executable_path=os.path.join(BASE_DIR, 'chromedriver.exe')) as driver:
    #         with WebDriver() as driver:

    #             TIMEOUT = 32

    #             # driver.get("https://google.com/ncr")
    #             # driver.find_element(By.NAME, "q").send_keys("cheese" + Keys.RETURN)
    #             # first_result = wait.until(presence_of_element_located((By.CSS_SELECTOR, "h3>div")))
    #             # print(first_result.get_attribute("textContent"))

    #             course_idx = 1
    #             # while loop [TODO]
    #             for page_idx in range(1, 50 + 1):

    #                 url_cur = url_search_base + str(page_idx)
    #                 driver.get(url_cur)
    #                 handle = driver.current_window_handle
    #                 print(handle, driver.title, driver.current_url)

    #                 if page_idx == 1:

    #                     # Go to Trust iframe
    #                     # popup = WebDriverWait(driver, timeout=TIMEOUT).until(lambda d: d.find_element_by_xpath("//div[starts-with(@id,'pop-div')]"))
    #                     popup_div = WebDriverWait(driver, timeout=TIMEOUT).until(
    #                         lambda d: d.find_element_by_class_name(
    #                             "truste_box_overlay_inner"
    #                         )
    #                     )

    #                     frame = popup_div.find_element_by_tag_name("iframe")
    #                     frame_id = frame.get_attribute("id")
    #                     driver.switch_to.frame(frame)
    #                     # driver.switch_to.frame(frame_id)

    #                     handle = driver.current_window_handle
    #                     print(driver.title, handle)

    #                     # Click on accept
    #                     # popup = WebDriverWait(driver, timeout=TIMEOUT).until(lambda d: d.find_element_by_class_name("pdynamicbutton"))
    #                     div = WebDriverWait(driver, timeout=TIMEOUT).until(
    #                         lambda d: d.find_element_by_class_name("pdynamicbutton")
    #                     )
    #                     el = div.find_element_by_class_name("call")
    #                     el.click()
    #                     print("Click")

    #                     # Go back to default window
    #                     handle = driver.current_window_handle
    #                     print(driver.title, handle)

    #                     # driver.switch_to.window(handle)
    #                     driver.switch_to.default_content()

    #                     driver.refresh()
    #                     handle = driver.current_window_handle
    #                     print(driver.title, handle)

    #                     handle = driver.current_window_handle
    #                     print(driver.title, handle)

    #                 # Get list of paths / courses
    #                 div = WebDriverWait(driver, timeout=TIMEOUT).until(
    #                     lambda d: d.find_element_by_id("mainSearchLegacy")
    #                 )
    #                 # ul_el = WebDriverWait(div, timeout=TIMEOUT).until(lambda d: d.find_element_by_css_selector('.members-holder ul li.invitation-holder'))
    #                 # ul_el = WebDriverWait(div, timeout=TIMEOUT).until(lambda d: d.find_element_by_xpath("//div[@class='grid-wrapper']"))
    #                 # ul_el = WebDriverWait(div, timeout=TIMEOUT).until(lambda d: d.find_element_by_xpath("/div[1]"))
    #                 ul_el = WebDriverWait(driver, timeout=TIMEOUT).until(
    #                     lambda d: d.find_element_by_xpath(
    #                         "//div[@id='mainSearchLegacy']/div[1]/div[1]/div[1]/ul[1]"
    #                     )
    #                 )
    #                 # ul_el = WebDriverWait(div, timeout=TIMEOUT).until(lambda d: d.find_elements_by_class_name("jss361"))
    #                 # ul_el = WebDriverWait(div, timeout=TIMEOUT).until(lambda d: d.find_element_by_tag_name("div"))
    #                 print(ul_el.get_attribute("class"))
    #                 # ul_el = WebDriverWait(ul_el, timeout=TIMEOUT).until(lambda d: d.find_element_by_tag_name("div"))
    #                 # print(ul_el.get_attribute('class'))
    #                 # ul_el = WebDriverWait(ul_el, timeout=TIMEOUT).until(lambda d: d.find_element_by_tag_name("div"))
    #                 # print(ul_el.get_attribute('class'))
    #                 # ul_el = WebDriverWait(ul_el, timeout=TIMEOUT).until(lambda d: d.find_element_by_tag_name("ul"))
    #                 # print('ul', ul_el.get_attribute('class'))
    #                 # block_lst = WebDriverWait(ul_el, timeout=TIMEOUT).until(lambda d: d.find_elements_by_tag_name('a'))
    #                 # print(block_lst.get_attribute('class'))
    #                 # block_lst = WebDriverWait(ul_el, timeout=TIMEOUT).until(lambda d: d.find_elements_by_class_name("MuiPaper-root MuiPaper-elevation1 MuiCard-root jss362 jss431 MuiPaper-rounded"))
    #                 # block_lst = WebDriverWait(ul_el, timeout=TIMEOUT).until(lambda d: d.find_element_by_xpath("/div[1]"))
    #                 block_lst = WebDriverWait(driver, timeout=TIMEOUT).until(
    #                     lambda d: d.find_elements_by_xpath(
    #                         "//div[@id='mainSearchLegacy']/div[1]/div[1]/div[1]/ul[1]//child::li"
    #                     )
    #                 )
    #                 # print(block_lst.get_attribute('class'))
    #                 # print(block_lst.get_attribute('class'), len(block_lst))
    #                 print(len(block_lst))

    #                 for idx, item in enumerate(block_lst):

    #                     is_available = True
    #                     try:
    #                         link = item.find_element_by_tag_name("a")
    #                         url = link.get_attribute("href")
    #                         print("url", url)
    #                     except:
    #                         is_available = False

    #                     if is_available:

    #                         print("Course:", page_idx, "-", idx, course_idx)
    #                         # block_type = link.find_element_by_xpath('//self::div[1]')
    #                         div_cur = link.find_element_by_xpath("./div")
    #                         # print('First div', div_cur.get_attribute('class'))

    #                         figure = div_cur.find_element_by_tag_name("figure")
    #                         print("Figure URL", figure.get_attribute("style"))

    #                         # block_type = div_cur.find_element_by_xpath('//span[contains(@class, MuiTypography-root)]')
    #                         block_type = div_cur.find_element_by_xpath("./div/span")
    #                         print("Type", block_type.text)

    #                         # title = item.find_element_by_tag_name('h6').text
    #                         title = div_cur.find_element_by_xpath("./div/h6")
    #                         print("Title", title.text)

    #                         desc = div_cur.find_element_by_xpath("./div/div[2]")
    #                         print("Description", desc.text)

    #                     else:
    #                         print("Course Not Available:", page_idx, "-", idx, course_idx)

    #                     course_idx += 1

    # #             # el_lst = WebDriverWait(driver, timeout=TIMEOUT).until(lambda d: d.find_elements_by_xpath("//div[@id='mainSearchLegacy')]//ul[@class='jss361']"))
    # #             lab_lnk = WebDriverWait(driver, timeout=TIMEOUT).until(lambda d: d.find_elements_by_css_selector("div#mainSearchLegacy>ul[class='jss361']"))
    # #             # for el in lab_lnk:
    # #             #     print(el)
    # #             lst = WebDriverWait(el_lst, timeout=TIMEOUT).until(lambda d: d.find_elements_by_tag_name("li"))
    # #             print(el_lst)
    # #             print(lst)

    # #             # wait = WebDriverWait(driver, 23)
    # #             handle = driver.current_window_handle

    # #             handles = driver.window_handles
    # #             print(handles)
    # #             print(driver.title)

    # #             url_cur = driver.current_url
    # #             print(url_cur)

    # #             lab_lnk = WebDriverWait(driver, timeout=TIMEOUT).until(lambda d: d.find_elements_by_css_selector('h6.MuiTypography-root jss498 MuiTypography-h6 MuiTypography-displayBlock'))

    # #             lab_lnk = WebDriverWait(driver, timeout=TIMEOUT).until(lambda d: d.find_element_by_id('pop-div203853870508980163'))
    # #             lab_lnk = WebDriverWait(driver, timeout=TIMEOUT).until(lambda d: d.find_element_by_css_selector('a.call'))
    # #             lab_lnk.click()

    # #             # first_result = wait.until(presence_of_element_located((By.CSS_SELECTOR, "call")))
    # #             masthead = driver.find_element_by_class_name('MuiTypography-root')

    # #             print(masthead)

    # #             # <h6 class="MuiTypography-root jss498 MuiTypography-h6 MuiTypography-displayBlock">Apprenez à programmer en Actionscript 3</h6>

    # # # div.MuiPaper-elevation1:nth-child(2)
    # # # html.js.supports.no-touchevents.cssfilters body.oc-body div#mainSearchLegacy.mainSearch div.grid-wrapper div.grid-inner div.jss340 ul.jss359 div.MuiPaper-root.MuiPaper-elevation1.MuiCard-root.jss360.jss429.MuiPaper-rounded
    # # # /html/body/div[4]/div/div/div/ul[1]/div[2]

    # # # div.MuiPaper-elevation1:nth-child(2) > div:nth-child(1) > li:nth-child(1) > a:nth-child(1) > div:nth-child(1) > div:nth-child(2) > h6:nth-child(2)
    # # # html.js.supports.no-touchevents.cssfilters body.oc-body div#mainSearchLegacy.mainSearch div.grid-wrapper div.grid-inner div.jss340 ul.jss359 div.MuiPaper-root.MuiPaper-elevation1.MuiCard-root.jss360.jss429.MuiPaper-rounded div.MuiCardContent-root.jss431.jss428.jss418 li.jss433 a.jss442 div.jss435.jss420.jss436.jss419.jss421 div.jss441.jss417 h6.MuiTypography-root.jss439.MuiTypography-h6.MuiTypography-displayBlock
    # # # /html/body/div[4]/div/div/div/ul[1]/div[2]/div/li/a/div/div[2]/h6

    # # # #pop-div203853870508980163

    # #             # alert = wait.until(EC.alert_is_present())
    # #             # alert = driver.switch_to.alert

    # #             # # Store the alert text in a variable
    # #             # text = alert.text

    # #             # # Press the Cancel button
    # #             # alert.dismiss()

    # #             # alert.accept()

    # #             first_result = wait.until(presence_of_element_located((By.CSS_SELECTOR, "MuiCardContent-root")))

    # #             elemnt = driver.find_element_by_css_selector('li')
    # #             print(elemnt)
    # #             print(elemnt.get_attribute("textContent"))

    # #             # first_result = wait.until(presence_of_element_located((By.CSS_SELECTOR, "h3>div")))
    # #             # print(first_result.get_attribute("textContent"))

    pass
