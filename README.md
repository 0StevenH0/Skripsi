This Repository does not include Bert model, no need to install it, we install it for you

![alt text](https://github.com/0StevenH0/Skripsi/blob/dev/Proposal_Graph.jpeg)

If a function does not have TODO, you can ignore it and work on that later

> If you're in pycharm ensure that you have changed your python environment to .venv in this folder
## To Run:
- run setup.py, switch to environment created (should be printed when you run it in terminal)
- on terminal :  run_server.py, dont stop it
- to start : uvicorn main:app --reload
  - this will download model, establish connection, set database
- to hit api : http://127.0.0.1:8000/response