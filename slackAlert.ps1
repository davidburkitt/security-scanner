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
}
"@)
#$payload.Append("]}")

Send-SlackMessage -Message $payload.ToString()
