# Headless YouTube Subscriber Bot

![YouTube](./youtube.jpg)

## Project Structure

```
.
├── README.md
├── UserAgents.txt
├── debug.log
├── drivers
│   ├── chromedriver.exe
│   ├── geckodriver.exe
│
├── geckodriver.log
├── proxylist.txt
├── requirements.txt
├── src
│   ├── bot.py
│   ├── settings.py
│   └── utils.py
├── youtube.jpg
├── youtube_subscriber.log
└── .credentials

```

## Run project

Before running the project make sure that all the variables in `settings.py` file are correct and you have following files in the project directory:

- .credentails (Which contains credentials, i.e., `email:password`)
- proxylist (Which contains http proxy in this format: `host:port:user:password`)

And most important thing is that you have selenium drivers in the `drivers` directory.

You can change the Target channel from `settings.py` file to set your youtube channel as a target.

After everything is done, run the following command:

```bash
python -m src.bot
```

You will find the logs in the `youtube_subscriber.log` file.
