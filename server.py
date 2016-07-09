from flask import Flask, session, render_template, request, redirect
import random
import datetime

app = Flask(__name__)
app.secret_key = "YoYoYoCoolioDood"

@app.route('/')
def index():
	# session.clear()
	if 'activities' not in session:
		session['activities'] = []
	if 'times' not in session:
		session['times'] = []
	if 'buildings' not in session:
		session['buildings'] = []
	if 'gold' not in session:
		session['gold'] = 0
	if 'isgain' not in session:
		session['isgain'] = []
	if 'length' not in session:
		session['length'] = 0
	return render_template('index.html')

@app.route('/process_money', methods = ['POST'])
def process_money():
	gold = 0
	building = request.form['building']
	time = datetime.datetime.now()
	hour = time.hour
	if hour > 12:
		hour -= 12
		morning = "pm"
	else:
		morning = "am"
	timestring = "({}/{}/{} {}:{} {})".format(time.year, time.month, time.day, hour, time.minute, morning)

	if building == 'farm':
		gold = random.randint(10, 20)
	elif building == 'cave':
		gold = random.randint(5, 10)
	elif building == 'house':
		gold = random.randint(2, 5)
	elif building == 'casino':
		gold = random.randint(-50, 50)

	session['gold'] += gold
	session['isgain'].append(gold >= 0)
	session['buildings'].append(building)
	session['times'].append(timestring)

	if gold >= 0:
		phrase = "Earned {} golds from the {}! {}".format(gold, building, timestring)
	else:
		phrase = "Entered a {} and lost {} golds... Ouch... {}".format(building, abs(gold), timestring)
	session['activities'].append(phrase)
	session['length'] += 1
	return redirect('/')

app.run(debug = True)