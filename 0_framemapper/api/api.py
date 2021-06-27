import time
from flask import Flask
from glob import glob
import os
import json

app = Flask(__name__, static_url_path='/static')

if os.path.exists('./db.json'):
    state = json.load(open('./db.json'))
else:
    state = {
        '360': { }
    }


@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/get_img_pair')
def get_img_pair():

    all_images = [x.split('frame')[1].split('.png')[0] for x in glob('./static/eyetracker/*.png')]
    notdone = [x for x in all_images if x not in state['360']]

    print(state) 

    return {
        'basePath': "static/360.jpg",
        'baseId': '360',
        'curImgPath': f"static/eyetracker/frame{notdone[0]}.png",
        
        'curImgId': notdone[0],
        'left': len(notdone),
    }

@app.route('/set_img_pair/<baseId>/<curImg>/<x>/<y>')
def set_img_pair(baseId, curImg, x, y):

    state[baseId][curImg] = (int(x), int(y))
    with open('db.json', 'w') as db:
        json.dump(state, db)

    return {'ok': 'ok'}