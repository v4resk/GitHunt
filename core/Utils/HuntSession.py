import os
import pickle
import requests
from colorama import Fore
from bs4 import BeautifulSoup
from getpass import getpass
requests.packages.urllib3.disable_warnings() 

class HuntSession:
    def __init__(self, cookie_file='cookies.pkl'):
        self.cookie_file = cookie_file
        self.cookies = {}
        # Debug is only enabled when GITHUNT_DEBUG environment variable is explicitly set to '1'
        # Default is '0', so debug is False by default
        self.debug = os.environ.get('GITHUNT_DEBUG', '0') == '1'

        def _debug(msg):
            if self.debug:
                print(f"{Fore.YELLOW}[debug]{Fore.WHITE} {msg}")
        self._debug = _debug

        # Prefer token-based auth if available (bypasses web login and MFA)
        github_token = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
        if github_token:
            print(f"{Fore.CYAN}[+] {Fore.WHITE}Using GitHub token from environment; skipping web authentication.")
            self.session = requests.Session()
            self.session.verify = False
            self.session.headers.update({
                'Authorization': f'Bearer {github_token}',
                'Accept': 'application/vnd.github+json',
                'X-GitHub-Api-Version': '2022-11-28',
                'User-Agent': 'GitHunt/1.0'
            })
            self._debug("Token-based session initialized with Authorization header.")
            return

        if os.path.exists(self.cookie_file):
            print(f"{Fore.CYAN}[+] {Fore.WHITE}Cookie file exists. Checking validity...")
            self._load_cookies()
            if not self._is_valid():
                print(f"{Fore.RED}[-] {Fore.WHITE}Cookies are invalid or expired. Re-authenticating...")
                self._delete_cookie_file()
                self.github_authenticate()
            else:
                print(f"{Fore.CYAN}[+] {Fore.WHITE}Cookies are valid.")
        else:
            print(f"{Fore.CYAN}[+] {Fore.WHITE}Cookie file does not exist. Authenticating...")
            self.github_authenticate()

        self.session = requests.Session()
        self.session.verify = False
        # Ensure cookies from auth are available in the session
        if self.cookies:
            self.session.cookies.update(self.cookies)

    def _load_cookies(self):
        """Load cookies from the pickle file."""
        with open(self.cookie_file, 'rb') as f:
            self.cookies = pickle.load(f)

    def _save_cookies(self, cookies):
        """Save cookies to the pickle file."""
        with open(self.cookie_file, 'wb') as f:
            pickle.dump(cookies, f)
        print(f"{Fore.CYAN}[+] {Fore.WHITE}Cookies saved to file.")

    def _is_valid(self):
        """Check if the stored cookies are valid for github.com."""
        try:
            # Request a page that requires authentication to verify cookie validity
            response = requests.get('https://github.com/settings/profile', cookies=self.cookies, allow_redirects=True, timeout=30)
            self._debug(f"Cookie validity check: status={response.status_code} url={response.url}")
            # If redirected back to login or the page contains sign-in prompts, cookies are invalid
            if "/login" in response.url or "Sign in" in response.text:
                print(f"{Fore.RED}[-] {Fore.WHITE}Error, you are not logged in.")
                self._delete_cookie_file()
                return False
            return True

        except requests.RequestException as e:
            print(f"{Fore.RED}[-] {Fore.WHITE}Request error: {e}")
            return False

    def _delete_cookie_file(self):
        """Delete the cookie file."""
        try:
            os.remove(f"./{self.cookie_file}")
            print(f"{Fore.CYAN}[+] {Fore.WHITE}Cookie file deleted.")
        except OSError as e:
            print(f"{Fore.RED}[-] {Fore.WHITE}Error deleting cookie file: {e}")


    def github_authenticate(self):        
        """Authenticate to GitHub and create a new cookie file."""
        print(f"{Fore.CYAN}[+] {Fore.WHITE}Authenticating to GitHub...")
        session = requests.Session()
        # Set a realistic User-Agent to avoid anti-bot blocks
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        })
        login_url = "https://github.com/login"
        
        self._debug(f"GET {login_url}")
        response = session.get(login_url, timeout=30)
        self._debug(f"login page: status={response.status_code} url={response.url}")
        if response.status_code != 200:
            print(f"{Fore.RED}[-] {Fore.WHITE}Failed to retrieve the login page. Status code: {response.status_code}")
            return

        # Parse the page to get the authenticity token
        soup = BeautifulSoup(response.text, 'html.parser')
        authenticity_token_el = soup.find('input', {'name': 'authenticity_token'})
        timestamp_el = soup.find('input', {'name': 'timestamp'})
        timestamp_secret_el = soup.find('input', {'name': 'timestamp_secret'})
        authenticity_token = authenticity_token_el['value'] if authenticity_token_el else None
        timestamp = timestamp_el['value'] if timestamp_el else None
        timestamp_secret = timestamp_secret_el['value'] if timestamp_secret_el else None
        self._debug(f"login tokens: authenticity_token={'ok' if authenticity_token else 'missing'}, timestamp={'ok' if timestamp else 'missing'}, timestamp_secret={'ok' if timestamp_secret else 'missing'}")
        if not all([authenticity_token, timestamp, timestamp_secret]):
            print(f"{Fore.RED}[-] {Fore.WHITE}Unable to retrieve all required tokens.")
            return

        # Perform the POST request to log in
        print(f"{Fore.YELLOW}[+] {Fore.WHITE}Credentials required...")
        username = input("Enter your username: ")
        password = getpass("Enter your password: ")
        data = {
            'commit': 'Sign in',
            'authenticity_token': authenticity_token,
            'login': username,
            'password': password,
            'add_account': '',
            'webauthn-conditional': 'undefined',
            'javascript-support': 'unknown',
            'webauthn-support': 'unknown',
            'webauthn-iuvpaa-support': 'unknown',
            'return_to': 'https://github.com/login',
            'allow_signup': '',
            'client_id': '',
            'integration': '',
            'required_field_c71d': '',
            'timestamp': timestamp,
            'timestamp_secret': timestamp_secret,
        }
        self._debug("POST https://github.com/session (credentials)")
        response = session.post("https://github.com/session", data=data, allow_redirects=True, timeout=30)
        self._debug(f"post-login: status={response.status_code} url={getattr(response, 'url', '')} cookies={[c.name for c in session.cookies]} history={[r.status_code for r in getattr(response, 'history', [])]}")

        # If GitHub returns a two-factor page, it will be a 200 with a 2FA form
        is_two_factor_page = False
        if response.status_code == 200:
            soup_after = BeautifulSoup(response.text, 'html.parser')
            # Detect 2FA by looking for the input field typically named 'otp' or 'app_otp'
            otp_input = soup_after.find('input', {'name': 'otp'}) or soup_after.find('input', {'name': 'app_otp'})
            if otp_input is not None or (hasattr(response, 'url') and 'two-factor' in response.url):
                is_two_factor_page = True
                self._debug("2FA detected: otp/app_otp input present or URL contains 'two-factor'.")
            else:
                self._debug("2FA not detected on post-login page.")

        if is_two_factor_page:
            print(f"{Fore.YELLOW}[+] {Fore.WHITE}2FA required. Please enter your 2FA code.")
            soup_2fa = BeautifulSoup(response.text, 'html.parser')
            # Find the 2FA form and collect all inputs to preserve hidden fields
            two_factor_form = None
            for form in soup_2fa.find_all('form'):
                action = form.get('action', '')
                if '/sessions/two-factor' in action:
                    two_factor_form = form
                    break
            if two_factor_form is None:
                two_factor_form = soup_2fa.find('form')

            form_action = two_factor_form.get('action', '/sessions/two-factor') if two_factor_form else '/sessions/two-factor'
            if form_action.startswith('/'):
                form_action = f"https://github.com{form_action}"
            self._debug(f"2FA form action: {form_action}")

            data_2fa = {}
            if two_factor_form is not None:
                for inp in two_factor_form.find_all('input'):
                    name = inp.get('name')
                    if not name:
                        continue
                    value = inp.get('value', '')
                    data_2fa[name] = value
            self._debug(f"2FA form inputs captured: {list(data_2fa.keys())}")

            # Determine the OTP field name and prompt user
            otp_field_name = 'otp'
            if 'otp' not in data_2fa and 'app_otp' in data_2fa:
                otp_field_name = 'app_otp'
            # If neither otp nor app_otp are present, try to switch to the app code page
            if 'otp' not in data_2fa and 'app_otp' not in data_2fa:
                self._debug("No OTP field found; attempting to switch to authenticator app code page.")
                # Look for a link to the app method
                app_link = None
                for a in soup_2fa.find_all('a'):
                    href = a.get('href', '')
                    text = (a.get_text() or '').lower()
                    if '/sessions/two-factor/app' in href or 'use a code' in text or 'enter a code' in text or 'verification code' in text:
                        app_link = href
                        break
                if app_link:
                    if app_link.startswith('/'):
                        app_link = f"https://github.com{app_link}"
                    self._debug(f"GET {app_link} (switch to app code)")
                    resp_app = session.get(app_link, allow_redirects=True, timeout=30)
                    self._debug(f"app code page: status={resp_app.status_code} url={resp_app.url}")
                    soup_2fa = BeautifulSoup(resp_app.text, 'html.parser')
                    two_factor_form = None
                    for form in soup_2fa.find_all('form'):
                        action = form.get('action', '')
                        if '/sessions/two-factor' in action:
                            two_factor_form = form
                            break
                    if two_factor_form is None:
                        two_factor_form = soup_2fa.find('form')
                    form_action = two_factor_form.get('action', '/sessions/two-factor') if two_factor_form else '/sessions/two-factor'
                    if form_action.startswith('/'):
                        form_action = f"https://github.com{form_action}"
                    self._debug(f"2FA form action (app): {form_action}")
                    data_2fa = {}
                    if two_factor_form is not None:
                        for inp in two_factor_form.find_all('input'):
                            name = inp.get('name')
                            if not name:
                                continue
                            value = inp.get('value', '')
                            data_2fa[name] = value
                    self._debug(f"2FA form inputs (app) captured: {list(data_2fa.keys())}")
                    if 'otp' in data_2fa:
                        otp_field_name = 'otp'
                    elif 'app_otp' in data_2fa:
                        otp_field_name = 'app_otp'
                else:
                    self._debug("No link to app code method found.")
            self._debug(f"Using OTP field name: {otp_field_name}")
            two_fa_code = input("Enter your 2FA code: ")
            data_2fa[otp_field_name] = two_fa_code

            # Some forms include remember device checkbox
            if 'trusted_device' in data_2fa and not data_2fa['trusted_device']:
                data_2fa['trusted_device'] = '1'

            # Retry up to 3 times
            for _ in range(3):
                self._debug(f"POST {form_action} (2FA submit)")
                response_2fa = session.post(form_action, data=data_2fa, allow_redirects=True, timeout=30)
                self._debug(f"2FA response: status={response_2fa.status_code} url={getattr(response_2fa, 'url', '')} cookies={[c.name for c in session.cookies]} history={[r.status_code for r in getattr(response_2fa, 'history', [])]}")
                # Validate by hitting an authenticated page
                try:
                    profile_check = session.get('https://github.com/settings/profile', allow_redirects=True, timeout=30)
                    self._debug(f"profile check after 2FA: status={profile_check.status_code} url={profile_check.url}")
                except Exception as ex:
                    self._debug(f"profile check error: {ex}")
                # Success if redirected away from two-factor page or cookies indicate login
                if (response_2fa.url and '/sessions/two-factor' not in response_2fa.url) or \
                   session.cookies.get('logged_in') == 'yes' or session.cookies.get('user_session'):
                    print(f"{Fore.CYAN}[+] {Fore.WHITE}2FA verified successfully. Authentication complete.")
                    self.cookies = session.cookies
                    self._save_cookies(self.cookies)
                    return
                print(f"{Fore.RED}[-] {Fore.WHITE}2FA verification failed. Please check your code.")
                # Small snippet of response content for diagnostics (no secrets)
                snippet = response_2fa.text[:200].replace('\n', ' ')
                self._debug(f"2FA page snippet: {snippet}")
                two_fa_code = input("Enter your 2FA code: ")
                data_2fa[otp_field_name] = two_fa_code
            return

        # If not a 2FA page, consider login success on presence of session cookies
        if response.status_code in (200, 302):
            if session.cookies.get('logged_in') == 'yes' or session.cookies.get('user_session'):
                print(f"{Fore.CYAN}[+] {Fore.WHITE}Valid credentials.")
                self.cookies = session.cookies
                self._save_cookies(self.cookies)
                return
            # Fallback: detect login error message
            if "Incorrect username or password" in response.text:
                print(f"{Fore.RED}[-] {Fore.WHITE}Invalid username or password.")
                return
        print(f"{Fore.RED}[-] {Fore.WHITE}Failed to login. Status code: {response.status_code}")
        self._debug(f"Login failure page url={getattr(response, 'url', '')} snippet={(response.text[:200] if hasattr(response, 'text') else '')}")


    