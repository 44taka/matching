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


class Pairs(Base):

    def __init__(self):
        super().__init__(url="https://pairs.lv")

    def run(self):
        try:
            logger.info("--- [Pairs足跡ツール] begin ----")
            # ドライバー設定
            driver = self.set_driver()

            # トップページ遷移
            driver.get(self.target_url)
            logger.info("トップページに遷移")
            time.sleep(3)

            # Facebookログイン画面を開く
            driver.find_element_by_class_name(
                "css-1tp5h8h-FacebookLoginButton"
            ).click()
            logger.info("Facebookログイン画面を開く")
            time.sleep(3)

            # Facebookログイン処理
            logger.info("Facebookログイン処理中...")
            self.facebook_login(driver)
            time.sleep(3)
            logger.info("Facebookログイン完了！")

            # プロフィール検索ページに遷移
            driver.get(self.target_url + "/search")
            logger.info("プロフィール検索ページに遷移")
            time.sleep(5)

            # 画面スクロール
            logger.info("画面スクロール中...")
            self.window_scroll(driver)
            logger.info("画面スクロール完了！")

            # BeautifulSoupにパース
            html = driver.page_source.encode("utf-8")
            soup = BeautifulSoup(html, "html.parser")
            profiles = soup.select("a.css-147kejb-ChunkLayout")
            logger.info("プロフィールを見る人数：%s", len(profiles))

            logger.info("** 1人ずつプロフィールを見る begin **")
            for i, prof in enumerate(profiles):
                driver.get(self.target_url + prof.get("href"))
                logger.debug("%s人目のプロフィール表示", i + 1)
                # 3〜5秒ランダムでスリープ
                time.sleep(random.randint(3, 5))
            logger.info("** 1人ずつプロフィールを見る end **")

            # slack通知
            self.success_message_to_slack(len(profiles))
        except Exception as e:
            # エラー処理
            logger.error("エラー発生：%s", e)
            self.error_message_to_slack(traceback.format_exc())
        finally:
            driver.quit()
            logger.info("--- [Pairs足跡ツール] end ----")
