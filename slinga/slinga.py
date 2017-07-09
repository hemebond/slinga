from flask import Flask
from flask import request
from flask import make_response
from flask import abort
from flask import jsonify
from urllib.parse import parse_qs
import json
import requests


app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
	URL = 'https://localhost:5665',
	USERNAME = 'root',
	PASSWORD = 'icinga',
))
app.config.from_envvar('SLINGA_SETTINGS', silent=True)


@app.route("/", methods=['POST'])
def index():
	post_body = request.get_data().decode('utf-8')
	try:
		parsed_body = parse_qs(post_body)
		payload = json.loads(parsed_body['payload'][0])
	except:
		abort(400)

	# Make sure we're getting a payload from our application
	if not 'token' in payload:
		abort(400)

	if 'TOKEN' in app.config and app.config['TOKEN'] != payload['token']:
			abort(403)

	if not 'callback_id' in payload:
		abort(400)

	# the callback_id should be "host" or "host!service"
	if '!' in payload['callback_id']:
		host, service = payload['callback_id'].split('!')
	else:
		host = payload['callback_id']
		service = None

	action = payload['actions'][0]['value']
	author_id = payload['user']['id']
	author_name = payload['user']['name']

	if action == 'acknowledge':
		if service is None:
			url = '{}/v1/actions/acknowledge-problem?type=Host&host={}'.format(app.config['URL'], host)
		else:
			url = '{}/v1/actions/acknowledge-problem?type=Service&service={}!{}'.format(app.config['URL'], host, service)

		ackdata = json.dumps({'author': author_name, 'comment': 'Acknowledged via Slack'}).encode('utf-8')
		headers = {'Accept': 'application/json'}

		try:
			r = requests.post(url, data=ackdata, headers=headers, auth=(app.config['USERNAME'], app.config['PASSWORD']), verify=False)
		except:
			e = sys.exc_info()[0]
			abort(make_response(jsonify(message['attachments'].append({'text': e, 'color': '#FF3333'})), 500))

		# Return a message to Slack to replace the button
		message = payload['original_message']
		if r.status_code == 200:
			message['attachments'].append(
				{
					'text': 'Acknowledged by <@{}|{}>'.format(author_id, author_name),
					'color': '#36A64F',
				}
			)
		else:
			abort(make_response(jsonify(message['attachments'].append({'text': 'Could not acknowledge problem.', 'color': '#FF3333'})), 500))

	return jsonify(message)
