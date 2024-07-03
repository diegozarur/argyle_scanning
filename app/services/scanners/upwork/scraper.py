import json
from typing import Dict, Optional, Any
from selenium.common import JavascriptException
from bs4 import BeautifulSoup
import requests
from .parser import parse_profile
from ..browser import get_remote_webdriver


class UpworkScraper:
    def __init__(self, scanner_settings: Dict[str, str]) -> None:
        """
        Initialize the UpworkScraper with scanner settings.

        :param scanner_settings: Dictionary containing settings for the scanner.
        """
        self._base_url = "https://www.upwork.com"
        self._scanner_settings = scanner_settings
        self._driver = get_remote_webdriver()
        self._session = requests.Session()
        self._ciphertext_url = "https://www.upwork.com/nx/find-work/best-matches"

    def get_tokens_from_cookies(self) -> Dict[str, str]:
        """
        Extract tokens from browser cookies.

        :return: Dictionary of tokens.
        """
        cookies = self._driver.get_cookies()
        tokens = {}
        for cookie in cookies:
            if "xsrf" in cookie["name"].lower():
                tokens["csrf_token"] = cookie["value"]
            elif "gql" in cookie["name"].lower():
                tokens["visitor_gql_token"] = cookie["value"]
            elif "forterToken" in cookie["name"]:
                tokens["forterToken"] = cookie["value"]
            elif "iovation" in cookie["name"]:
                tokens["iovation"] = cookie["value"]
        return tokens

    def start_searching(self) -> Dict[str, Any]:
        """
        Start the scraping process.

        :return: Parsed profile data.
        """
        try:
            self._driver.get(self._base_url)
            tokens = self.get_tokens_from_cookies()

            self._login(tokens)
            ciphertext = self._get_ciphertext()

            if not ciphertext:
                raise ValueError("Failed to retrieve ciphertext from Upwork")

            profile_details = self._get_profile_details(ciphertext)
            parsed_profile = parse_profile(profile_details)
        except JavascriptException as e:
            self._driver.quit()
            raise Exception(f"JavaScript execution failed during scraping!")
        except Exception as e:
            self._driver.quit()
            raise Exception(f"Scraper failed with error: {e}")

        self._driver.quit()
        return parsed_profile.dict()

    def _login(self, tokens: Dict[str, str]) -> None:
        """
        Perform the login action using tokens.

        :param tokens: Dictionary containing necessary tokens.
        """
        req_params = dict(
            url=self._scanner_settings["url"],
            headers={
                "accept": "*/*",
                "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
                "content-type": "application/json",
                "priority": "u=1, i",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "macOS",
                "sec-ch-viewport-width": "1120",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "x-odesk-csrf-token": tokens.get("csrf_token", ""),
                "x-requested-with": "XMLHttpRequest",
            },
            body={
                "login": {
                    "mode": "password",
                    "iovation": tokens.get("iovation", ""),
                    "username": self._scanner_settings["username"],
                    "elapsedTime": 28952,
                    "forterToken": tokens.get("forterToken", ""),
                    "deviceType": "desktop",
                    "password": self._scanner_settings["password"],
                    "securityCheckCertificate": tokens.get(
                        "securityCheckCertificate", ""
                    ),
                    "authToken": tokens.get("authToken", ""),
                }
            },
            method="POST",
        )
        self._fetch_with_script(**req_params)

    def _get_profile_details(self, ciphertext: str) -> dict:
        """
        Get the profile details using the ciphertext.

        :param ciphertext: Ciphertext of the profile.
        :return: Profile details in JSON format.
        """
        req_params = dict(
            url=f"https://www.upwork.com/freelancers/api/v1/freelancer/profile/{ciphertext}/details?excludeAssignments=True",
            headers={
                "accept": "application/json, text/plain, */*",
                "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
                "priority": "u=1, i",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "macOS",
                "sec-ch-viewport-width": "1120",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "x-odesk-user-agent": "oDesk LM",
                "x-requested-with": "XMLHttpRequest",
                "x-upwork-accept-language": "en-US",
            },
        )
        return self._fetch_with_script(**req_params)

    def _get_ciphertext(self) -> str:
        """
        Fetch the ciphertext from the best matches page.

        :return: Ciphertext string.
        """
        html_response = self._fetch_with_script(
            url=self._ciphertext_url,
            headers={
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
                "cache-control": "max-age=0",
                "priority": "u=0, i",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "macOS",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "same-origin",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
            },
        )
        ciphertext = self._extract_ciphertext(html_response)
        if not ciphertext:
            return ""
        return ciphertext

    def _extract_ciphertext(self, html: str) -> Optional[str]:
        """
        Extract the ciphertext from the given HTML.

        :param html: HTML content as a string.
        :return: Ciphertext if found, otherwise None.
        """
        soup = BeautifulSoup(html, "html.parser")
        profile_link = soup.find("a", href=True, text="Profile")
        if profile_link:
            href = profile_link["href"]
            ciphertext = href.split("/")[-1]
            return ciphertext
        return None

    def _fetch_with_script(
            self,
            url: str,
            headers: Dict[str, str],
            body: Optional[Dict] = None,
            method: str = "GET",
    ) -> Optional[Dict]:
        """
        Execute a fetch request using JavaScript in the browser.

        :param url: URL to fetch.
        :param headers: Headers to include in the fetch request.
        :param body: Body of the POST request, if any.
        :param method: HTTP method to use.
        :return: Response from the fetch request, parsed as JSON if possible.
        """
        fetch_script = f"""
        return fetch("{url}", {{
          "headers": {json.dumps(headers)},
          "method": "{method}",
          "body": {json.dumps(body) if body else "None"},
          "mode": "cors",
          "credentials": "include"
        }}).then(response => {{
              if (response.headers.get('content-type')?.includes('application/json')) {{
                return response.json();
              }} else {{
                return response.text();
              }}
            }});
        """
        return self._driver.execute_script(fetch_script)
