from getpass import getpass
import re
try:
    re._pattern_type = re.Pattern
except AttributeError:
    pass
import werkzeug
try:
    werkzeug.cached_property = werkzeug.utils.cached_property
except AttributeError:
    pass
from robobrowser import RoboBrowser

LOGIN_URL = 'https://ecourts.justice.wa.gov.au/eCourtsPortal/Account/Login'
USERNAME_FIELD_NAME = 'UserName'
PASSWORD_FIELD_NAME = 'Password'
JURISDICTION_SELECTOR_NAME = 'ucQuickSearch$mUcJDLSearch$ddlJurisdiction'
PARTY_NAME_FIELD_START_PAGE_NAME = 'ucQuickSearch$txtPartyName'
PARTY_NAME_FIELD_NAME = 'txtPartyName'
MATTERS_TABLE_ID = 'dgdMatterList'

def search(names):
    username = getpass('eLodgment username?')
    password = getpass('eLodgment password?')
    browser = RoboBrowser(parser='html5lib')
    browser.open(LOGIN_URL)
    acknowledgement_form = browser.get_form()
    browser.submit_form(acknowledgement_form)
    login_form = browser.get_form()
    login_form[USERNAME_FIELD_NAME].value = username
    login_form[PASSWORD_FIELD_NAME].value = password
    browser.submit_form(login_form)
    browser.follow_link(browser.get_link('eLodgment'))
    search_form = browser.get_form()
    search_form[JURISDICTION_SELECTOR_NAME].value = 'Supreme Court'
    browser.submit_form(search_form)
    search_form = browser.get_form()
    search_form[PARTY_NAME_FIELD_START_PAGE_NAME].value = 'test'  # any text will work to get through to the non-start page version
    browser.submit_form(search_form)

    results = {}

    for name in names:
        try:
            name, firstname = name
        except ValueError:
            pass
        search_form = browser.get_form()
        search_form[PARTY_NAME_FIELD_NAME].value = name