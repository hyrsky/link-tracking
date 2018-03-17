# link-tracking
Track clicked links and report results to google sheets

## Install instructions ##

1. Get Google Drive API credentials: https://gspread.readthedocs.io/en/latest/oauth2.html
2. Set ```GOOGLE_SHEETS_ID``` environment variable

```
virtualenv venv --python=python3.6
source venv/bin/activate
pip install -r requirements.txt
```

## Deploy ##

```
(inside virtualenv)
zappa deploy production
```

## Testing ##

```
curl -X GET -v "localhost:8000/?id=1337&val=666&url=https%3A%2F%2Fgoogle.com"
```
