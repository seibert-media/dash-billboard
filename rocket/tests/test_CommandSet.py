
import unittest
import Config
import CommandSet

class CommandSetTest(unittest.TestCase):

  def test_find_command_set(self):
    Config.COMMAND_SETS = {
        "charly" : (1),
        "BETH"   : (2),
        "john"   : (3),
    }
    self.assertEqual(CommandSet.find_command_set("charly"), (1))
    self.assertEqual(CommandSet.find_command_set("beth"),   (2))
    self.assertEqual(CommandSet.find_command_set("joHN"),   (3))

  def test_find_remote_command_set(self):
    Config.REMOTE = {
      "smith"  : True,
      "miller" : True,
    }
    Config.COMMAND_SETS = {
      "charly" : (1),
      "remote" : (2),
    }
    self.assertEqual(CommandSet.find_command_set("smith"),  (2))
    self.assertEqual(CommandSet.find_command_set("miller"), (2))

  def test_set_not_found(self):
    Config.REMOTE = { }
    Config.COMMAND_SETS = {
        "charly" : (1),
    }
    self.assertEqual(CommandSet.find_command_set("waldo"), None)

