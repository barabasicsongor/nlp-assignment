from cleaner import delete_tags

class Email(object):

  def __init__(self, header, body, fileid):
    self.header = header
    self.body = body
    self.fileid = fileid

  def del_tags(self):
    self.header = delete_tags(self.header)
    self.body = delete_tags(self.body)