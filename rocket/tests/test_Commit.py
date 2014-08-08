import unittest

import Commit

class CommitTest(unittest.TestCase):

  def test_create_by_json(self):
    commit_json = {
     'branch'    : 'trunk',
     'committer' : 'john',
     'id'        : '15.12345.1775',
     'revision'  : '12348',
     'stage1'    : 2,
     'stage2'    : 0,
     'stage3'    : 0,
     'timestamp' : '2013-07-05_12:36:43'}
    commit = Commit.from_json(commit_json)
    self.assertEqual(commit.branch,     'trunk')
    self.assertEqual(commit.bundle,     '15.12345.1775')
    self.assertEqual(commit.revision,   '12348')
    self.assertEqual(commit.committer,  'john')
    self.assertEqual(commit.stage1,     2)
    self.assertEqual(commit.stage2,     0)
    self.assertEqual(commit.stage3,     0)
    self.assertEqual(commit.timestamp,  '2013-07-05_12:36:43')

  def test_parse_datetime(self):
    commit = Commit.Commit('trunk', '15.12345.1775', '12345', 'john', 2, 0, 0, '2013-07-05_12:03:01')
    self.assertEqual(commit.datetime.year, 2013);
    self.assertEqual(commit.datetime.month, 7);
    self.assertEqual(commit.datetime.day, 5);
    self.assertEqual(commit.datetime.hour, 12);
    self.assertEqual(commit.datetime.minute, 3);
    self.assertEqual(commit.datetime.second, 1);

  def test_is_complete(self):
    commit = Commit.Commit('trunk', '15.12345.1775', '12345', 'john', Commit.STATUS_UNKOWN, Commit.STATUS_UNKOWN, Commit.STATUS_UNKOWN, '2013-07-05_12:03:01')
    self.assertFalse(commit.is_complete());

    commit = Commit.Commit('trunk', '15.12345.1775', '12345', 'john', Commit.STATUS_BUILDING, Commit.STATUS_UNKOWN, Commit.STATUS_UNKOWN, '2013-07-05_12:03:01')
    self.assertFalse(commit.is_complete());

    commit = Commit.Commit('trunk', '15.12345.1775', '12345', 'john', Commit.STATUS_BUILDING, Commit.STATUS_BUILDING, Commit.STATUS_UNKOWN, '2013-07-05_12:03:01')
    self.assertFalse(commit.is_complete());

    commit = Commit.Commit('trunk', '15.12345.1775', '12345', 'john', Commit.STATUS_SUCCESS, Commit.STATUS_UNKOWN, Commit.STATUS_UNKOWN, '2013-07-05_12:03:01')
    self.assertFalse(commit.is_complete());

    commit = Commit.Commit('trunk', '15.12345.1775', '12345', 'john', Commit.STATUS_FAIL, Commit.STATUS_UNKOWN, Commit.STATUS_UNKOWN, '2013-07-05_12:03:01')
    self.assertTrue(commit.is_complete());

    commit = Commit.Commit('trunk', '15.12345.1775', '12345', 'john', Commit.STATUS_FAIL, Commit.STATUS_BUILDING, Commit.STATUS_UNKOWN, '2013-07-05_12:03:01')
    self.assertTrue(commit.is_complete());

    commit = Commit.Commit('trunk', '15.12345.1775', '12345', 'john', Commit.STATUS_SUCCESS, Commit.STATUS_SUCCESS, Commit.STATUS_UNKOWN, '2013-07-05_12:03:01')
    self.assertTrue(commit.is_complete());

  def test_empty(self):
    commit = Commit.Commit()
    self.assertEqual(commit.stage1, Commit.STATUS_UNKOWN);
    self.assertEqual(commit.stage2, Commit.STATUS_UNKOWN);
    self.assertEqual(commit.stage3, Commit.STATUS_UNKOWN);
    self.assertFalse(commit.is_complete());

