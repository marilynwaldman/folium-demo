import requests
import folium
import geocoder
import string
import os
import json
from functools import wraps, update_wrapper
from datetime import datetime
from pathlib import Path
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *
from dominate.tags import img


from ediblepickle import checkpoint
from flask import Flask, render_template, request, redirect, url_for, send_file, make_response


###############################################
#      Define navbar with logo                #
###############################################
logo = img(src='./static/img/logo.png', height="50", width="50", style="margin-top:-15px")
#here we define our menu items

topbar = Navbar(logo,
                Link('IXWater','http://ixwater.com'),
                View('Home', 'main')     
                )

# registers the "top" menubar
nav = Nav()
nav.register_element('top', topbar)




app = Flask(__name__)
Bootstrap(app)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.vars = {}


@app.route('/')
def main():
  return redirect('/index.html')

@app.route('/index.html', methods=['GET'])
def index():
  if request.method == 'GET':
    #return render_template('input.html')
    map_name = f"CenCal.html"
    #have to set map path - used by template
    map_path = os.path.join(app.root_path, 'static/' + map_name)
    app.vars['map_path'] = map_path
    
    if Path(map_path).exists():
        return render_template('display.html')
    else:     
        return redirect('/maperror.html')

    pass

@app.route('/maps/map.html')

def show_map():
  map_path = app.vars.get("map_path")
  map_file = Path(map_path)
  if map_file.exists():
    return send_file(map_path)
  else:
    return render_template('error.html', culprit='map file', details="the map file couldn't be loaded")

  pass

@app.route('/error.html')
def error():
  details = "There was some kind of error."
  return render_template('error.html', culprit='logic', details=details)

@app.route('/apierror.html')
def apierror():
  details = "There was an error with one of the API calls you attempted."
  return render_template('error.html', culprit='API', details=details)

@app.route('/maperror.html')
def geoerror():
  details = "Map not found."
  return render_template('error.html', culprit='the Map', details=details)

nav.init_app(app)

if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0')