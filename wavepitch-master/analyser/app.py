

import flask
import argparse
import sys, os

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))

from analyser.pitchogram import pitchogram_from_url 


app = flask.Flask(__name__)
DEFAULT_URL = 'https://s3-eu-west-1.amazonaws.com/music-analysis/rise_like_a_phoenix_first_15s.wav'


@app.route("/")
def index():
    
    default_url = DEFAULT_URL
    return flask.render_template("index.html", active_page='main', default_url = default_url)



@app.route("/about")
def about():
    
    return flask.render_template("about.html", active_page='about')
 


@app.route("/analyse/", methods=["POST"])
def analyse():
    """
    On request, this returns a list of ``ndata`` randomly made data points.

    :param filename: 
        wav file to load

    :returns data:
        A JSON with
          note_names: array of note names
          time_values:  array of time in seconds
          active_notes:  whether note n is detected at time interval t

    """
    try:
        
        url = flask.request.form["url"]
        filtered = flask.request.form["filtered"]
        
        
        if not url.startswith("http://") and not url.startswith("https://")  :
            raise Exception('Invalid URL, url start with http/https required')
        #print url
        #payload = '{}'
        
        payload = pitchogram_from_url(url, 1*1024*1024, filtered = (filtered == "true"))
        
        return payload
    except:
        flask.abort(400)
        pass
    



    
    
    
    

if __name__ == "__main__":
    import os

    port = 8000
    
    app.debug = True
    app.run(port=port, host='0.0.0.0',debug=True)
    
    