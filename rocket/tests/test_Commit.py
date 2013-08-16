import unittest

import Commit

class CommitTest(unittest.TestCase):

  def test_create_by_json(self):
    commit_json = {
     u'branch'    : u'trunk',
     u'committer' : u'john',
     u'id'        : u'15.12345.1775',
     u'revision'  : u'12348',
     u'stage1'    : 2,
     u'stage2'    : 0,
     u'stage3'    : 0,
     u'timestamp' : u'2013-07-05_12:36:43'}
    commit = Commit.from_json(commit_json)
    self.assertEqual(commit.branch,     'trunk')
    self.assertEqual(commit.bundle,     '15.12345.1775')
    self.assertEqual(commit.revision,   '12348')
    self.assertEqual(commit.committer,  'john')
    self.assertEqual(commit.stage1,     2)
    self.assertEqual(commit.stage2,     0)
    self.assertEqual(commit.stage3,     0)
    self.assertEqual(commit.timestamp,  '2013-07-05_12:36:43')

