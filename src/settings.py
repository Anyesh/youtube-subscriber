import os

BASE_DIR = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))


DRIVER_PATH = os.path.join(BASE_DIR, "drivers/geckodriver.exe")

HEADLESS = False

UA_FILENAME = "UserAgents.txt"

P_FILENAME = "proxylist.txt"

UAPATH = os.path.join(BASE_DIR, UA_FILENAME)
PROXYPATH = os.path.join(BASE_DIR, P_FILENAME)

CRD_PATH = os.path.join(BASE_DIR, ".credentials")
PLUGIN_PATH = os.path.join(BASE_DIR, ".plugin/vimm_chrome_proxyauth_plugin.zip")

FAILED_CRED = os.path.join(BASE_DIR, ".failed_creds")
NEW_CRED = os.path.join(BASE_DIR, ".new_creds")

TESTPATH = ""

TMP_PWD = "Apple11@A"

SIGNIN = "https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?redirect_uri=https%3A%2F%2Fdevelopers.google.com%2Foauthplayground&prompt=consent&response_type=code&client_id=407408718192.apps.googleusercontent.com&scope=email&access_type=offline&flowName=GeneralOAuthFlow"

## yedi socks rexa vani
SOCKS = False

UNSUBSCRIBE = True
TARGET_CHANNEL = (
    "https://www.youtube.com/channel/UCPd5mEfJ8PkwlP3yjQfh4xQ?view_as=subscriber"
)
