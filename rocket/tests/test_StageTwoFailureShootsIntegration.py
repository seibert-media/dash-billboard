import unittest

import Commit
import ShootTrigger
import HTTPHelper
import Stalk
import Device
import Config

read_url_answers = [
    """{"success" : "true",
    "results" : [{
  "branch": "trunk",
  "committer": "charly",
  "id": "1.1.1",
  "revision": "1",
  "stage1": 3,
  "stage2": 3,
  "stage3": 0,
  "timestamp": "2013-09-06_14:02:33"
  },
  {
  "branch": "trunk",
  "committer": "ben",
  "id": "1.2.2",
  "revision": "2",
  "stage1": 3,
  "stage2": 3,
  "stage3": 0,
  "timestamp": "2013-09-06_14:22:09"
  },
  {
  "branch": "trunk",
  "committer": "john",
  "id": "1.3.3",
  "revision": "3",
  "stage1": 3,
  "stage2": 0,
  "stage3": 0,
  "timestamp": "2013-09-06_14:23:17"
  }
  ]}
  """,
  """ { "success" : "true",
  "results" : [{ "branch": "trunk",
  "committer": "charly",
  "id": "1.1.1",
  "revision": "1",
  "stage1": 3,
  "stage2": 3,
  "stage3": 0,
  "timestamp": "2013-09-06_14:02:33"
  },
  {
  "branch": "trunk",
  "committer": "ben",
  "id": "1.2.2",
  "revision": "2",
  "stage1": 3,
  "stage2": 3,
  "stage3": 0,
  "timestamp": "2013-09-06_14:22:09"
  },
  {
  "branch": "trunk",
  "committer": "john",
  "id": "1.3.3",
  "revision": "3",
  "stage1": 3,
  "stage2": 2,
  "stage3": 0,
  "timestamp": "2013-09-06_14:33:17"
  }
  ]}
  """
]
read_url_answers.reverse()

def do_nothing():
  pass

class StageTwoFailureShootsIntegration(unittest.TestCase):
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
      ),
      "ben" : (
        ("fire", 1),
      ),
      "john" : (
        ("fire", 1),
      ),
    }

  def mock_read_url(self):
    HTTPHelper.read_url = self.read_url_mock
  
  def setUp(self):
    self.times_shot = 0
    self.reset_called = 0
    self.mock_configuration()
    self.mock_read_url()
    self.device = self.mocked_device()
    self.stalk = Stalk.Stalk(self.device)

  def test_update_from_success_to_failure(self):
    self.stalk.poll_commit_status_iteration()
    self.stalk.poll_commit_status_iteration()
    self.assertEqual(self.times_shot, 1)

