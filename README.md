# QuartOpenID

A simple webapp for testing the feasibility for integrating OpenID with Quart

## Pre-requisites

```console
$ pip install quart
```

## Run

```console
$ quart run
```

The app also runs with the default VSCode debugger. Use the following launch.json

```
"configurations": [
    {
      "name": "Python: Quart",
      "type": "python",
      "request": "launch",
      "module": "quart",
      "env": {
        "FLASK_APP": "app.py",
        "FLASK_DEBUG": "1"
      },
      "args": ["run"],
      "jinja": true,
      "justMyCode": true
    }
  ]
```
