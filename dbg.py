from flask import Flask, render_template
from flask_socketio import SocketIO
import tensorflow
from Talk import ask

print ("This is socket file")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

@app.route('/')
def sessions():
	return render_template('session.html')

def messageReceived(methods=['GET', 'POST']):
	print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['POST']):
	socketio.emit('my response', json, callback=messageReceived)
	print('received my event: ' + str(json))
	txt_body = json['message']
	json['user_name'] = "Bot"
	json['message'] = ask(str(txt_body))
	# json['message'] = txt_body
	socketio.emit('my response', json, callback=messageReceived)




if __name__ == '__main__':
	socketio.run(app, debug=True)