This Repository does not include Bert model, no need to install it, we install it for you

![alt text](https://github.com/0StevenH0/Skripsi/blob/dev/Proposal_Graph.jpeg)

If a function does not have TODO, you can ignore it and work on that later

### Important
> If you're in pycharm ensure that you have changed your python environment to .venv in this folder

> Manager should handle Task Related On Initializing (IK normal manager don't do this)

> Controller should handle task related to manipulating 

## To Run:
- run setup.py, switch to environment created (should be printed when you run it in terminal)
- to start : uvicorn main:app --reload
  - this will download model, establish connection, set database
- to hit api : http://127.0.0.1:8000/response