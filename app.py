from flask import Flask
from flask import request
from flask import make_response
from flask import abort
from flask import jsonify
from urllib.parse import parse_qs
import json
from icinga2api.client import Client
import config


app = Flask(__name__)


@app.route("/", methods=['POST'])
def index():
	try:
		post_body = request.get_data().decode('UTF-8')
		parsed_body = parse_qs(post_body)
		payload = json.loads(parsed_body['payload'][0])
	except:
		abort(400)

	# Make sure we're getting a payload from our application
	if not 'token' in payload:
		abort(400)
	if payload['token'] != config.validation_token:
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

	if action == 'acknowledge':
		client = Client('https://{}:{}'.format(config.host, config.port), config.username, config.password)

		if service is None:
			r = client.actions.acknowledge_problem('Host',
			                                       'host.name=="{}"'.format(host),
			                                       payload['user']['name'],
			                                       'Acknowledged via Slack')
		else:
			r = client.actions.acknowledge_problem('Service',
			                                       'host.name=="{}" && service.name=="{}"'.format(host, service),
			                                       payload['user']['name'],
			                                       'Acknowledged via Slack')

	message = payload['original_message']
	message['attachments'].append(
		{
			'text': 'Acknowledged by <@{}|{}>'.format(payload['user']['id'], payload['user']['name']),
			'color': '#36A64F',
		}
	)

	return jsonify(message)


# Run with
# python3 ./app.py
# or
# FLASK_DEBUG=1 FLASK_APP=app.py python -m flask run --host 0.0.0.0 --port 8000
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)
