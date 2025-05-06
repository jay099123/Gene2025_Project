from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

"""
TO START YOUR CHROME WITH DEBUGGING CAPABILITY
start chrome "--profile-directory=Default --new-window --remote-debugging-port=9222 --remote-debugging-address=0.0.0.0"
"""

options = Options()

# options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("--disable-infobars")
# options.add_argument("--start-maximized")
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

# options.debugger_address = "127.0.0.1:9222"  # Address of the remote debugging port
options.debugger_address = "172.27.192.1:9222"  # Address of the remote debugging port

# Initialize the WebDriver with the options
driver = webdriver.Chrome(options=options)

# driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#     "source": """
#         Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
#         Object.defineProperty(navigator, 'platform', { get: () => 'Win32' });
#         Object.defineProperty(navigator, 'vendor', { get: () => 'Google Inc.' });
#         Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
#         window.chrome = {
#             runtime: {}
#         };
#         const originalQuery = window.navigator.permissions.query;
#         window.navigator.permissions.query = (parameters) => (
#             parameters.name === 'notifications' ?
#                 Promise.resolve({ state: Notification.permission }) :
#                 originalQuery(parameters)
#         );
#     """
# })

driver.get("https://www.591.com.tw/")