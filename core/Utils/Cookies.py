import os
import pickle
import requests
from colorama import init, Fore
from bs4 import BeautifulSoup
from getpass import getpass

class Cookies:
    def __init__(self, cookie_file='cookies.pkl'):
        self.cookie_file = cookie_file
        self.cookies = {}

        if os.path.exists(self.cookie_file):
            print(f"{Fore.GREEN}[+] {Fore.WHITE}Cookie file exists. Checking validity...")
            self._load_cookies()
            if not self._is_valid():
                print(f"{Fore.RED}[-] {Fore.WHITE}Cookies are invalid or expired. Re-authenticating...")
                self._delete_cookie_file()
                self.github_authenticate()
            else:
                print(f"{Fore.GREEN}[+] {Fore.WHITE}Cookies are valid.")
        else:
            print(f"{Fore.GREEN}[+] {Fore.WHITE}Cookie file does not exist. Authenticating...")
            self.github_authenticate()

        self.session = requests.Session()
        self.session.verify = False
        self.session.cookies.update(self.cookies)


    def _load_cookies(self):
        """Load cookies from the pickle file."""
        with open(self.cookie_file, 'rb') as f:
            self.cookies = pickle.load(f)

    def _save_cookies(self, cookies):
        """Save cookies to the pickle file."""
        with open(self.cookie_file, 'wb') as f:
            pickle.dump(cookies, f)
        print(f"{Fore.GREEN}[+] {Fore.WHITE}Cookies saved to file.")

    def _is_valid(self):
        """Check if the stored cookies are valid for github.com."""
        try:
            # Test request to GitHub to verify cookie validity
            response = requests.get('https://github.com', cookies=self.cookies)
            
            # Check if 'Sign in' text is present on the page
            if "Sign in" in response.text:
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
            print(f"{Fore.GREEN}[+] {Fore.WHITE}Cookie file deleted.")
        except OSError as e:
            print(f"{Fore.RED}[-] {Fore.WHITE}Error deleting cookie file: {e}")


    def github_authenticate(self):        
        """Authenticate to GitHub and create a new cookie file."""
        print(f"{Fore.GREEN}[+] {Fore.WHITE}Authenticating to GitHub...")
        session = requests.Session()
        login_url = "https://github.com/login"
        
        response = session.get(login_url)
        if response.status_code != 200:
            print(f"{Fore.RED}[-] {Fore.WHITE}Failed to retrieve the login page. Status code: {response.status_code}")
            return

        # Parse the page to get the authenticity token
        soup = BeautifulSoup(response.text, 'html.parser')
        authenticity_token = soup.find('input', {'name': 'authenticity_token'})['value']
        timestamp = soup.find('input', {'name': 'timestamp'})['value']
        timestamp_secret = soup.find('input', {'name': 'timestamp_secret'})['value']
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
        response = session.post("https://github.com/session", data=data)
        if response.status_code == 200:
            print(f"{Fore.GREEN}[+] {Fore.WHITE}Valid credentials.")
            #Check if we need to handle 2FA
            if "session-otp-input-label" in response.text:
                print(f"{Fore.YELLOW}[+] {Fore.WHITE}2FA required. Please enter your 2FA code.")
                # Extract the authenticity token from the 2FA page
                soup = BeautifulSoup(response.text, 'html.parser')
                authenticity_token_2fa = soup.find('input', {'name': 'authenticity_token'})['value']
                if not authenticity_token_2fa:
                    print(f"{Fore.RED}[-] {Fore.WHITE}Unable to retrieve 2FA authenticity token.")
                    return
                
                # Prompt user for 2FA code
                two_fa_code = input("Enter your 2FA code: ")
                data_2fa = {
                    'authenticity_token': authenticity_token_2fa,
                    'app_otp': two_fa_code,
                }
                response_2fa = session.post("https://github.com/sessions/two-factor", data=data_2fa)
                if response_2fa.status_code == 200 and username in response_2fa.text:
                    print(f"{Fore.GREEN}[+] {Fore.WHITE}2FA verified successfully. Authentication complete.")
                    self._save_cookies(session.cookies)
                else:
                    print(f"{Fore.RED}[-] {Fore.WHITE}2FA verification failed. Please check your code.")
        else:
            print(f"Failed to login. Status code: {response.status_code}")


