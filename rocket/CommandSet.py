
import Config
import Log

def has_command_set(user):
  return CommandSet.find_user_command_set(user) != None

def find_command_set(user):
  if user.lower() in Config.REMOTE:
    user = "remote"

  # Not efficient but our user list is probably less than 1k.
  # Do a case insenstive search for convenience.
  for key in Config.COMMAND_SETS:
    if key.lower() == user.lower():
      # We have a command set that targets our user so got for it!
      return Config.COMMAND_SETS[key]
      match = True
      break
  return None

def run(device, command, value):
  command_set = find_command_set(command)
  if command_set != None:
    __run_command_set(device, command_set)
  else:
    __run_command(device, command, value)

def run_command_set(device, user):
  command_set = find_command_set(user)
  if command_set != None:
    __run_command_set(device, command_set)
    return True
  else:
    return False

def __run_command_set(device, commands):
  device.setup()
  for cmd, value in commands:
    __run_command(device, cmd, value)
  device.reset()

def __run_command(device, command, value):
  command = command.lower()
  if command == "right":
    device.move_right(value)
  elif command == "left":
    device.move_left(value)
  elif command == "up":
    device.move_up(value)
  elif command == "down":
    device.move_down(value)
  elif command == "zero" or command == "park" or command == "reset":
    device.reset_position()
  elif command == "pause" or command == "sleep":
    time.sleep(value / 1000.0)
  elif command == "led":
    if value == 0:
      device.turn_led_off()
    else:
      device.turn_led_on()
  elif command == "fire" or command == "shoot":
    device.shoot(value)
  else:
    Log.log("error: Unknown command: '%s'" % command)

