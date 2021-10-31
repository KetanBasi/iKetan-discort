# iKetan-dct
iKetan Discord Bot

## How-To

Install latest Python 3
Windows: Check python.org/downloads
```bash
sudo apt install python3
```
Site note: Python 3.9+ ***Cannot*** be used on Windlws 7 or earlier

Install all required Python packages listed in requirements.txt
```bash
pip install -r requirements.txt
```

Add environment variable manually or create .env file, which contains:
1. ***"iketan-token"***: Discord bot token from Discord dev site
2. ***"owner"***: Your Discord user ID
3. ***"tenor"***: Tenor token for gif funcs
4. ***"unsplash"***: Unsplash token for image/wallpaper search
5. ***"notion"***

Run it
```bash
python3 main.py
```
