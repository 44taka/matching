import logging.config
import random
import time
import traceback

import sentry_sdk
from bs4 import BeautifulSoup

import config
from bin.base import Base

# sentry初期化
sentry_sdk.init(config.SENTRY["url"], traces_sample_rate=1.0)

# ロギング設定読み込み
logging.config.dictConfig(config.LOG)
logger = logging.getLogger(__name__)


class Omiai(Base):

    def __init__(self):
        super().__init__(url="https://fb.omiai-jp.com/")

    def run(self):
        try:
            logger.info("--- [Omiai足跡ツール] begin ----")
            # ドライバー設定
            driver = self.set_driver()

            # トップページ遷移
            driver.get(self.target_url)
            logger.info("トップページに遷移")

            # 5秒スリープ
            time.sleep(3)

            # ログイン画面遷移
            driver.find_element_by_class_name("login_btn").click()
            logger.info("ログイン画面に遷移")
            time.sleep(3)

            # Facebookログイン画面を開く
            driver.find_element_by_id("om-button-fb-login").click()
            logger.info("Facebookログイン画面を開く")
            logger.debug("URLチェック:%s", driver.current_url)
            time.sleep(3)

            # Facebookログイン処理
            logger.info("Facebookログイン処理中...")
            self.facebook_login(driver)
            time.sleep(3)
            logger.info("Facebookログイン完了！")

            # 画面スクロール
            logger.info("画面スクロール中...")
            self.window_scroll(driver)
            logger.info("画面スクロール完了！")

            # BeautifulSoupにパース
            html = driver.page_source.encode("utf-8")
            soup = BeautifulSoup(html, "html.parser")
            search_list_items = soup.select("div.search-list-item")
            logger.info("プロフィールを見る人数：%s", len(search_list_items))

            # 1人ずつプロフィールを見る
            logger.info("** 1人ずつプロフィールを見る begin **")
            for i in range(len(search_list_items)):
                row = i + 1
                logger.info("%s人目のプロフィール", row)

                # プロフィールを表示
                el = "#om-search-index-content .search-list-item:nth-child({})"
                driver.find_element_by_css_selector(el.format(row)).click()
                # 1秒スリープ
                time.sleep(1)

                # プロフィールを閉じる
                driver.find_element_by_css_selector(
                    "#om-modal-member-detail .btn-dialog-close"
                ).click()
                # 1〜3秒ランダムでスリープ
                time.sleep(random.randint(1, 3))
            logger.info("** 1人ずつプロフィールを見る end **")

            # slack通知
            self.success_message_to_slack(len(search_list_items))
        except Exception as e:
            # エラー処理
            logger.error("エラー発生：%s", e)
            self.error_message_to_slack(traceback.format_exc())
        finally:
            # ドライバー閉じる
            driver.quit()
            logger.info("--- [Omiai足跡ツール] end ----")
