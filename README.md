# site-monitor-python
A web service/site monitor in Python that sends notifications to a webhook (e.g., Slack WebHook)

## How to use:
1. Specify the site names, Url's and a notification WebHook using the config file name site-monitor.config
   You can monitor multiple sites, whose values are separated by commas (','). For example:
   ```
   SiteFoo, SiteBar
   https://foo.example.com, https://bar.example.com
   https://hooks.slack.com/services/blah/blah/blah
   ```
2. Run the python program with the config file in the same folder:

   `python site-monitor.py`
   
