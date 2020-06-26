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
                "text": "Security Scanning Alert"
            }
        },
        {
            "type": "divider"
        }
    ],
    "attachments": [
        {
            "color": "#FF0000",
            "title": "Vulnerabiltiies detected",
            "text": "$($SlackNotification)"
        }
    ]
}
"@)
#$payload.Append("]}")

Send-SlackMessage -Message $payload.ToString()
