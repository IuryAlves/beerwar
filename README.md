# beerwar
Python war game server

## Install

    pip install -r requirements.txt


## Run

    python server.py


## API

- `/imalive/` POST (name: 'w', direction: 'u')
- `/point/<direction>` POST
- `/goto/<direction>` POST
- `/junp/<direction>` POST
- `/shoot/<direction>/` POST

### Direction

- `u` up
- `d` down
- `l` left
- `r` right
