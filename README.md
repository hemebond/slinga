# slinga

*Note:* Development on this application has only just begun so functionality is limited.

Control [Icinga2](https://www.icinga.com/) via interactive [Slack](https://slack.com/) messages using this Flask app.

Slinga is a Flask application that parses the response from Slack when a user clicks the Acklnowledge button in a message. Slinga will then send an `acknowledge-problem` request to the Icingaweb2 server.

## Configuration
The configuration file should be updated with the Icingaweb2 API credentials and, optionally, the Slack verification token.

URL
:   Icinga2 API host (default: https://localhost:5665)

USERNAME
:   Icinga2 API username (default: root)

PASSWORD
:   Icinga2 API password (default: icinga)

TOKEN
:   Slack verification token. Any messages that don't contain this token will be rejected. (optional)
