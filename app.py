# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

from __future__ import unicode_literals
from enum import Enum
import errno
import os
import sys
import tempfile
from argparse import ArgumentParser
import excelread
import random
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton
)
import os
import notifer
import traceback

import stealer
import random
import datetime

app = Flask(__name__)
VERSION = "KBIS 1.1 (MELT)"

UPDATE_HISTORY = """
12/3 
     エクセルファイルの取得URLを変更git
     excelToid廃止
12/6    ver 1.0 (NELV)
     VERSION作った
     ジョーク機能の追加
12/7    ver 1.0.1
     インデントの修正
        ver 1.0.2
     バージョン照会追加
     バージョンの書き方を修正
     !damaの結果に少数が含まれないように修正
12/10   ver 1.0.3
     group_checkを修正
     alt-textについて修正
12/11   ver 1.0.4
     datetimeモジュールを追加
     それを用いて更新日時を取得
     再起動/起動時のデータ取得の
     結果をmenuに明示
12/25   ver 1.0.5
     予備費が表示されない不具合を修正
12/28   ver 1.0.6
     レイアウト修正
12/31   ver 1.0.7
     内部修正
        ver 1.0.7.1
     さらにほんのちょっと修正
        ver 1.0.8
     messageが複数遅れるらしいのでテスト
        ver 1.0.9
     レイアウト修正
        ver 1.0.9.1
     messageが複数送ろうとすると文字数
     制限が厳しいのでやっぱやめた
1/6     ver 1.0.10
     コード大幅修正　DLFailed時の処理を変更した。
1/7     ver 1.0.11
     コードに解説を少し追加　このまま可読性を上げていきたい
        ver 1.1
     ソースコード公開
    """
VERSION_MEMO = """鍵が溶けて公開される・・・みたいな"""

DEV_MEMO = """複数のメッセージが返信できるらしい・・・"""

REUD_MEMO = """パブリックレポジトリに何とかしてみた。"""

WAKE_TIME = datetime.datetime.now().strftime('%m/%d %H:%M')


class UserType(Enum):
    """
    KBISではユーザの種類を4種類に分割する。

    値が大きければ大きいほど権限が強い
    """
    EXTERNAL_USER = 0
    NORMAL_USER = 1
    WELLKNOWN_USER = 2
    ADMINISTRATOR = 3  # can add wellknown_user etc..
    DEVELOPER = 4  # same as admin + add admin


def get_user_type(user_id: str) -> UserType:
    """
    ユーザの権限をuser_idとmanagerから識別する。

    :param user_id: str

        ユーザのID

    :return: UserType

        ユーザの権限
    """
    global manager
    for i in special_users:
        if i[1] == user_id:
            return UserType(int(i[2]))
    for i in manager.memberlist:
        if i.id == user_id:
            return UserType.NORMAL_USER
    return UserType.EXTERNAL_USER




try:
    DLFailedFlag = False
    stealer.download_file_from_google_drive ( os.getenv ( 'MANAGE_BOOK' ), '会計管理簿.xlsx' )
    stealer.download_file_from_google_drive ( os.getenv ( 'SPECIALUSERIDS' ), 'SpecialUserIds' )
    stealer.download_file_from_google_drive ( os.getenv ( 'EXCELIDS' ), 'excel-id.txt' )
    specialIdsFile = open ( 'SpecialUserIds' )
    string_list = specialIdsFile.readlines ( )
    string_list = [ i.strip ( ) for i in string_list ]
    special_users = [ ]
    for i in string_list:
        special_users.append ( i.split ( ',' ) )
    manager = excelread.Manager('会計管理簿.xlsx')
except:
    notifer.output('may download failed go to failed_mode...')
    notifer.output(traceback.format_exc())
    DLFailedFlag = True

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')



# function for create tmp dir for download content
def make_static_tmp_dir():
    try:
        os.makedirs(static_tmp_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
            pass
        else:
            raise

#以下の二つはcurlコマンドでサーバを寝かせないようにするため

@app.route("/renew")
def renew2():
    return "renew curl success!"


@app.route("/alive")
def open():
    return "alive!"


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except LineBotApiError as e:
        print("Got exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            print("  %s: %s" % (m.property, m.message))
        print("\n")
    except InvalidSignatureError:
        abort(400)
    return 'OK'


def template_message_send(word: str, event, button_label='メニューに戻る', button_word='menu'):
    """
    ボタンが一つ付加されたメッセージを返信する関数

    :param word:
        送りたい文字列

    :param event:
        eventオブジェクト

    :param button_label:
        ボタンのラベル

    :param button_word:
        ボタンを押した時にユーザが送信することになるワード

    :return None:


    """
    buttons_template = ButtonsTemplate(
        text=word, actions=[
            MessageAction(label=button_label, text=button_word)
        ])
    template_message = TemplateSendMessage(
        alt_text=word, template=buttons_template)
    line_bot_api.reply_message(event.reply_token, template_message)



def template_text_send(word: str, event):
    """
    ボタンがついていないメッセージを返信する関数

    :param word:
        送りたい文字列

    :param event:
        eventオブジェクト

    :return None:
    """
    if isinstance(event.source, SourceUser):
        line_bot_api.reply_message(
            event.reply_token, [TextSendMessage(text=word)])
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=word))


def omikuji() -> str:
    """
    乱数を用いておみくじを行う関数

    strが返ります

    :return str:
        おみくじの結果
    """
    value = random.random()
    notifer.output(f'おみくじに挑戦!\nvalue={value}')
    if value < 0.001:
        return '大吉'
    elif value < 0.004:
        return '中吉'
    elif value < 0.007:
        return '吉'
    elif value < 0.014:
        return '小吉'
    elif value < 0.021:
        return '末吉'
    elif value < 0.034:
        return '末凶'
    elif value < 0.050:
        return '凶'
    elif value < 0.052:
        return '大凶'
    elif value < 0.060:
        return 'ぴょん吉'
    elif value < 0.066:
        return 'だん吉'
    elif value < 0.074:
        return 'かん吉'
    elif value < 0.084:
        return '松'
    elif value < 0.1:
        return '鶴'
    elif value < 0.12:
        return '梅'
    elif value < 0.14:
        return '目白'
    elif value < 0.16:
        return '桜'
    elif value < 0.18:
        return 'ほととぎす'
    elif value < 0.20:
        return 'ホトトギス'
    elif value < 0.24:
        return '牡丹'
    elif value < 0.28:
        return '蝶'
    elif value < 0.33:
        return 'イノシシ'
    elif value < 0.35:
        return '坊主'
    elif value < 0.38:
        return '月'
    elif value < 0.41:
        return '盃'
    elif value < 0.44:
        return '紅葉'
    elif value < 0.47:
        return '鹿'
    elif value < 0.50:
        return '歯科'
    elif value < 0.53:
        return 'シカ'
    elif value < 0.56:
        return 'ニャア'
    elif value < 0.59:
        return '鳳凰'
    elif value < 0.62:
        return 'ピジョット'
    elif value < 0.65:
        return 'アップルパイ'
    elif value < 0.68:
        return 'このおみくじはジョークです。'
    elif value < 0.69:
        return 'ウルトアレア(UR)'
    elif value < 0.71:
        return 'ダブルスーパーレア(SSR)'
    elif value < 0.75:
        return 'レア(R)'
    elif value < 0.77:
        return 'ノーマル(N)'
    elif value < 0.778:
        return '大当たり!!!!!'
    elif value < 0.779:
        return 'これは0.1%でしか表示されないメッセージです！　おめでとう！'
    elif value < 0.80:
        return 'ネタ切れ'
    elif value < 0.84:
        return 'レジェンドレア'
    elif value < 0.88:
        return 'エピックレア'
    elif value < 0.92:
        return 'レア'
    elif value < 0.94:
        return '天才'
    elif value < 0.97:
        return '秀才'
    elif value < 0.99:
        return '最強'
    elif value < 0.9901:
        return '神'
    else:
        return 'そこそこ'



notifer.output(f'{VERSION} 起動')


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    """
    LINE_BOTにメールが送られた時に使用される関数
    :param event:
        LINEから貰えるデータ。
        色々入っている
    :return: なし
    """
    global manager
    profile = line_bot_api.get_profile(event.source.user_id)

    if DLFailedFlag:
        """
        ダウンロードに失敗した場合は、Herokuをクラッシュさせて再起動させる。
        """
        template_text_send('Sorry! GoogleDrive エラーのため再起動を行います。　数分後にお試しください。',event)
        notifer.output (f'screenname: {profile.display_name} \nid: {profile.user_id} \ntext: {event.message.text}' )
        while True:
            pass


    text = event.message.text
    user_type = get_user_type(profile.user_id, manager)
    success_str = '失敗' if DLFailedFlag else '成功'

    notifer.output(
        f'screenname: {profile.display_name} \nid: {profile.user_id} \ntext: {event.message.text}\n権限:{user_type}')
    if text.startswith('!'):  # joke commands
        word = text[1:]
        ret = 'debug return'
        if word == 'jokes':
            JORK_LIST = """!omikuji 運勢を占います
!dama    ランダムでお年玉の金額を表示させます。
!ver     バージョン裏話
!dev     開発裏話
!reud    めっちゃどうでもいい話"""
            ret = JORK_LIST
        elif word == 'omikuji':
            res = omikuji()
            notifer.output(f'結果:{res}')
            ret = f'くじ引きの結果:{res}'
        elif word == 'dama':
            res = int(random.gauss(10000, 5000))
            notifer.output(f'お年玉に挑戦! 結果:{res}円')
            ret = f'{res}円 ゲット！'
        elif word == 'ver':
            ret = VERSION_MEMO
        elif word == 'dev':
            ret = DEV_MEMO
        elif word == 'reud':
            ret = REUD_MEMO
        else:
            ret = ' ! コマンドが認識できません'

        template_message_send(ret, event)
    elif text == 'help' and user_type != UserType.EXTERNAL_USER:
        word = """[profile] IDを紹介します
[rank] 自分の権限が分かります
[check] 滞納額を確認します
[menu] メニューを表示します
[group_check] 班の予算状況が見れます
[his] アップデート履歴を確認します
[ver] 現在のバーションを確認します
[!jokes] ???"""
        template_text_send(word, event)
    elif text == 'dev_see' and (user_type == UserType.DEVELOPER or user_type == UserType.ADMINISTRATOR):
        notifer.output(manager.output_data())
        if isinstance(event.source, SourceUser):
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text='Display name: ' + profile.display_name),
                    TextSendMessage(
                        text='Your id is: ' + profile.user_id + 'if you want to go back to menu \n input [menu] plz')
                ]
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Bot can't use profile API without user ID"))
    elif text == 'ver':
        template_message_send(VERSION, event)
    elif text == 'profile':
        template_text_send(f'Your id is {profile.user_id}', event)
        notifer.output('IDは以下の通りです。')
        notifer.output(f'{profile.user_id}')
    elif text == 'his':
        template_text_send(UPDATE_HISTORY, event)
        notifer.output('history opened')
    elif text == 'rank':
        if (user_type == UserType.EXTERNAL_USER):
            mes = 'あなたは外部ユーザです。'
        elif (user_type == UserType.NORMAL_USER):
            mes = 'あなたは部内の人間です。'
        elif (user_type == UserType.ADMINISTRATOR):
            mes = '管理者さんこんにちは！！！'
        elif (user_type == UserType.DEVELOPER):
            mes = 'ようこそ開発者さん！'
        if isinstance(event.source, SourceUser):
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text=mes)
                ]
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Bot can't use profile API without user ID"))
    elif text == 'check' and (
            UserType.DEVELOPER == user_type or UserType.ADMINISTRATOR == user_type or UserType.NORMAL_USER == user_type or UserType.WELLKNOWN_USER == user_type):
        notifer.output(success_str)
        if (UserType.DEVELOPER == user_type):
            buttons_template = ButtonsTemplate(
                text=f'更新日時:{WAKE_TIME}', actions=[
                    URIAction(label='Go To reud.net', uri='https://reud.net/'),
                    # PostbackAction ( label='Back to menu', data='menu' ),
                    # PostbackAction ( label='ping with text', data='ping', text='ping' ),
                    MessageAction(label='Back to menu', text='menu')
                ])
            template_message = TemplateSendMessage(
                alt_text=f'更新日時:{WAKE_TIME}\n起動時更新:{success_str}', template=buttons_template)
            line_bot_api.reply_message(event.reply_token, template_message)

        else:
            data = manager.getFromId(profile.user_id)
            ret_text = f'滞納額は{data.money:,}円です。\n更新日時{WAKE_TIME}' if data.money >= 0 else f'{abs(data.money):,}円の返金あり。\n更新日時{WAKE_TIME}'
            buttons_template = ButtonsTemplate(
                text=ret_text, actions=[
                    # URIAction(label='Go to line.me', uri='https://line.me'),
                    # PostbackAction(label='Back to menu', data='menu'),
                    # PostbackAction(label='ping with text', data='ping', text='ping'),
                    MessageAction(label='Back to menu', text='menu')
                ])
            template_message = TemplateSendMessage(
                alt_text=ret_text, template=buttons_template)
            line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'menu' and (
            UserType.DEVELOPER == user_type or UserType.ADMINISTRATOR == user_type or UserType.NORMAL_USER == user_type or UserType.WELLKNOWN_USER == user_type):
        if (UserType.DEVELOPER == user_type):
            buttons_template = ButtonsTemplate(
                text=f'(Developer)\n', actions=[
                    MessageAction(label='班の予算額を確認', text='group_check'),
                    MessageAction(label='check prof', text='profile'),
                    MessageAction(label='omikuji', text='!omikuji'),
                    MessageAction(label='help', text='help'),

                ])
            template_message = TemplateSendMessage(
                alt_text=f'(Developer)\n更新日時:{WAKE_TIME}\n起動時更新:{success_str}', template=buttons_template)
            line_bot_api.reply_message(event.reply_token, template_message)
        elif (UserType.NORMAL_USER == user_type):
            data = manager.getFromId(profile.user_id)
            buttons_template = ButtonsTemplate(
                text=f'ようこそ {data.name}さん', actions=[
                    MessageAction(label='滞納額を確認', text='check'),
                    MessageAction(label='班の予算額を確認', text='group_check'),
                    MessageAction(label='help', text='help'),
                    MessageAction(label='see_history', text='his'),

                ])
            template_message = TemplateSendMessage(
                alt_text=f'ようこそ {data.name}さん', template=buttons_template)
            line_bot_api.reply_message(event.reply_token, template_message)
        elif (UserType.WELLKNOWN_USER == user_type):
            data = manager.getFromId(profile.user_id)
            buttons_template = ButtonsTemplate(
                text=f'ようこそ {data.name}さん(well_known)', actions=[
                    MessageAction(label='滞納額を確認', text='check'),
                    MessageAction(label='班の予算額を確認', text='group_check'),
                    MessageAction(label='help', text='help'),

                ])
            template_message = TemplateSendMessage(
                alt_text=f'ようこそ {data.name}さん(well_known)', template=buttons_template)
            line_bot_api.reply_message(event.reply_token, template_message)
        elif (UserType.ADMINISTRATOR == user_type):
            data = manager.getFromId(profile.user_id)
            buttons_template = ButtonsTemplate(
                text=f'ようこそ {data.name}さん(admin)', actions=[
                    MessageAction(label='滞納額を確認', text='check'),
                    MessageAction(label='班の予算額を確認', text='group_check'),
                    MessageAction(label='help', text='help'),
                    MessageAction(label='crash', text='crash'),

                ])
            template_message = TemplateSendMessage(
                alt_text=f'ようこそ {data.name}さん(admin)', template=buttons_template)
            line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'crash' and (UserType.DEVELOPER == user_type or UserType.ADMINISTRATOR == user_type):
        notifer.output('サーバをクラッシュさせます...')
        template_text_send('Goodbye', event)
        while (True):
            pass
    elif text == 'see connection' and (UserType.DEVELOPER == user_type or UserType.ADMINISTRATOR == user_type):
        notifer.output('output connect....')
        notifer.output(manager.outputIdConnection())
        buttons_template = ButtonsTemplate(
            title=f'output success', text=f'back to menu ?', actions=[
                # URIAction(label='Go to line.me', uri='https://line.me'),
                # PostbackAction(label='Back to menu', data='menu'),
                # PostbackAction(label='ping with text', data='ping', text='ping'),
                MessageAction(label='Back to menu', text='menu')
            ])
        template_message = TemplateSendMessage(
            alt_text='Buttons alt text', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'group_check' and user_type != UserType.EXTERNAL_USER:
        output = ''

        for i in manager.groups:
            output += f'{i.name} : {i.money:,}円\n'
        notifer.output(output)
        template_message_send(output, event)

    else:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='すいません　コマンドが認識できませんでした！'))





if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    # create tmp dir for download content
    make_static_tmp_dir()
    try:
        app.run(debug=options.debug, port=options.port)
    except:
        notifer.output(traceback.format_exc())
