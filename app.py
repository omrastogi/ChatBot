from flask import Flask, request
from cbot import Pattern_Search

model = Pattern_Search()
model.load_representations()
app = Flask(__name__)


@app.route('/state')
def index():
	return 'Server Works!'


@app.route('/', methods=['POST'])
def reply_message():
	print(request.headers)
	msg = request.form['body']
	scr, reply = model.infer(msg)
	return reply


if __name__ == "__main__":
	# model = QAModel()
	app.run()