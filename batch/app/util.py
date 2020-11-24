import datetime
import slackweb
import config


def now():
    """
    現在時刻取得
    :return: 現在時刻
    """
    return datetime.datetime.now()


def notify_slack(message=None):
    """
    slack通知処理
    url: https://github.com/satoshi03/slack-python-webhook
    :param message: 通知メッセージ
    :return:
    """
    if message is not None:
        slack = slackweb.Slack(url=config.SLACK["url"])
        slack.notify(text=message)


def num2alpha(num):
    if num <= 26:
        return chr(64 + num)
    elif num % 26 == 0:
        return num2alpha(num//26-1)+chr(90)
    else:
        return num2alpha(num//26)+chr(64 + num % 26)
