
from datetime import datetime

# Commit format:
#
# {u'branch': u'trunk',
#  u'committer': u'beth',
#  u'id': u'15.12345.1772',
#  u'revision': u'12345',
#  u'stage1': 3,
#  u'stage2': 3,
#  u'stage3': 2,
#  u'timestamp': u'2013-07-05_11:11:58'}
def from_json(json_obj):
  return Commit(
    json_obj["branch"],
    json_obj["id"],
    json_obj["revision"],
    json_obj["committer"],
    json_obj["stage1"],
    json_obj["stage2"],
    json_obj["stage3"],
    json_obj["timestamp"]
  )

def cmp_map_by_revision(x, y):
  if int(x["revision"]) < int(y["revision"]):
      return -1
  elif int(y["revision"]) < int(x["revision"]):
      return 1
  else:
      return 0

def cmp_map_by_timestamp(x, y):
  if cmp(x["timestamp"], y["timestamp"]) < 0:
      return -1
  elif cmp(x["timestamp"], y["timestamp"]) > 0:
      return 1
  else:
      return 0

STATUS_FAIL     = 2
STATUS_SUCCESS  = 3
STATUS_BUILDING = 1
STATUS_UNKOWN   = 0

class Commit:
  def __init__(self, branch, bundle, revision, committer, stage1, stage2, stage3, timestamp):
    self.branch    = branch
    self.bundle    = bundle
    self.revision  = revision
    self.committer = committer
    self.stage1    = stage1
    self.stage2    = stage2
    self.stage3    = stage3
    self.timestamp = timestamp
    self.datetime  = datetime.strptime(timestamp, "%Y-%m-%d_%H:%M:%S")

  def key(self):
    # There may be multiple test runs for a revision
    return self.revision + self.timestamp

  def is_success(self):
    return self.stage1 == STATUS_SUCCESS and self.stage2 == STATUS_SUCCESS

  def is_building(self):
    return self.stage1 == STATUS_BUILDING or (self.stage1 != STATUS_FAIL and self.stage2 == STATUS_BUILDING)

  def is_failure(self):
    return self.stage1 == STATUS_FAIL or self.stage2 == STATUS_FAIL

  def is_unkown(self):
    return self.stage1 == STATUS_UNKOWN or self.stage2 == STATUS_UNKOWN

  def is_complete(self):
    return self.stage1 == STATUS_FAIL or (self.stage1 == STATUS_SUCCESS and (self.stage2 == STATUS_FAIL or self.stage2 == STATUS_SUCCESS))
  
