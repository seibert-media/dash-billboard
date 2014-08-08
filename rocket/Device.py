
import Log
import platform
import time
import usb
#import usb.core
#import usb.util

# Protocol command bytes
DOWN    = 0x01
UP      = 0x02
LEFT    = 0x04
RIGHT   = 0x08
FIRE    = 0x10
STOP    = 0x20

class Device:
  def __init__(self):
    self.device = None
    self.device_type = None

  def setup(self):
    self.device = usb.core.find(idVendor=0x2123, idProduct=0x1010)
    if self.device is None:
      self.device = usb.core.find(idVendor=0x0a81, idProduct=0x0701)
      if self.device is None:
        raise ValueError('Missile device not found')
      else:
        self.device_type = "Original"
    else:
      self.device_type = "Thunder"
    
    # On Linux we need to detach usb HID first
    if "Linux" == platform.system():
      try:
        self.device.detach_kernel_driver(0)
      except Exception, e:
        pass # already unregistered    
    
    self.device.set_configuration()
  
  def reset(self):
    self.device.reset()

  def move_right(self, value):
    self.send_move(RIGHT, value)

  def move_left(self, value):
    self.send_move(LEFT, value)

  def move_up(self, value):
    self.send_move(UP, value)

  def move_down(self, value):
    self.send_move(DOWN, value)

  def reset_position(self):
    # Move to bottom-left
    self.send_move(DOWN, 1000)
    self.send_move(LEFT, 6000)

  def shoot(self, value):
    if value < 1 or value > 4:
      value = 1
    # Stabilize prior to the shot, then allow for reload time after.
    time.sleep(0.5)
    for i in range(value):
      self.send_cmd(FIRE)
      time.sleep(4.5)
    # stop the shooting
    self.send_move(DOWN, 1)

  def send_move(self, cmd, duration_ms):
    self.send_cmd(cmd)
    time.sleep(duration_ms / 1000.0)
    self.send_cmd(STOP)
  
  def send_cmd(self, cmd):
    if "Thunder" == self.device_type:
      self.device.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, cmd, 0x00,0x00,0x00,0x00,0x00,0x00])
    elif "Original" == self.device_type:
      self.device.ctrl_transfer(0x21, 0x09, 0x0200, 0, [cmd])

  def turn_led_on(self):
    self.send_led(0x01)

  def turn_led_off(self):
    self.send_led(0x00)
  
  def send_led(self, cmd):
    if "Thunder" == self.device_type:
      self.device.ctrl_transfer(0x21, 0x09, 0, 0, [0x03, cmd, 0x00,0x00,0x00,0x00,0x00,0x00])
    elif "Original" == self.device_type:
      Log.log("there is no LED on this device")
  
