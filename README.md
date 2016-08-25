# Pivotal Tracker Integration Service for Mattermost

This integration service posts comments, new story and story status changes to to [Mattermost's incoming webhooks](http://docs.mattermost.com/developer/webhooks-incoming.html).

## Project Goal

This middle-man project should help you integrate your changes from Pivotal Tracker into your Mattermost instance.

## Requirements

To run this integration you need:

1. A **web server** running **Ubuntu 14.04/16.04** and **Python 2.7+**.
2. A **[Pivotal Tracker account](https://www.pivotaltracker.com/)** with a project to which you have administrator access
3. A **[Mattermost account](http://www.mattermost.org/)** where [incoming webhooks are enabled](https://github.com/mattermost/platform/blob/master/doc/integrations/webhooks/Incoming-Webhooks.md#enabling-incoming-webhooks)

Many web server options will work, below we provide instructions for [**Heroku**](README.md#heroku-based-install) and a general [**Linux/Ubuntu**](README.md#linuxubuntu-1404-web-server-install) server.
### Heroku-based Install

**:heavy_exclamation_mark: This was not adapted to the new python package.**

To install this project using Heroku, you will need:

1. A **Heroku account**, available for free at [Heroku.com](https://signup.heroku.com/)
2. A **GitHub account**, available for free at [GitHub.com](https://github.com/join)

Here's how to start:

1. **Create a copy of this project to manipulate**
  1. Log in to your GitHub account. Go to the [Github repository of this project](https://git.studioqi.ca/lefebvre/mattermost-integration-pivotal) and click **Fork** in the top-right corner to create a copy of this project that you control and manipulate.
2. **Deploy your project copy to Heroku**
  1. Go to your [**Heroku Dashboard**](https://dashboard.heroku.com/apps) and click **+** in the top-right corner then **Create New App**. Give your app a unqiue name (like `mattermost-pivotaltracker-[YOUR_GITHUB_USERNAME]`), select your region and click **Create App**.
  2. Heroku directs you to the **Deploy** tab of the dashboard for your new app, select **GitHub** as your connection option, then click **Connect to GitHub** at the bottom of the screen to authorize Herkou to access your GitHub account.
  3. In the pop up window, click **Authorize Application** to allow Heroku to access your accounts repositories. On your Heroku dashboard, select your account in the first drop-down then search for the repo we created earlier by forking this project. Type `mattermost-integration-pivotaltracker` in the **repo-name** field, then click **Search** and then the **Connect** button once Heroku finds your repository.
  4. Scroll to the bottom of the new page. Under the **Manual Deploy** section, make sure the `master` branch is selected then click **Deploy Branch**. After a few seconds you'll see a confirmation that the app has been deployed.
  5. At the top of your app dashboard, go to the **Settings** tab and scroll down to the **Domains** section. Copy the URL below **Heroku Domain** (we'll refer to this as `http://<your-heroku-domain>/` and we'll need it in the next step)
  6. Leave your Heroku interface open as we'll come back to it to finish the setup.

3. **Connect your PivotalTracker project to your Heroku instance**
  1. On your Pivotal Tracker dashboard, listing all your projects. Next to your project name, click on the **gear**.
  2. On the left, click on **Integration**.
  3. At the bottom of the page, enter `http://<your-heroku-domain>/new_event` and select **v5**.
  4. Rinse and repeat for every project you want to track.

4. **Set up your Mattermost instance to receive incoming webhooks**
 1. Log in to your Mattermost account. Click the three dot menu at the top of the left-hand side and go to **Account Settings** > **Integrations** > **Incoming Webhooks**.
 2. Under **Add a new incoming webhook** select the channel in which you want your Pivotal Tracker notifications to appear, then click **Add** to create a new entry.
 3. Copy the contents next to **URL** of the new webhook you just created (we'll refer to this as `https://<your-mattermost-webhook-URL>` and add it to your Heroku server).
 4. Go back to your Heroku app dashboard under the **Settings** tab. Under the **Config Variables** section, click **Reveal Config Vars**
     1. Type `MATTERMOST_WEBHOOK_URL` in the **KEY** field and paste `https://<your-mattermost-webhook-URL>` into the **VALUE** field, then click **Add**.


### Linux/Ubuntu 14.04/16.04 Web Server Install

The following procedure shows how to install this project on a Linux web server running Ubuntu 14.04/16.04. Make sure the port is open on your firewall (`5000` by default).

To install this project using a Linux-based web server, you will need a Linux/Ubuntu 14.04/16.04 web server supporting Python 2.7+ or a compatible version. Other compatible operating systems and Python versions should also work.

Here's how to start:

1. **Set up your Mattermost instance to receive incoming webhooks**
 1. Log in to your Mattermost account. Click the three dot menu at the top of the left-hand side and go to **Account Settings** > **Integrations** > **Incoming Webhooks**.
 2. Under **Add a new incoming webhook** select the channel in which you want your Pivotal Tracker notifications to appear, then click **Add** to create a new entry.
 3. Copy the contents next to **URL** of the new webhook you just created (we'll refer to this as `https://<your-mattermost-webhook-URL>`).

2. **Set up this project to run on your web server**
 1. Set up a **Linux Ubuntu 14.04** server either on your own machine or on a hosted service, like AWS.
 2. **SSH** into the machine, or just open your terminal if you're installing locally.
 3. Confirm **Python 2.7** or a compatible version is installed by running:
    - `python --version` If it's not installed you can find it [here](https://www.python.org/downloads/)
 4. Install **pip** and other essentials:
    - `sudo apt-get install python-pip python-dev build-essential`
 5. Create a virtualenv if you want to keep things separated:
    - `[sudo] pip install virtualenv`
    - to handle virtual envs even simpler consider the virtualenvwrapper:  `[sudo] pip install virtualenvwrapper`
 6. Install integration requirements:
    - `[sudo] pip install git+https://git.studioqi.ca/lefebvre/mattermost-integration-pivotaltracker.git`
 7. Run the server:
    - `mattermost_pivotaltracker --help`
    - `mattermost_pivotaltracker $MATTERMOST_WEBHOOK_URL`
    You will see the output similar to `Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)`. This is default IP:PORT pair
    the integration service will listen on. We will refer to this address as the `https://<your-mattermost-integration-URL>`). You may change the IP:PORT with the adequate command-line options (see --help)
 8. You may want to add an upstart script to auto-start mattermost_pivotaltracker at boot:
 
```
# /etc/init/mattermost-pivotaltracker.conf
start on runlevel [2345]
stop on runlevel [016]
respawn

# Change this to the relevant user
setuid mattermost

# Change the path if necessary, add options if need be
exec /home/mattermost/ve/bin/mattermost_pivotaltracker http://mattermost/hooks/hook-id
```

 Instead of `/etc/init/` script you may want to handle the mattermost_pivotaltracker with supervisor (http://supervisord.org/). The
    sample config file can be as simple as:
    
```
[program:mattermost-pivotaltracker]
user=mattermost
command=/home/mattermost/ve/mattermost/bin/mattermost_pivotaltracker http://mattermost/hooks/hook-id
autostart=true
autorestart=true
stdout_logfile=/home/mattermost/logs/mattermost_pivotaltracker.log
redirect_stderr=true
```

3. **Connect your PivotalTracker project to your Heroku instance**
  1. On your Pivotal Tracker dashboard, listing all your projects. Next to your project name, click on the **gear**.
  2. On the left, click on **Integration**.
  3. At the bottom of the page, enter `http://<your-heroku-domain>/new_event` and select **v5**.
