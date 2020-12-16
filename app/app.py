import pymysql
from flask import jsonify
from flask import flash, request
from flaskext.mysql import MySQL
import pymysql
from flask import jsonify
from flask import flash, request

from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics
import logging
import sys
import json_logging
import json
import os

# checking the port mentioned in env, if not then let's exit
if os.environ.get("SERVE_PORT") == None or os.environ.get("DB_HOST") == None:
    print("Environment variable SERVE_PORT or DB_HOST is not defined. Exiting.")
    exit()

app = Flask(__name__)



# logging
json_logging.init_flask(enable_json=True)
json_logging.init_request_instrument(app)
# Init logger
logger = logging.getLogger("test-logger")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

# For collecting metrics from flask to prometheus
metrics = PrometheusMetrics(app)


mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ.get("DB_PW")
app.config['MYSQL_DATABASE_DB'] = 'sampledb'
app.config['MYSQL_DATABASE_HOST'] = os.environ.get("DB_HOST")
mysql.init_app(app)

'''
Get all documents
'''


@app.route('/guests')
def users():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT firstname, lastname, email FROM myguests")
    # pass
        rows = cursor.fetchall()
        resp = jsonify(rows)
        

        resp.status_code = 200
        logger.info("Logging response", extra={
                'props': {"response": resp.json}})
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


if __name__ == '__main__':

    # Running the app
    app.run(host='0.0.0.0', port=os.environ.get("SERVE_PORT"))
