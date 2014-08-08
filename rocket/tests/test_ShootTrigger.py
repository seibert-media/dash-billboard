import unittest

import Commit
import ShootTrigger

class ShootTriggerTest(unittest.TestCase):
  shot_users = []

  def reset_seen_commits(self):
    self.shootTrigger.seen_commits = {}

  def reset_shoot_counter(self):
    self.shot_users = []

  def on_shoot(self, name):
    self.shot_users.append(name)
  
  def setUp(self):
    self.shootTrigger = ShootTrigger.ShootTrigger(self.on_shoot)
    self.reset_seen_commits()
    self.reset_shoot_counter()

  def test_update_from_success_to_failure(self):
    self.shootTrigger.update([])
    self.shootTrigger.update([
    # tests okay
    {u'branch': u'trunk',
     u'committer': u'andy',
     u'id': u'15.12345.1775',
     u'revision': u'12345',
     u'stage1': 3,
     u'stage2': 3,
     u'stage3': 0,
     u'timestamp': u'2013-07-05_12:33:43'},
    # tests fail
    {u'branch': u'trunk',
     u'committer': u'charly',
     u'id': u'15.12346.1775',
     u'revision': u'12346',
     u'stage1': 2,
     u'stage2': 0,
     u'stage3': 0,
     u'timestamp': u'2013-07-05_12:34:43'},
    ])
    self.assertEqual(len(self.shot_users), 1)
    self.assertEqual(self.shot_users[0], 'charly')

  def test_simple_case_from_success_to_failure(self):
    self.shootTrigger.handle_commits([
      Commit.Commit('trunk', '15.12345.1775', '12345', 'andy',   Commit.STATUS_SUCCESS, Commit.STATUS_SUCCESS, Commit.STATUS_UNKOWN, '2013-07-05_12:33:43'),
      Commit.Commit('trunk', '15.12346.1775', '12346', 'charly', Commit.STATUS_FAIL,    Commit.STATUS_UNKOWN,  Commit.STATUS_UNKOWN, '2013-07-05_12:34:43'),
    ])
    self.assertEqual(len(self.shot_users), 1)
    self.assertEqual(self.shot_users[0], 'charly')
    
  def test_status_already_failing_then_ignore_it(self):
    self.shootTrigger.handle_commits([
      Commit.Commit('trunk', '15.12345.1775', '12345', 'charly',   Commit.STATUS_FAIL, Commit.STATUS_UNKOWN, Commit.STATUS_UNKOWN, '2013-07-05_12:33:43'),
      Commit.Commit('trunk', '15.12346.1775', '12346', 'beth',     Commit.STATUS_FAIL, Commit.STATUS_UNKOWN, Commit.STATUS_UNKOWN, '2013-07-05_12:34:43'),
    ])
    self.assertEqual(len(self.shot_users), 0)

  def test_ignore_already_known_commits(self):
    self.shootTrigger.handle_commits([
      Commit.Commit('trunk', '15.12345.1775', '12345', 'beth',   Commit.STATUS_SUCCESS, Commit.STATUS_SUCCESS, Commit.STATUS_UNKOWN, '2013-07-05_12:33:43'),
      Commit.Commit('trunk', '15.12346.1775', '12346', 'charly', Commit.STATUS_FAIL,    Commit.STATUS_UNKOWN,  Commit.STATUS_UNKOWN, '2013-07-05_12:34:43'),
    ])

    # new data delivery
    self.shootTrigger.handle_commits([
      Commit.Commit('trunk', '15.12345.1775', '12345', 'beth',   Commit.STATUS_SUCCESS, Commit.STATUS_SUCCESS, Commit.STATUS_UNKOWN, '2013-07-05_12:33:43'),
      Commit.Commit('trunk', '15.12346.1775', '12346', 'charly', Commit.STATUS_FAIL,    Commit.STATUS_UNKOWN,  Commit.STATUS_UNKOWN, '2013-07-05_12:34:43'),
    ])
    self.assertEqual(len(self.shot_users), 1)
    self.assertEqual(self.shot_users[0], 'charly')
  
  def test_do_not_shoot_twice_even_if_failure_reported_in_different_poll_cycles(self):
    self.shootTrigger.handle_commits([
      Commit.Commit('trunk', '15.12345.1775', '12345', 'beth',   Commit.STATUS_SUCCESS, Commit.STATUS_SUCCESS, Commit.STATUS_UNKOWN, '2013-07-05_12:33:43'),
      Commit.Commit('trunk', '15.12346.1775', '12346', 'charly', Commit.STATUS_FAIL,    Commit.STATUS_UNKOWN,  Commit.STATUS_UNKOWN, '2013-07-05_12:34:43'),
    ])
    self.shootTrigger.handle_commits([
      Commit.Commit('trunk', '15.12347.1775', '12347', 'john',   Commit.STATUS_FAIL,    Commit.STATUS_UNKOWN, Commit.STATUS_UNKOWN, '2013-07-05_12:35:43'),
    ])
    self.assertEqual(len(self.shot_users), 1)
    self.assertEqual(self.shot_users[0], 'charly')

  def test_ignore_first_status_update(self):
    self.shootTrigger.handle_commits([
      Commit.Commit('trunk', '15.12345.1775', '12345', 'beth',   Commit.STATUS_SUCCESS, Commit.STATUS_SUCCESS, Commit.STATUS_UNKOWN, '2013-07-05_12:33:43'),
      Commit.Commit('trunk', '15.12346.1775', '12346', 'john',   Commit.STATUS_FAIL,    Commit.STATUS_UNKOWN,  Commit.STATUS_UNKOWN, '2013-07-05_12:34:43'),
    ], True);
    self.assertEqual(len(self.shot_users), 0)

  def test_ignore_first_but_not_second_status_update(self):
    self.shootTrigger.handle_commits([
      Commit.Commit('trunk', '15.12345.1775', '12345', 'john',   Commit.STATUS_FAIL,     Commit.STATUS_UNKOWN, Commit.STATUS_UNKOWN, '2013-07-05_12:33:43'),
    ], True);
    self.shootTrigger.handle_commits([
      Commit.Commit('trunk', '15.12346.1775', '12346', 'beth',   Commit.STATUS_SUCCESS,  Commit.STATUS_SUCCESS, Commit.STATUS_UNKOWN, '2013-07-05_12:34:43'),
    ]);
    self.shootTrigger.handle_commits([
      Commit.Commit('trunk', '15.12347.1775', '12347', 'john',   Commit.STATUS_FAIL,     Commit.STATUS_UNKOWN, Commit.STATUS_UNKOWN, '2013-07-05_12:35:43'),
    ]);
    self.assertEqual(len(self.shot_users), 1)
    self.assertEqual(self.shot_users[0], 'john')

  def test_only_complete_commits_keep_single_complete_commit(self):
    filtered = self.shootTrigger.only_complete_commits([
      Commit.Commit('trunk', '1.1.1', '1', 'john1', Commit.STATUS_FAIL,     Commit.STATUS_FAIL,     Commit.STATUS_FAIL,   '2013-01-01_00:00:00'),
    ]);
    self.assertEqual(len(filtered), 1);

  def test_only_complete_commits_remove_single_incomplete_commit(self):
    filtered = self.shootTrigger.only_complete_commits([
      Commit.Commit('trunk', '1.1.1', '1', 'john1', Commit.STATUS_UNKOWN,     Commit.STATUS_UNKOWN,     Commit.STATUS_UNKOWN,   '2013-01-01_00:00:00'),
    ]);
    self.assertEqual(len(filtered), 0);

  def test_only_complete_commits_if_one_incomplete_commit_found(self):
    filtered = self.shootTrigger.only_complete_commits([
      Commit.Commit('trunk', '1.1.1', '1', 'john1', Commit.STATUS_FAIL,     Commit.STATUS_FAIL,     Commit.STATUS_FAIL,   '2013-01-01_00:00:00'),
      Commit.Commit('trunk', '1.2.2', '2', 'john2', Commit.STATUS_UNKOWN,   Commit.STATUS_UNKOWN,   Commit.STATUS_UNKOWN, '2013-01-02_00:00:00'),
      Commit.Commit('trunk', '1.3.3', '3', 'john3', Commit.STATUS_FAIL,     Commit.STATUS_UNKOWN,   Commit.STATUS_UNKOWN, '2013-01-03_00:00:00'),
    ]);
    self.assertEqual(filtered[0].bundle, "1.1.1");
    self.assertEqual(len(filtered), 1);
  
  def test_stage2_failure_followed_by_stage1_failure_shoots(self):
    self.shootTrigger.handle_commits([
      Commit.Commit('trunk', '15.12345.1775', '12345', 'john',   Commit.STATUS_SUCCESS,  Commit.STATUS_FAIL, Commit.STATUS_UNKOWN, '2013-07-05_12:33:43'),
    ], True);
    self.shootTrigger.handle_commits([
      Commit.Commit('trunk', '15.12346.1775', '12346', 'beth',   Commit.STATUS_FAIL,  Commit.STATUS_UNKOWN, Commit.STATUS_UNKOWN, '2013-07-05_12:34:43'),
    ]);
    self.assertEqual(len(self.shot_users), 1)
    self.assertEqual(self.shot_users[0], 'beth')


