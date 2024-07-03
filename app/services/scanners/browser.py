from selenium import webdriver
from flask import current_app
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options


def get_remote_webdriver() -> webdriver.Remote:
    # Initialize the WebDriver
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Set the URL of the Selenium Hub
    selenium_hub_url = current_app.config.get("SELENIUM_HUB_URL", "http://selenium-hub:4444")
    if not selenium_hub_url:
        raise Exception("SELENIUM_HUB_URL is not set in the configuration")

    if options is None:
        raise Exception("Failed to initialize Chrome options")

    try:
        capabilities = options.to_capabilities()
        print(f"Using capabilities: {capabilities}")

        return webdriver.Remote(
            command_executor=selenium_hub_url,
            options=options,
        )
    except Exception as err:
        raise Exception(
            f"Failed to connect to the Selenium Remote WebDriver at {selenium_hub_url}. "
            f"Ensure that the Selenium Hub is up and running. Error: {err}."
        )
