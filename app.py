from flask import Flask, jsonify
from flask import request
from flask.ext.mongoengine import MongoEngine



app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {'DB': 'thermostats' }
db = MongoEngine(app)

class Temperature(db.Document):
    temp = db.FloatField()
    timestamp = db.IntField()

@app.route('/temperature', methods = ['POST'])
def post_temperature():
    # POST A TEMP FROM REQUEST ARGS
    temperature = request.args.get('temperature', None)
    timestamp = request.args.get('timestamp', None)

    if temperature and timestamp:
        try:
            temperature = float( temperature )
        except ValueError:
            return jsonify( { 'return_code': 'Error! Temperature invalid.' } )
        try:
            timestamp = int( timestamp )
        except ValueError:
            return jsonify( { 'return_code': 'Error! Timestamp invalid.' } )
        
        t = { 'temp':temperature,
                'timestamp':timestamp }
        try:
            Temperature(**t).save()
            return jsonify( t )
        except:
            return jsonify( { 'return_code': 'Error! Database error.' } )

    else:
        return jsonify( { 'return_code': 'Error! Must supply a temperature.' } )
    return jsonify( { 'return_code': 'Success!' } )

if __name__ == '__main__':
    app.run(debug = True)

