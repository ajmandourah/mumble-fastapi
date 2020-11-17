# mumble-fastapi
### A FlaskCVP but with FASTAPI and Python 3.X instead.

As an alternative to FlaskCVP, this script updated to be compatible with Python 3.X instead. It uses FASTAPI to offer a better async performance. additionally I added a another path called widget which can be used as a URL in JSON viewer mobile apps. I personally use 'JSON response widget' which let you create a widget in your Android desktop giving you an overview of connected users.

# Usage:

Clone the repo, install the requirements and run it with hypercorn.

```
git clone https://github.com/ajmandourah/mumble-fastapi.git
cd mumble-fastapi
pip3 install -r requirements.txt
hypercorn mumble-fastapi:app --bind 0.0.0.0:3000 # Or use your host:port
```
