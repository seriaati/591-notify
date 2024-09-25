# 591-notify

591 中古屋爬蟲 + LINE Notify 通知

## 前置作業

你需要:

- Python 3.11+
- 一個 [LINE Notify](https://notify-bot.line.me/my/) Token
- 想要爬取的 591 中古屋網址 (例如: <https://sale.591.com.tw/?shType=list&regionid=17&station=4341,4340,4342,4343,4335&metro=238&price=750_1000,1000_1250&pattern=2&label=9,4&shape=2&totalRows=192&firstRow=0>)

## 安裝

```bash
pip install .
playwright install
```

## 使用

不通知 LINE Notify (測試程式是否運行正常時用):

```bash
python run.py --url <591 網址>

# 例如
python run.py --url "https://sale.591.com.tw/?shType=list&regionid=17&station=4341,4340,4342,4343,4335&metro=238&price=750_1000,1000_1250&pattern=2&label=9,4&shape=2&totalRows=192&firstRow=0"
```

要通知 LINE Notify:

```bash
python run.py --url <591 網址> --token <LINE Notify Token>

# 例如
python run.py --url "https://sale.591.com.tw/?shType=list&regionid=17&station=4341,4340,4342,4343,4335&metro=238&price=750_1000,1000_1250&pattern=2&label=9,4&shape=2&totalRows=192&firstRow=0" --token "ABCDEF1234567890"
```

要使用代理的話，請在 `.env` 中設定以下環境變數:

```env
PROXY_USERNAME=
PROXY_PASSWORD=
PROXY_SERVER=
```

## 注意事項

第一次執行的時候不會發送 LINE Notify 通知。第二次及之後執行的時候，如果發現新的房屋，就會發送通知。
