from bs4 import BeautifulSoup
import requests
import random
import re
import socket
from . import settings


def loadUserAgents(ua_path):
    UAList = []
    UAFile = open(ua_path, "r")
    for UserAgents in UAFile:
        UAList.append(UserAgents.strip())
    random.shuffle(UAList)
    return UAList


def getproxies(file_path=None, proxynova=True):
    proxies = []
    if file_path:
        print("Using proxies from file")
        with open(file_path, "r") as f:
            data = f.readlines()

        proxies = [x.strip("\n") for x in data]

    else:
        if proxynova:
            print("Using Proxynova")

            data = requests.get("https://www.proxynova.com/proxy-server-list/")
            raw = data.content
            soup = BeautifulSoup(raw, "html.parser")
            for lines in soup.findAll("tr"):  # tr vitrs ko sap nikalne
                if (
                    len(lines.findAll("td")) == 7
                ):  ## tr vitra ko td haru josko length chai 8 xa
                    content = lines.contents[1].contents[1].contents[1].contents[0]
                    pattern = r"'([A-Za-z0-9_\./\\-]*)'"
                    ip = re.search(pattern, content).group()

                    try:
                        ip = eval(ip)
                    except Exception as e:
                        print("Invalid IP during eval: ", e)
                        continue

                    try:
                        socket.inet_aton(ip)
                    except Exception as e:
                        print("Invalid IP after eval: ", e)
                        continue

                    proxies.append(
                        str(ip) + ":" + lines.contents[3].contents[0].strip()
                    )

        else:
            print("Using SSL Proxies")
            data = requests.get("http://sslproxies.org/")
            raw = data.content
            soup = BeautifulSoup(raw, "html.parser")
            for lines in soup.findAll("tr"):
                if len(lines.findAll("td")) == 8:
                    proxies.append(
                        lines.contents[0].contents[0]
                        + ":"
                        + lines.contents[1].contents[0]
                    )
    random.shuffle(proxies)
    return proxies


def create_proxyauth_extension(
    proxy_host,
    proxy_port,
    proxy_username,
    proxy_password,
    scheme="http",
    plugin_path=None,
):
    """Proxy Auth Extension
    args:
        proxy_host (str): domain or ip address, ie proxy.domain.com
        proxy_port (int): port
        proxy_username (str): auth username
        proxy_password (str): auth password
    kwargs:
        scheme (str): proxy scheme, default http
        plugin_path (str): absolute path of the extension
    return str -> plugin_path
    """
    import string
    import zipfile

    if plugin_path is None:
        plugin_path = settings.PLUGIN_PATH

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = string.Template(
        """
    var config = {
            mode: "fixed_servers",
            rules: {
              singleProxy: {
                scheme: "${scheme}",
                host: "${host}",
                port: parseInt(${port})
              },
              bypassList: ["foobar.com"]
            }
          };
    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
    function callbackFn(details) {
        return {
            authCredentials: {
                username: "${username}",
                password: "${password}"
            }
        };
    }
    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """
    ).substitute(
        host=proxy_host,
        port=proxy_port,
        username=proxy_username,
        password=proxy_password,
        scheme=scheme,
    )
    with zipfile.ZipFile(plugin_path, "w") as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return plugin_path


if __name__ == "__main__":
    import os
    import sys
    from contextlib import contextmanager

    @contextmanager
    def stdout_redirected(to=os.devnull):
        """
        import os

        with stdout_redirected(to=filename):
            print("from Python")
            os.system("echo non-Python applications are also supported")
        """
        fd = sys.stdout.fileno()

        ##### assert that Python and C stdio write using the same file descriptor
        ####assert libc.fileno(ctypes.c_void_p.in_dll(libc, "stdout")) == fd == 1

        def _redirect_stdout(to):
            sys.stdout.close()  # + implicit flush()
            os.dup2(to.fileno(), fd)  # fd writes to 'to' file
            sys.stdout = os.fdopen(fd, "w")  # Python writes to fd

        with os.fdopen(os.dup(fd), "w") as old_stdout:
            with open(to, "w") as file:
                _redirect_stdout(to=file)
            try:
                yield  # allow code to be run with the redirected stdout
            finally:
                _redirect_stdout(to=old_stdout)  # restore stdout.
                # buffering and flags such as
                # CLOEXEC may be different

    import ctypes

    libc = ctypes.CDLL(None)
    print("here")
    libc.puts(b"here from C")

    with stdout_redirected():
        print("Python print output")
        libc.puts(b"This comes from C")
        os.system("echo and this is from echo")
        # raise ("Error Error")
