from flask import Flask, request
from model import QAModel

model = QAModel()
app = Flask(__name__)


@app.route('/state')
def index():
	return 'Server Works!'


@app.route('/', methods=['POST'])
def reply_message():
	print(request.headers)
	msg = request.form['body']
	scr, reply = model.inference(msg)
	return reply


if __name__ == "__main__":
	# model = QAModel()
	app.run()