CloudRunでスクレーパー動かして現物の保有銘柄CSVを取得してGCSに保存します。

[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run)

上記ボタンをポチると認証要のCloudRunアプリがデプロイされるので、**CloudRun起源元** の役割を付与したサービスアカウントを使って
CloudSchedulerから `/sbiscrape`、 `/rakutenscrape` に向けて認証付きリクエストを定期送信しましょう。
https://cloud.google.com/run/docs/triggering/using-scheduler?hl=ja

また、デプロイ中にCloudShellで以下の環境変数を設定してください。
- SBI_ID
- SBI_PW
- SBI_BUCKET
- RAKUTEN_ID
- RAKUTEN_PW
- RAKUTEN_BUCKET
