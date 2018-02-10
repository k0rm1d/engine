
class Module:

  def __init__(self, name):
    self.__name = name

  @property
  def libraries(self):
    raise NotImplementedError("libraries not implemented")

  @property
  def library_path(self):
    raise NotImplementedError("library_path not implemented")

  @property
  def include_path(self):
    raise NotImplementedError("includes not implemented")

  @property
  def libs(self):
    return NotImplementedError("libs not implemented")

  def __str__(self):
    return "{}(include_path = {}, library_path = {}, libraries = {}, libs = {})".format(
      self.__name, self.include_path, self.library_path, self.libraries, self.libs)
