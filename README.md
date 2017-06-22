slinga
======

*Note:* Development on this application has only just begun so functionality is limited.

Control [Icinga2](https://www.icinga.com/) via interactive [Slack](https://slack.com/) messages using this Flask app and notification script.

Slinga App
==========
Slinga is a Flask application that parses the response from Slack when a user clicks the Acklnowledge button in a message sent from the `slack-notification.py` script. Slinga will then send an `acknowledge-problem` request to the Icingaweb2 server.

The `config.py` file should be updated with the Icingaweb2 API credentials and, optionally, the Slack verification token.

Icinga2 NotificationCommand Objects
===================================
    object NotificationCommand "slack-host-notification"  {
            import "plugin-notification-command"
            command = [ SysconfDir + "/icinga2/scripts/slack-notification.py", ]

            arguments = {
                    "-u" = "$notification.vars.webhook_url$"
                    "-t" = "$notification.type$"
                    "-w" = "http://icingaweb2.company.com"
                    "-a" = "$notification.author$"
                    "-c" = "$notification.comment$"
                    "-m" = "$host.output$"
                    "-H" = "$host.name$"
                    "-s" = "$host.state$"
            }
    }
    object NotificationCommand "slack-service-notification"  {
            import "plugin-notification-command"

            command = [ SysconfDir + "/icinga2/scripts/slack-notification.py", ]
            arguments = {
                    "-u" = "$notification.vars.webhook_url$"
                    "-t" = "$notification.type$"
                    "-w" = "http://icingaweb2.company.com"
                    "-a" = "$notification.author$"
                    "-c" = "$notification.comment$"
                    "-m" = "$service.output$"
                    "-s" = "$service.state$"
                    "-H" = "$host.display_name$"
                    "-S" = "$service.name$"
            }
    }
