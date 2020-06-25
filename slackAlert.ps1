param (
   [String] $SlackNotificationUrl,
   [String] $SlackNotification
)

function Send-SlackMessage([string]$Message) {
    Invoke-WebRequest -Uri $SlackNotificationUrl -Method Post -Headers @{"content-type"="application/json"} -Body $Message
}

$payload = [System.Text.StringBuilder]::new(@"
{
	"blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "$($SlackNotification)"
            }
        },
        {
            "type": "divider"
        }
    ]
    "attachments": [
        {
            "color": "#2eb886",
            "title": "Security Scanning Alert",
            "text": "$($SlackNotification)",
            "fields": [
                {
                    "title": "Priority",
                    "value": "High",
                    "short": false
                }
            ],
        }
  ]
}
"@)
#$payload.Append("]}")

Send-SlackMessage -Message $payload.ToString()
