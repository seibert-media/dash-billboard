
import time
import json

import Log
import Device
import Config
import ShootTrigger
import HTTPHelper
import CommandSet

class Stalk:
  def __init__(self, device):
    self.device = device
    self.shoot_trigger = ShootTrigger.ShootTrigger(self.shoot_user)

  def poll_sleep(self):
    time.sleep(Config.POLL_SLEEP_SECONDS)

  def poll_commit_status(self):
    while True:
      try:
        self.poll_commit_status_iteration()
        self.poll_sleep()
      except Exception as inst:
        Log.log("got exception while fetching dashboard data, ignoring")
        Log.log(inst)
        self.poll_sleep()
        continue

  def poll_commit_status_iteration(self):
    response_string = HTTPHelper.read_url(Config.DASHBOARD_URL)
    # Uncomment for high debug output of the original input data
    # Log.log("got response: "+ response_string);
    response = json.loads(response_string)
    if not "success" in response:
      Log.log("got an error from the dashboard server, ignoring")
      return
    commits = response["results"]
    self.shoot_trigger.update(commits)
  
  def shoot_user(self, user):
    Log.log("targeting: "+ user)
    user_found = CommandSet.run_command_set(self.device, user)
    if not user_found:
      Log.log("WARNING: No target command set defined for user %s" % user)
      return
              
