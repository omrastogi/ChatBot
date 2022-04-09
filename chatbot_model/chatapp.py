from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import os

from wtforms.fields.html5 import EmailField

import tensorflow
from Talk import ask


app = Flask(__name__)
app.secret_key = os.urandom(24)

# Config MySQL
mysql = MySQL()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sslchat'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Initialize the app for use with this MySQL class
mysql.init_app(app)

@app.route('/')
def index():
	cur = mysql.connection.cursor()
	result = cur.execute("SELECT * FROM users WHERE username=%s", ["Om"])
		
	data = cur.fetchone()
	session['logged_in'] = True
	session['uid'] = 0
	session['s_name'] = 'User'
	uid = session['uid']
	session['name'] = 'Bot'
	session['lid'] = 1

	x = '1'
	cur.execute("UPDATE users SET online=%s WHERE id=%s", (x, uid))
	flash('You are now logged in', 'success')
	mysql.connection.commit()

		# Close Connection
	cur.close()
	# return redirect(url_for('index'))

	
	print ('Index')
	return render_template('newhome.html')




class MessageForm(Form):    # Create Message Form
	body = StringField('', [validators.length(min=1)], render_kw={'autofocus': True})


@app.route('/chatting/', methods=['GET', 'POST'])
def chatting():
	# print (session)
	
	if 'uid' in session:
		print('inside chatting')
		id = session['uid']

		form = MessageForm(request.form)
		# Create cursor
		cur = mysql.connection.cursor()

		# lid name
		get_result = cur.execute("SELECT * FROM users WHERE id=%s", [id])
		# print ('result',get_result)

		l_data = cur.fetchone()
		if get_result > 0:
			# session['name'] = l_data['name']
			uid = session['uid']
			# session['lid'] = id

			if request.method == 'POST' and form.validate():
				txt_body = form.body.data
				# Create cursor
				cur = mysql.connection.cursor()
				# print ('text',txt_body)
				cur.execute("INSERT INTO messages(body, msg_by, msg_to) VALUES(%s, %s, %s)",
							(txt_body, 0, 1))
				

				# if txt_body == 'hi':
				# 	txt_body = 'Hello'
				# else:
				# 	txt_body = 'I am good'
				# print (txt_body)
				txt_body = ask(str(txt_body))
				cur.execute("INSERT INTO messages(body, msg_by, msg_to) VALUES(%s, %s, %s)",
							(txt_body, 1, 0))
				# Commit cursor
				mysql.connection.commit()

			# Get users
			cur.execute("SELECT * FROM users")
			users = cur.fetchall()

			# Close Connection
			cur.close()
			return render_template('newchat_room.html', users=users, form=form)
			# return redirect(url_for('login'))
		else:
			flash('No permission!', 'danger')
			return redirect(url_for('index'))
	else:
		print ('NOT FOUND UID')
		return redirect(url_for('index'))


@app.route('/chats', methods=['GET', 'POST'])
def chats():
	print ('chat',session)
	if 'lid' in session:
		id = session['lid']
		uid = session['uid']
		print (id)
		# Create cursor
		cur = mysql.connection.cursor()
		# Get message
		cur.execute("SELECT * FROM messages WHERE (msg_by=%s AND msg_to=%s) OR (msg_by=%s AND msg_to=%s) "
					"ORDER BY id ASC", (0, 1, 1, 0))
		chats = cur.fetchall()
		# Close Connection
		cur.close()
		return render_template('newchats.html', chats=chats,)
	return redirect(url_for('index'))


if __name__ == '__main__':
	app.run(debug=True)