# Azure Functions の Python ランタイムを使ったサンプル

Azure App Service のひとつである Functions を Python ランタイムを使い、ローカルマシン上の
プロジェクトで開発し、クラウドにデプロイする。

[Azure Functions のドキュメント](https://docs.microsoft.com/ja-jp/azure/azure-functions/)


## VS code にプロジェクトを作成する

ローカルで開発するためには、[コマンドラインまたはターミナル上でやる](https://docs.microsoft.com/ja-jp/azure/azure-functions/functions-create-first-azure-function-azure-cli)か、
[Visual Studio Code 上でおこなう](https://docs.microsoft.com/ja-jp/azure/azure-functions/functions-create-first-function-vs-code)。

いずれにしても、拡張機能等をインストールする必要がある。ここでは、VS code を使って開発する。

拡張機能のインストール等の準備が終わったら、プロジェクトのルートとなるフォルダを作成する。

```shell
$ mkdir azure-functions-sample-in-python
```

[ドキュメント](https://docs.microsoft.com/ja-jp/azure/azure-functions/functions-create-first-function-vs-code)のとおりにプロジェクトを作成するが、
そのとき、上で作ったフォルダを指定する。また、言語は Python を選択する。

Azure の Functions は、`Function app` というリソース単位で作成されるわけだが、ここで作成する
プロジェクトがそれに対応するものになる。プロジェクトを作成すると、プロジェクトルートはだいたい
次のような構成になっている。

```shell
.
├── .env
│   ├──
│   ...
├── .funcignore
├── .git
│   ├──
│   ...

├── .gitignore
├── .vscode
│   ├── extensions.json
│   ├── launch.json
│   ├── settings.json
│   └── tasks.json
├── host.json
├── local.settings.json
└── requirements.txt
```

`.git/` があることからわかるようにすでに Git で管理可能な状態になっている。また `.env` は Python の
仮想環境だ。`local.settings.json` は、Azure 上の `Function app` のアプリケーション設定に対応するもので、
このプロジェクトで作成した関数をローカルで実行する際に使用する。初期状態は次のようになっている。

```json
{
  "IsEncrypted": false,
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsStorage": ""
  }
}
```

**AzureWebJobsStorage** に対する設定値は、デフォルトでは Azure 上の `Function app` リソースを作成するときに
指定あるいは作成するストレージアカウントの接続文字列になる。ローカルなので空文字列になっているが、Portal 上で
`Function app` を作成してアプリケーション設定を確認すると、そのようになっている。このストレージは、関数のコードや
設定値を格納するために必須のものだ。


## HttpTrigger

[Visual Studio Code を使用した初めての関数の作成](https://docs.microsoft.com/ja-jp/azure/azure-functions/functions-create-first-function-vs-code) にそって Http リクエストで
トリガされる関数を作成するが、言語は Python を選択する。

作成時に認証レベルとして、`Anonymous`, `Admin`, `Host` が選べるのだが、これは Http リクエストに
どの認証用のキーをつけるか、あるいはつけないかを選ぶものだ。ローカルで実行しやすいように `Anonymous` を
選択するが、Portal 上で `Function app` 内の関数の設定で切り替えたり、キーを変更したりできる。

認証については、[承認キー](https://docs.microsoft.com/ja-jp/azure/azure-functions/functions-bindings-http-webhook#authorization-keys) を参照。

関数を作成すると、関数名のフォルダが作成され、そこに関数本体のコードである `__init__.py`、およびトリガとバインディングの設定ファイル
である `function.json` が作成される。

[Azure Functions でのトリガーとバインドの概念](https://docs.microsoft.com/ja-jp/azure/azure-functions/functions-triggers-bindings)


## ローカルでの実行

VS code のデバッガで実行する。


## Azure へ発行（デプロイ）する

VS code 上からプロジェクトをデプロイするとき、デプロイ先となる `Function app` を一緒に作成することもできるし、
先に作成しておいた `Function app` にデプロイ（上書き）することもできる。

デプロイと一緒に作成する場合、作成した `Function app` は従量課金プランの `Function app` となった。`Function app` 名を
**functions-linux** とし、ロケーションを米国西部にすると、**WestUSLinuxDynamicPlan** という名前の `App service プラン`
リソースが同じロケーションに自動で作成された。これ以後に同じロケーションに従量課金プランの Linux 用 `Function app` を作成すると
この `App service プラン` が使用されるのだろう。

`Function app` は App service のひとつなので、App service プランというリソースに所属しないといけない。このとき、
上で見たように従量課金プランの App service か本来の App service プランの二択がある。

[Azure Functions のスケールとホスティング](https://docs.microsoft.com/ja-jp/azure/azure-functions/functions-scale)

ローカルプロジェクトを Azure へデプロイしたとき、`local.settings.json` の内容は（デフォルトでは）アップされない。したがって、
前もって `Function app` リソースをつくっておいて、そこへデプロイした場合を除き、デプロイ後に Portal 上でその `Function app` の
アプリケーション設定から（必要な設定があるなら）設定しなければならない。


## BusyLoop

３秒間ビジーループして、プロセスID をレスポンスする HttpTrigger 関数。先程の HttpTrigger もプロセスID をレスポンスするように
して実験してみた。

従量課金プランで試した場合、BusyLoop と HttpTrigger は各々常に同じプロセスID を返すが、両者のプロセスID は異なっている。
BusyLoop と HttpTrigger は各々並行して走ることができるが、BusyLoop への複数のリクエストが並行して走ることはなかった。
ただし、ビジーループでなく、sleep で停止するようにすると並行して走れた。

従量課金プランでなく、Portal 上で OS が Linux, ランタイムが Python の `App service プラン` リソースを作成し、
そこに所属する `Function app` を作成して、そこへデプロイして試してみると、BusyLoop も HttpTrigger が返す PID は
同じになり、常に同じ PID を返した。そして、BusyLoop どうしだけでなく、BusyLoop と HttpTrigger も並行実行はできなくなった。

したがって、従量課金でない `App service プラン` では `Function app` 内の関数はすべて１つの Python プロセスを
使っており、従量課金では関数ごとに異なるプロセスを使っている。そして、Python の GIL のせいで CPU バインドなビジーループでは
並行処理ができなかったというわけだ。

[Azure Functions の Python 開発者向けガイド](https://docs.microsoft.com/ja-jp/azure/azure-functions/functions-reference-python)

[Azure Functions の Python 開発者向けガイド#非同期](https://docs.microsoft.com/ja-jp/azure/azure-functions/functions-reference-python#async)

上の非同期に関する記述は、従量課金プランには当てはまらないのだろう。


## BlobTrigger

[Azure Blob Storage によってトリガーされる関数の作成](https://docs.microsoft.com/ja-jp/azure/azure-functions/functions-create-storage-blob-triggered-function)

HttpTrigger 関数と同じようにして VS code 上で Blob ストレージからトリガされる関数を作成できる。作成するとき、
拡張機能のインストールを求められる。HttpTrigger 以外では拡張機能が必要らしい。

作成するとき、使用する Blob コンテナ名とパス名、およびストレージアカウントのアプリ設定名を聞かれる。それは作成された関数の
`function.json` に反映される。たとえば次のようになる。

```json
{
  "scriptFile": "__init__.py",
  "bindings": [
    {
      "name": "myblob",
      "type": "blobTrigger",
      "direction": "in",
      "path": "samples-workitems/foo/{file_name}",
      "connection": "AzureWebJobsStorage"
    }
  ]
}
```

"connection" に "AzureWebJobsStorage" という文字列が設定されているがこれはアプリ設定名なので、`local.settings.json` 内で
この文字列のキーに対して、使用するストレージアカウントの接続文字列をセットしなければならない。ローカルでテスト実行するにはそれが
必要である。Azure 上にデプロイして実行する場合、その `Function app` のアプリケーション設定で設定しなければならない。

[Azure Functions における Azure Blob Storage のバインド](https://docs.microsoft.com/ja-jp/azure/azure-functions/functions-bindings-storage-blob)



## QueueTrigger

Azure Queue Storage のキューにメッセージが追加されたことをトリガに実行される QueueTrigger 関数を作成できる。作成時に
指示するパラメータは BlobTrigger と似たようなものだ。

[Azure Functions における Azure Queue Storage のバインド](https://docs.microsoft.com/ja-jp/azure/azure-functions/functions-bindings-storage-queue)


## PutMessage2Queue

Http リクエストで送信されてきたパラメータを Queue ストレージのキューへメッセージとして追加する HttpTrigger 関数。
キューに出力するために出力バインディングの設定を `function.json` に定義し、それを使うように関数本体のコードを変更せねばならない。

[Azure Functions の Python 開発者向けガイド#出力](https://docs.microsoft.com/ja-jp/azure/azure-functions/functions-reference-python#outputs)


## QueueTriggered_VmStarter

キューから VM 名が入ったメッセージを取り出して、その VM をスタートさせる QueueTriggered 関数。

VM を操作するための認証情報が必要になるので、前もってそのための Service principal を作成しておかねばならない。

[方法:リソースにアクセスできる Azure AD アプリケーションとサービス プリンシパルをポータルで作成する](https://docs.microsoft.com/ja-jp/azure/active-directory/develop/howto-create-service-principal-portal)

作成した認証情報を関数コードから利用できるようにするために `Function app` のアプリケーション設定に定義しておかなくてはいけない。
ローカルなら `local.settings.json` 内に定義する。VM が所属するリソースグループ名も定義しておく。アプリケーション設定の設定値には
関数コード内からは環境変数としてアクセスできる。

VM 操作用の Python モジュールが必要になるので、仮想環境内で次のことを実行する。

```shell
$ pip install azure-common azure-mgmt-compute
$ pip freeze >requirements.txt
```

VM へスタートリクエストを送るかどうかを決めるのに、[VM のライフサイクルと状態](https://docs.microsoft.com/ja-jp/azure/virtual-machines/linux/states-lifecycle)を考慮している。



## local.settings.json のデプロイ

`Function app` 内のすべての関数は、`Function app` のアプリケーション設定に定義されている設定値を自分のトリガおよび
バインディング設定ファイルである `function.json` から使うし、関数コードから環境変数でアクセスできる。

ローカル環境でプロジェクトを動かすときに使用するアプリケーション設定が `local.settings.json` だ。プロジェクト作成直後には

```json
{
  "IsEncrypted": false,
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsStorage": ""
  }
}
```

であり、これが最低限の内容になる（AzureWebJobsStorage は空なのでなくてもいい）。HttpTrigger 関数だけなら
これでも十分だが、BlobTrigger 関数等の場合、使用するストレージアカウントの接続文字列を設定値として定義しないといけない。
関数コード内で独自に使用する設定値もここに定義する。

プロジェクトを Auzre にデプロイしても、`local.settings.json` はデフォルトではアップされないので、必要な設定は
Portal 上で `Function app` のアプリケーション設定をしないといけない。

`local.settings.json` を Azure 上の `Function app` にデプロイしたいなら、次のようにする。

```shell
$ func azure functionapp publish {Azure 上の Function app の名前} --publish-local-settings-only -o --overwrite-settings -i
```

こうすると、指定した `Function app` のアプリケーション設定に `local.settings.json` の内容が上書き、かつマージ
される。`--overwrite-settings -i` のオプションがないと、同じ設定項目があった場合、それを上書きするかどうか確認の
プロンプトが出る。


## local.settings.json の暗号化

`local.settings.json` の中身は、ローカルマシンのキーを使用して暗号化できる。暗号化するには、次のようにする。

```shell
$ func settings encrypt
```

こうすると、現在のプロジェクトの `local.settings.json` の中身が暗号化される。復号化するには、

```shell
$ func settings decrypt
```

とすればいい。


## GitHub へ push する

作成直後のプロジェクトは git のローカルリポジトリが設定済みなので、commit し、好きなリモートリポジトリへと push できる。

GitHub を使うなら、ブラウザ上で `azure-functions-sample-in-python` という空のリポジトリを作成し、作成後に
表示される指示にしたがって次のようにすればいい。

```shell
$ git remote add origin git@github.com:fortune/azure-functions-sample-in-python.git
$ git push -u origin master
```

もちろん、前もって鍵の生成や `~/.ssh/config` ファイルで Github 向けの設定が済んでいなければならない。


## ソース管理の方針

`local.settings.json` はソース管理から除外するように `.gitignore` ファイルで最初から設定されている。
`local.settings.json` にはストレージアカウントへの接続文字列等、秘密にすべき情報が含まれることがあるので
これは当然のことだ。

各開発者のテスト環境やステージング環境、本番環境ごとに Azure 上の `Function app` は別々になるから、
それらのアプリケーション設定も `local.settings.fortune.json`, `local.settings.staging.json`, `local.settings.microsoft.json` などのように個別に作成し、それらもソース管理からは除外する。そして、デプロイするときに
`local.settings.json` にコピーして、**local.settings.json のデプロイ** で述べたやり方でアップしてやればいい。

もしくは、ローカルのアプリ設定はデプロイせずに、Portal 上でアプリケーション設定をし、それをダウンロードするように
してもいいかもしれない。
