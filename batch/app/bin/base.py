import random
import time

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import config
import util


class Base(object):

    def __init__(self, url):
        self.target_url = url

    def set_driver(self) -> webdriver.Remote:
        return webdriver.Remote(
            command_executor="http://selenium-hub:4444/wd/hub",
            desired_capabilities=DesiredCapabilities.CHROME
        )

    def facebook_login(self, driver: webdriver.Remote) -> None:
        # 操作ウィンドウを切り替える
        driver.switch_to.window(driver.window_handles[1])
        # ログイン実行
        driver.find_element_by_id("email").send_keys(config.FB["user_id"])
        driver.find_element_by_id("pass").send_keys(config.FB["password"])
        driver.find_element_by_name("login").click()
        time.sleep(5)
        # OKボタン押下
        driver.find_element_by_name("__CONFIRM__").click()
        # 操作ウィンドウ切り替える
        driver.switch_to.window(driver.window_handles[0])

    def window_scroll(self, driver: webdriver.Remote) -> None:
        for _ in range(random.randint(3, 5)):
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(3)

    def success_message_to_slack(self, count: int) -> None:
        message = "ステータス：OK"
        message += "\n足跡をつけた人数：" + str(count)
        util.notify_slack(message)

    def error_message_to_slack(self, err: str) -> None:
        message = "ステータス：NG"
        message += "\nエラー内容：" + err
        util.notify_slack(message)

