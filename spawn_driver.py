import json
import os
import tempfile
from functools import reduce
from fake_useragent import UserAgent
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import undetected_chromedriver as webdriver


class ChromeWithPrefs(webdriver.Chrome):
    def __init__(self, *args, options=None, **kwargs):
        if options:
            self._handle_prefs(options)

        super().__init__(*args, options=options, **kwargs)

        # remove the user_data_dir when quitting
        self.keep_user_data_dir = False

    @staticmethod
    def _handle_prefs(options):
        if prefs := options.experimental_options.get("prefs"):
            # turn a (dotted key, value) into a proper nested dict
            def undot_key(key, value):
                if "." in key:
                    key, rest = key.split(".", 1)
                    value = undot_key(rest, value)
                return {key: value}

            # undot prefs dict keys
            undot_prefs = reduce(
                lambda d1, d2: {**d1, **d2},  # merge dicts
                (undot_key(key, value) for key, value in prefs.items()),
            )

            # create an user_data_dir and add its path to the options
            user_data_dir = os.path.normpath(tempfile.mkdtemp())
            options.add_argument(f"--user-data-dir={user_data_dir}")

            # create the preferences json file in its default directory
            default_dir = os.path.join(user_data_dir, "Default")
            os.mkdir(default_dir)

            prefs_file = os.path.join(default_dir, "Preferences")
            with open(prefs_file, encoding="latin1", mode="w") as f:
                json.dump(undot_prefs, f)

            # pylint: disable=protected-access
            # remove the experimental_options to avoid an error
            del options._experimental_options["prefs"]


def start():
    prefs = {'permissions.default.image': 2, 'extensions.contentblocker.enabled': True,
             'dom.ipc.plugins.enabled.libflashplayer.so': False, 'media.autoplay.default': 1,
             'media.autoplay.allow-muted': False}
    chrome_options = webdriver.ChromeOptions()
    caps = DesiredCapabilities().CHROME
    # caps["pageLoadStrategy"] = "none"
    caps["pageLoadStrategy"] = "none"
    # chrome_options.binary_location = os_environ.get("GOOGLE_CHROME_BIN")
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument('--start-fullscreen')
    # chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_argument('--blink-settings=videosEnabled=false')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument(f'user-agent={UserAgent().random}')
    chrome_options.add_argument('--disable-popup-blocking')

    chrome_options.add_experimental_option("prefs", prefs)

    # use the derived Chrome class that handles prefs
    driver = ChromeWithPrefs(options=chrome_options, use_subprocess=True, desired_capabilities=caps)
    return driver
