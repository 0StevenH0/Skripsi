This Repository does not include Bert model, no need to install it, we install it for you

![alt text](https://github.com/0StevenH0/Skripsi/blob/dev/Proposal_Graph.jpeg)

If a function does not have TODO, you can ignore it and work on that later

### Important

> If you're in pycharm ensure that you have changed your python environment to .venv in this folder

> Manager should handle Task Related On Initializing (IK normal manager don't do this)

> Controller should handle task related to manipulating

> To Ease Tracking Result, all record are automatically stored in records folder with @Record decorator, you are expected to already know the order of each record to read, so i will not explain it ☜(⌒▽⌒)☞☜(⌒▽⌒)☞.

## To Run (step by step)

- run setup.py, switch to environment created (should be printed when you run it in terminal)
- run main.py, it should initialize everything
- to start : uvicorn main:app --reload
  - if you cant run this, uninstall fastapi, then pip install fastapi==0.103.0 uvicorn
- to hit api : http://0.0.0.0:8000/response
- use ur own api key on settings -> google api key
  - to get api key: use google ai studio
- to download model weight, remind me, i don't upload yet, bcs huge size
