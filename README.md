KBIS on LINEBOT
====

Kohken Blance Inquary System

## Description
LINE BOTを用いた部内会計情報の照会を行うアプリケーション
## Requirement
Python 3.6.7

see [requirements](https://github.com/reud/KBIS_LINEBOT/blob/master/requirements.txt)
## Setup


[LINE Developers](https://developers.line.biz/ja/)

[Heroku](https://jp.heroku.com/)

の登録してください。

HerokuはCLIもインストールして下さい。
#### Windows
`https://devcenter.heroku.com/articles/heroku-cli
#### Mac

```
$ brew install heroku/brew/heroku
```

#### Ubuntu
```
$ sudo snap install --classic heroku
```


##### その後


LINE_Developers登録後にLINE_BOTを作成してLINE_CHANNEL_SECRETとLINE_CHANNEL_ACCESS_TOKENを取得して下さい。
LINE Notifyを作成してLINE_NOTIFY_TOKENを取得してください

LINE_BOT,LINE Notifyの作り方自体はサイト探せばめっちゃいっぱいあるので割愛させて頂きます・

あとは動作環境に合わせて以下のように操作してください


### Local + Ngrok
```
$ export LINE_CHANNEL_SECRET=YOUR_LINE_CHANNEL_SECRET
$ export LINE_CHANNEL_ACCESS_TOKEN=YOUR_LINE_CHANNEL_ACCESS_TOKEN
$ export NOTIFER_TOKEN=YOUR_LINE_NOTIFY_TOKEN
$ export MANEGE_BOOK='Google driveの管理簿ファイルの共有id'
$ export SPECIALUSERIDS='Google driveの特別ユーザファイルの共有id'
$ export EXCELIDS='Google driveのexcel-id.txtの共有id'

$ pip install -r requirements.txt

$ ngrok http (port)

$ python app.py
```


### Heroku
```

$ heroku create

$ heroku config:set LINE_CHANNEL_SECRET=YOUR_LINE_CHANNEL_SECRET
$ heroku config:set LINE_CHANNEL_ACCESS_TOKEN=YOUR_LINE_CHANNEL_ACCESS_TOKEN
$ heroku config:set NOTIFER_TOKEN=YOUR_LINE_NOTIFY_TOKEN
$ heroku config:set MANEGE_BOOK='Google driveの管理簿ファイルの共有id'
$ heroku config:set SPECIALUSERIDS='Google driveの特別ユーザファイルの共有id'
$ heroku config:set EXCELIDS='Google driveのexcel-id.txtの共有id'



$ git push heroku master
```

urlをLINE_BOTのwebhook URLに設定すれば完了です。(LINE_BOTの設定画面から設定できます)

Herokuを使用する場合、無料枠だと30分間アクセスがないとシャットダウンされてしまいます。
なのでHeroku Schdulerを使うか、ラズパイとかで10分ごとにwebhook URLにcurlコマンドを飛ばすなどして、アクセスしてあげてください。



## Install
```
$ git clone https://github.com/reud/KBIS_LINEBOT.git
```




## Author

[reud](https://github.com/reud)
