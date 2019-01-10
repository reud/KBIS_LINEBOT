## KBISのセットアップ方法

### 　やる事
#### ・LINE_BOTの作成
#### ・Herokuアカウントの作成と設定
#### ・LINE Notify トークンの取得

### 初めに
BashっていうWindowsでいうコマンドプロンプトみたいな奴(厳密には違う)の操作が多発します。　Mac,Linuxでは標準で付いているのですがWindowsには付いてないので、Windowsでは[Windows Subsystem for Linux](http://www.atmarkit.co.jp/ait/articles/1608/08/news039.html)というものをインストールしてください。(ここからはWSLと呼びます)
仕組みとかは理解しなくて大丈夫です。
Ubuntuって奴をインストールしてください。
インストール後はユーザアカウントの作成とかあるので指示通りに進めてください

設定完了後に
```
(PC名):~$
```
このような感じになっていたら完了です。

以降　
```
$ ls
```
って書いてあった場合はそこにlsって打ってエンターキーを押して実行してくださいって事です。
こんな感じにコマンドを打って操作していきます。



### LINE_BOTの作成
[【第1回】Messaging APIを使うためにチャンネルを作成する](https://masatoshihanai.com/php-line-bot-01/)
を参考に進めてください。

　進めるにあたって以下の点に注意してください。

・結構頻繁にLINE Developersのサイトがアプデ入るため画面がちょっと違う可能性もあります。

・LINE-BOTの名前は　KBIS-LINEBOT でお願いします。

・プランはフリーにしてください。

・大業種、小業種などは好きにどうぞ

・BOT作成後、LINE Developers でChannel SecretとChannel Access Tokenをメモしておく。
### ・Herokuアカウントの作成
Herokuが何かと言うと簡単に言うと、サーバを無料で貸してくれるサービスです。
[こちら](https://www.heroku.com/)
からSign Up を選んでアカウントを作成してください。
ここからは
Bashの作業です。
以降の説明は全て　UbuntuかWindows(WSL)で説明を行います。
```
$ wget -qO- https://cli-assets.heroku.com/install-ubuntu.sh | sh
```
これでHerokuをインストール出来ます。
インストール出来たか確認するためには
```
$ heroku --version
```
と打ち込んでバージョンが見えたら、成功しています。
インストールが終わったら実際にログインしてみましょう。

```
$ heroku login
```

と入力してHerokuアカウントのメアドとパスワードを入力してログイン出来ればHerokuを使う準備は完了です。

このままHerokuの設定を続けていきましょう。

GitHubからKBISのコードを取得しましょう

```
$ git clone https://github.com/reud/KBIS_LINEBOT
```

取得したらKBIS_LINEBOTのフォルダに移動するためcdコマンドします
```
$ cd KBIS_LINEBOT
```
次にこのコードをHerokuのアプリとして登録します。
```
$ heroku create kbis-linebot_DEP
```
名前はcreateの後になります(今回はkbis-linebot_DEP)。　なんでも良いです。
コマンド実行後、アプリケーションのURL
'https://"アプリ名".herokuapp.com/'
が出力されるのでどっかにメモっておいて下さい。

あとはもうちょっとです。

#### ・LINE Notify トークンの取得
[[超簡単]LINE notify を使ってみる](https://qiita.com/iitenkida7/items/576a8226ba6584864d95)
KBISのログなどはLINE Notifyと言うサービスにより通知されます。
上記のURLを参考にしてLINE Notifyのアクセストークンを取得し、メモっておいて下さい。
通知を送信するルームは好きなところにどうぞ、個人情報だらけなので信頼できる人間のみがいる部屋か自分だけで良いと思います。

#### ・Herokuに登録したKBISとLINEの設定を繋げてデプロイ
もうちょっとです。

まずは今までにメモってきた

・LINE Notifyのアクセストークン

・Channel Secret

・Channel Access Token

を手元においてください。

あとは会計管理者から、googledriveの共有ファイルであるexcel-id.txtとSpecialUserIdsと会計管理簿.xlsxのidを聞いてください。(idの教え方は今度書く)

以上6つの情報をHerokuのアプリに教えてあげます。

ここでherokuに教える形式が

```
$ heroku config:set ENV_VAR_NAME="value"
```

このようになっています。　何が言いたいかって言うと、　情報の前後に"が付くって事です。

これ以上説明しても混乱するので具体的な設定方法を伝えます。

```
$ heroku config:set LINE_CHANNEL_SECRET="Channel Secret"
$ heroku config:set LINE_CHANNEL_ACCESS_TOKEN="Channel Access Token"
$ heroku config:set NOTIFER_TOKEN="LINE Notifyのアクセストークン"
$ heroku config:set MANEGE_BOOK="会計管理簿.xlsxのid"
$ heroku config:set SPECIALUSERIDS="SpecialUserIdsのid"
$ heroku config:set EXCELIDS="excel-id.txtのid"
```
６行もコードがあってしんどいですが一個一個設定してください。

設定が完了した場合は　あとは　とどめです。

```
$ git push heroku master
```
これを実行すればherokuにKBISがデプロイされて、自動的に実行されます。
LINE NotifyからKBISが起動したという通知が来ればセットアップは終了です。

お疲れ様でした。
