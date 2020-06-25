param (
   [String] $SlackNotificationUrl,
   [String] $SlackNotification
)

function Send-SlackMessage([string]$Message) {
    Invoke-WebRequest -Uri $SlackNotificationUrl -Method Post -Headers @{"content-type"="application/json"} -Body $Message
}

$payload = [System.Text.StringBuilder]::new(@"
{
    "attachments": [
        {
            "color": "#2eb886",
            "title": "Security Scanning Alert",
            "text": "$($SlackNotification)",
        }
    ]
}
"@)
#$payload.Append("]}")

Send-SlackMessage -Message $payload.ToString()
