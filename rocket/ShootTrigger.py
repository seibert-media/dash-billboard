# -*- coding: utf8 -*-

import Log
import Commit 

class ShootTrigger:

  def __init__(self, callback):
    self.first_update = True
    self.previous_commit = Commit.Commit()
    self.seen_completed_commits = {}
    self.callback = callback

  def shoot_user(self, user):
    self.callback(user)

  def only_complete_commits(self, commits):
    complete_commits = []
    for commit in commits:
      if commit.is_complete():
        complete_commits.append(commit)
      else:
        break
    return complete_commits
  
  def handle_commits(self, commits, just_initialize_dont_shooting = False):
    # We remove commits that are still building, but only the most recent ones
    # older ones should fall into the list of known commits and never be recognized
    # again
    commits = self.only_complete_commits(commits)
  
    if len(commits) == 0:
      return
  
    for commit in commits[:-1]:
      self.handle_commit(commit)
    # Handle the last commit we receive special - it's the most recent one
    self.handle_commit(commits[-1], not just_initialize_dont_shooting)
  
  
  def handle_commit(self, commit, last = False): 
    # Uncomment for debugging
    # print "commit: "
    # pprint.pprint(commit)
  
    # Skip already known commits
    if commit.key() in self.seen_completed_commits:
      #Log.log("Skipping commit: " + commit.key())
      return
  
    self.seen_completed_commits[commit.key()] = True
  
    if last:
        Log.log("Status: "+ self.previous_commit.to_str() +" ➔ "+ commit.to_str())
  
    # If there is a failure detected after a success, shoot
    if commit.is_worse_than(self.previous_commit) and last:
      self.shoot_user(commit.committer)

    self.previous_commit = commit
 
  def update(self, commits):
    # Uncomment for more debug information
    # Log.log("got a response with "+ str(len(commits)) + " commits.")

    # Sort commits, recent items to the end
    commits = sorted(commits, cmp=Commit.cmp_map_by_timestamp)

    # Only look at latest 10 commits
    del commits[:-10]

    commit_objects = []
    for commit in commits:
      commit_objects.append(Commit.from_json(commit))

    self.handle_commits(commit_objects, self.first_update)
    self.first_update = False

  
