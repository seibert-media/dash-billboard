import unittest

import Commit
import ShootTrigger
import HTTPHelper
import Stalk
import Device
import Config

read_url_answers = [
    '{\
    "success" : "true",\
    "results" : [\
    {"branch": "trunk",\
    "committer": "andy",\
    "id": "15.12345.1775",\
    "revision": "12345",\
    "stage1": 3,\
    "stage2": 3,\
    "stage3": 0,\
    "timestamp": "2013-07-05_12:33:43"},\
    {"branch": "trunk",\
    "committer": "charly",\
    "id": "15.12346.1775",\
    "revision": "12346",\
    "stage1": 2,\
    "stage2": 2,\
    "stage3": 0,\
    "timestamp": "2013-07-05_12:34:43"}\
    ]}',
    '{\
    "success" : "true",\
    "results" : [\
    {"branch": "trunk",\
    "committer": "andy",\
    "id": "15.12347.1775",\
    "revision": "12347",\
    "stage1": 3,\
    "stage2": 3,\
    "stage3": 0,\
    "timestamp": "2013-07-05_12:33:43"},\
    {"branch": "trunk",\
    "committer": "charly",\
    "id": "15.12348.1775",\
    "revision": "12348",\
    "stage1": 2,\
    "stage2": 2,\
    "stage3": 0,\
    "timestamp": "2013-07-05_12:34:43"}\
    ]}',
]

def do_nothing():
  pass

class StalkIntegrationTest(unittest.TestCase):
  times_shot = 0
  reset_called = 0

  def on_shoot(self, value):
    self.times_shot += 1

  def on_reset_position(self):
    self.reset_called += 1

  def mocked_device(self):
    device = Device.Device()
    device.shoot = self.on_shoot
    device.reset_position = self.on_reset_position
    device.setup = do_nothing
    device.reset = do_nothing
    return device

  def read_url_mock(self, url):
    return read_url_answers.pop()
  
  def mock_configuration(self):
    Config.POLL_SLEEP_SECONDS = 1
    Config.COMMAND_SETS = {
      "charly" : (
        ("fire", 1),
        ("zero", 0)
      ),
    }

  def mock_read_url(self):
    HTTPHelper.read_url = self.read_url_mock
  
  def setUp(self):
    self.mock_configuration()
    self.mock_read_url()
    self.device = self.mocked_device()
    self.stalk = Stalk.Stalk(self.device)

  def test_update_from_success_to_failure(self):
    self.stalk.poll_commit_status_iteration()
    self.stalk.poll_commit_status_iteration()
    self.assertEqual(self.times_shot, 1)
    self.assertEqual(self.reset_called, 1)

