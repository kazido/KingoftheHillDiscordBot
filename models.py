from tortoise import fields
from tortoise.models import Model
from tortoise.manager import Manager as _Manager
from tortoise.queryset import QuerySet as _QuerySet
from base64 import b64decode as _decode, b64encode as _encode


cns = [
  "abcdefghi",
  "jklmnopqr",
  "stuvwxyzA",
  "BCDEFGHIJ",
  "KLMNOPQRS",
  "TUVWXYZ01",
  "23456789=",
  "+/",
]

class InvQuerySet(_QuerySet):
  def filter(self, uid, item, **kwargs):
    return super().filter(item_uid=Inventory.encode(uid, item), **kwargs)

class InvManager(_Manager):
  def get_queryset(self):
    return InvQuerySet(self._model)

class Users(Model):
  class Meta:
    table = "users"

  uid         = fields.BigIntField(unique=True)
  pid         = fields.BigIntField(null=True)
  coins       = fields.BigIntField(default=0)
  in_party    = fields.BooleanField(default=bool)
  party_owner = fields.BooleanField(default=bool)
  experience  = fields.BigIntField(default=0)

class Inventory(Model):
  class Meta:
    manager = InvManager()
    table = "inventory"

  item_uid = fields.CharField(120, unique=True)
  count = fields.BigIntField()

  def decode(self, seperator: str = "."):
    c,_="",0
    item_uid=str(self.item_uid)[1:]
    for i in item_uid:
      if _==0:
        fmt=cns[int(i)]
        _=1
      else:
        c+=fmt[int(i)]
        _=0
    cnt=_decode(bytes(c, encoding="utf-8")).decode("utf-8")
    assert seperator in cnt
    uid, item = cnt.split(seperator)
    return [int(uid), int(item)]

  @classmethod
  def encode(cls, uid: int, item: int, seperator: str = "."):
    resp = "1"
    enc = _encode(bytes(str(uid)+"."+str(item), encoding="utf-8")).decode("utf-8")
    for c in enc:
      for n, cn in enumerate(cns):
        if c in cn:
          resp += str(n)+str(cn.index(c))

    return resp


  @classmethod
  async def create(cls, uid: int, item: int, count: int):
    instance = cls(item_uid=cls.encode(uid, item), count=count)
    instance._saved_in_db = False
    db = cls._choose_db(True)
    await instance.save(using_db=db, force_create=True)
    return instance

class Parties(Model):
  pid = fields.BigIntField(unique=True)
  owner = fields.BigIntField(unique=True)
  member = fields.BigIntField(unique=True)
