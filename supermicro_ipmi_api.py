import requests as rq
import secrets as s

# ----------------------------------------------------------------------------------------------------------------------
# GLOBALS
# ----------------------------------------------------------------------------------------------------------------------

session = rq.session()
logged_in = False

# urls
login_url = f"http://{s.ip_address}/cgi/login.cgi"
logout_url = f"http://{s.ip_address}/cgi/logout.cgi"
impi_url = f"http://{s.ip_address}/cgi/ipmi.cgi"


# ----------------------------------------------------------------------------------------------------------------------
# FUNCTIONS
# ----------------------------------------------------------------------------------------------------------------------

def login(url: str = None, usr_name: str = None, password: str = None):
    """
    Performs a login to get the session cookie from the IPMI Interface.

    :param url: url to send post request to. default is login_url in globals
    :param usr_name: user name for the login. default secrets.server_usr
    :param password: password for the login. default secrets.server_pwd
    :return:
    """
    _url = login_url
    _usr = s.server_usr
    _pwd = s.server_pwd
    global logged_in

    # overwrite populated entries
    if url is not None:
        _url = url

    if usr_name is not None:
        _usr = usr_name

    if password is not None:
        _pwd = password

    _login = session.request("POST", _url, data={"name": _usr, "pwd": _pwd})

    # check response
    if not _login.ok:
        raise ValueError(f"Wrong Credentials or URL: code {_login.status_code}")

    logged_in = True


def logout(url: str = None):
    """
    Performs logout.

    :param url: url for logout. default logout_url
    :return:
    """
    _url = logout_url
    global logged_in

    if url is not None:
        _url = url

    _logout = session.request("GET", _url)

    logged_in = False

    if not _logout.ok:
        raise ValueError(f"Wrong Credentials or URL: code {_logout.status_code}")


def power_on(logout_after: bool = False):
    """
    Performs power on. If the user is not logged in, a login with the defaults is attempted.

    :param logout_after: logs user out after power_on
    :return:
    """
    if not logged_in:
        login()

    _power_on = session.request("POST", impi_url, data={"POWER_INFO.XML": "(1, 1)"})

    if not _power_on.ok:
        raise ValueError(f"Wrong Credentials or URL: code {_power_on.status_code}")

    if logout_after:
        logout()


def power_off_orderly(logout_after: bool = False):
    """
    Performs orderly poweroff. If the user is not logged in, a login with the defaults is attempted.

    :param logout_after: logs user out after orderly power off
    :return:
    """
    if not logged_in:
        login()

    _power_off_o = session.request("POST", impi_url, data={"POWER_INFO.XML": "(1, 5)"})

    if not _power_off_o.ok:
        raise ValueError(f"Wrong Credentials or URL: code {_power_off_o.status_code}")

    if logout_after:
        logout()


def power_off_immediately(logout_after: bool = False):
    """
    Performs immediate power off. If the user is not logged in, a login with the defaults is attempted.

    :param logout_after: logs user out after immediate power off
    :return:
    """
    if not logged_in:
        login()

    _power_off_i = session.request("POST", impi_url, data={"POWER_INFO.XML": "(1, 0)"})

    if not _power_off_i.ok:
        raise ValueError(f"Wrong Credentials or URL: code {_power_off_i.status_code}")

    if logout_after:
        logout()


def reset_power(logout_after: bool = False):
    """
    Performs power reset. If the user is not logged in, a login with the defaults is attempted.

   :param logout_after: logs user out after power reset
   :return:
   """
    if not logged_in:
        login()

    _power_off_r = session.request("POST", impi_url, data={"POWER_INFO.XML": "(1, 3)"})

    if not _power_off_r.ok:
        raise ValueError(f"Wrong Credentials or URL: code {_power_off_r.status_code}")

    if logout_after:
        logout()


def power_cycle(logout_after: bool = False):
    """
    Performs power cycle. If the user is not logged in, a login with the defaults is attempted.

   :param logout_after: logs user out after power cycle
   :return:
   """
    if not logged_in:
        login()

    _power_off_ps = session.request("POST", impi_url, data={"POWER_INFO.XML": "(1, 2)"})

    if not _power_off_ps.ok:
        raise ValueError(f"Wrong Credentials or URL: code {_power_off_ps.status_code}")

    if logout_after:
        logout()
