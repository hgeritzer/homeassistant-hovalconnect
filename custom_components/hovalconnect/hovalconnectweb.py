"""
"""
import logging
from pprint import pprint
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from requests_html import HTMLSession

URL_START = "https://connect.hoval.com"
URL_SETTINGS_PLANT = (
    "https://connect.hoval.com/service/companion-data/api/settings/plant/"
)
URL_SNAPSHOTS_LIVE = (
    "https://connect.hoval.com/service/companion-data/api/dashboard/snapshots/live/"
)
URL_LATEST_PLANT_EVENTS = (
    "https://connect.hoval.com/service/companion-data/api/plant-events/latest"
)

_LOGGER = logging.getLogger(__name__)


class HovalconnectWebSession(object):
    """HovalConnect web session"""

    def __init__(self, username, password):
        self.last_url = None
        self.username = username
        self.password = password
        self.session = None
        self.logged_in = False
        self.debug = False
        self.plant_access_token = None
        self.plant_id = None

    def _get_url(self, url):
        # GET request
        return self.session.get(url)

    def get_all_forms(self, response):
        """Returns all form tags found on a web page's `url`"""
        # for javascript driven website
        # res.html.render()
        soup = BeautifulSoup(response.html.html, "html.parser")

        # print(type(response))

        return soup.find_all("form")

    def _get_form_details(self, form, extract_data: bool = True):
        """Returns the HTML details of a form,
        including action, method and list of form controls (inputs, etc)"""
        details = {}
        # get the form action (requested URL)
        action = form.attrs.get("action")
        if action:
            action = action.lower()
        # get the form method (POST, GET, DELETE, etc)
        # if not specified, GET is the default in HTML
        method = form.attrs.get("method", "get").lower()
        # get all form inputs
        inputs = []
        for input_tag in form.find_all("input"):
            # get type of input form control
            input_type = input_tag.attrs.get("type", "text")
            # get name attribute
            input_name = input_tag.attrs.get("name")
            # get the default value of that input tag
            input_value = input_tag.attrs.get("value", "")
            # add everything to that list
            inputs.append(
                {"type": input_type, "name": input_name, "value": input_value}
            )
        for select in form.find_all("select"):
            # get the name attribute
            select_name = select.attrs.get("name")
            # set the type as select
            select_type = "select"
            select_options = []
            # the default select value
            select_default_value = ""
            # iterate over options and get the value of each
            for select_option in select.find_all("option"):
                # get the option value used to submit the form
                option_value = select_option.attrs.get("value")
                if option_value:
                    select_options.append(option_value)
                    if select_option.attrs.get("selected"):
                        # if 'selected' attribute is set, set this option as default
                        select_default_value = option_value
            if not select_default_value and select_options:
                # if the default is not set, and there are options, take the first option as default
                select_default_value = select_options[0]
            # add the select to the inputs list
            inputs.append(
                {
                    "type": select_type,
                    "name": select_name,
                    "values": select_options,
                    "value": select_default_value,
                }
            )
        for textarea in form.find_all("textarea"):
            # get the name attribute
            textarea_name = textarea.attrs.get("name")
            # set the type as textarea
            textarea_type = "textarea"
            # get the textarea value
            textarea_value = textarea.attrs.get("value", "")
            # add the textarea to the inputs list
            inputs.append(
                {"type": textarea_type, "name": textarea_name, "value": textarea_value}
            )

        # put everything to the resulting dictionary
        details["action"] = action
        details["method"] = method
        details["inputs"] = inputs
        details["url"] = urljoin(self.last_url, action)

        if extract_data is True:
            data = {}
            for input_tag in details["inputs"]:
                data[input_tag["name"]] = input_tag["value"]
            details["data"] = data

        if self.debug is True:
            pprint(details)

        return details

    def _submit_form(self, form_details):

        url = urljoin(self.last_url, form_details["action"])
        if self.debug is True:
            print(
                "========================================================================================================"
            )
            print("last url: " + str(self.last_url))
            print("new  url: " + str(url))
            print(
                "========================================================================================================"
            )
        if form_details["method"] == "post":
            response = self.session.post(url, data=form_details["data"])
        elif form_details["method"] == "get":
            response = self.session.get(url, params=form_details["data"])
        self.last_url = url
        return response

    def _get_first_form_details(self, response):
        forms = self.get_all_forms(response)
        form_details = self._get_form_details(forms[0])
        return form_details

    def _dump_cookies(self):
        for cookie in self.session.cookies:
            print("cookie domain = " + cookie.domain)
            print("cookie name = " + cookie.name)
            print("cookie value = " + cookie.value)
            print("*************************************")

    def login(self):
        """Login"""
        self.session = HTMLSession()

        # request 1
        response = self._get_url(URL_START)
        print("getting url " + response.url)
        form_details = self._get_first_form_details(response)

        # follow login flow until we get back to the starting url
        while self.last_url == "" or not self.last_url == URL_START:
            response = self._submit_form(form_details)
            print("getting url " + response.url)

            # print(response.html.html)

            if response.url.startswith(URL_START):
                print("logged in")
                break

            form_details = self._get_first_form_details(response)

            if "j_username" in form_details["data"]:
                form_details["data"]["j_username"] = self.username
                form_details["data"]["j_password"] = self.password

    def _get_json(
        self, url, send_xml_http_request: bool = True, send_plant_token: bool = False
    ):
        if send_xml_http_request is True:
            self.session.headers.update({"X-Requested-With": "XMLHttpRequest"})

        if send_plant_token is True:
            self.session.headers.update(
                {"X-Plant-Access-Token": self.plant_access_token}
            )

        # pprint(self.session.headers)

        return self.session.get(url)

    def get_latest_events(self):
        """Get latest events"""
        self.session.headers.update({"X-Requested-With": "XMLHttpRequest"})
        self.session.headers.update({"X-Plant-Access-Token": self.plant_access_token})

        response = self.session.get(URL_LATEST_PLANT_EVENTS)
        print(response.status_code)
        print(response.text)

    def set_plant(self, plant_id: str):
        """ "set plant by id"""
        _LOGGER.info("Setting plant to %s", plant_id)

        self.plant_id = plant_id
        response = self._get_json(URL_SETTINGS_PLANT + self.plant_id)
        print(str(response.status_code) + " " + response.text)
        json = response.json()
        self.plant_access_token = json["token"]

    def get_live_state(self):
        """get live state"""
        _LOGGER.info("Getting live state for plant %s", self.plant_id)
        response = self._get_json(URL_SNAPSHOTS_LIVE + self.plant_id, True, True)
        # print("response ==")
        # pprint(response.status_code)
        return response
