
# Define a dictionary of "command sets" that map usernames to a sequence 
# of commands to target the user (e.g their desk/workstation).  It's 
# suggested that each set start and end with a "zero" command so it's
# always parked in a known reference location. The timing on move commands
# is milli-seconds. The number after "fire" denotes the number of rockets
# to shoot.

COMMAND_SETS = {
  "john" : (
      ("zero", 0),
      ("right", 200),
      ("up", 200),
      ("fire", 1),
      ("zero", 0),
  ),
  "charly" : (
      ("zero", 0),
      ("led", 1),
      ("right", 1000),
      ("up", 1000),
      ("fire", 1),
      ("led", 0),
      ("zero", 0),
  ),
  "remote" : (
      ("zero", 0),
      ("up", 500),
      ("right", 500),
      ("fire", 1),
      ("zero", 0),
  ),
}

# You can specify all remote developers here, they will all
# be targeted by executing the "remote" command set.
REMOTE = {
  "supervillan" : True,
  "sirbreaksalot" : True,
}

# TODO Configure with an URL to the CI Dashboard that does not require any form
# of authorization or SSL problems.
DASHBOARD_BASE_URL = "https://example.com/dash"

POLL_SLEEP_SECONDS = 15

DASHBOARD_URL = DASHBOARD_BASE_URL + "/bundle?branch=trunk&limit=10&sort=%5B%7B%22property%22%3A%22revision%22%2C%22direction%22%3A%22DESC%22%7D%5D"

# If you're Jenkins server is secured by HTTP basic auth, sent the
# username and password here.  Else leave this blank.
HTTPAUTH_USER                   = ""
HTTPAUTH_PASS                   = ""

