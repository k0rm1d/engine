from .. import Module
import drake

from .. import Module
import drake

class Assimp(Module):

  EXPECTED = {
    "4.1.0": {
      "headers": ["assimp/config.h"],
      "libraries": {
        "linux": ["libassimp.so"]
      },
      "others": []
    }
  }

  def __init__(self,
               version,
               base_url = None,
               platform = "linux",
               dest = drake.Path("Assimp"),
               expected_headers = None):
    super().__init__("Assimp")
    self.__base_url = base_url or "https://github.com/assimp/assimp/archive"
    self.__version = version
    self.__platform = "linux"
    self.__tar = drake.Node(dest  / "v{version}.tar.gz".format(version = self.__version))
    self.__path = dest / "assimp-{version}".format(version = self.__version)
    self.__include_path = self.__path / "include"
    self.__library_path = self.__path / "lib"
    self.__cmake_lists = drake.Node(self.__path / "CMakeLists.txt")
    self.__makefile = drake.Node(self.__path / "Makefile")
    drake.HTTPDownload(url = self.url, dest = self.__tar)
    drake.Extractor(tarball = self.__tar,
                    targets = [
                      str(self.__cmake_lists.name_absolute())[len(str(dest)) + 1:]
                    ]).targets()
    drake.ShellCommand(
      sources = [self.__cmake_lists],
      targets = self.headers + [self.__makefile],
      command = [
        'cmake', '.'
      ],
      cwd = self.__path)
    drake.ShellCommand(
      sources = [self.__makefile],
      targets = self.libraries,
      command = ['make', 'assimp'],
      cwd = self.__path)

  @property
  def headers(self):
    return drake.nodes(*[self.__include_path / f for f in Assimp.EXPECTED[self.__version]["headers"]])

  @property
  def libraries(self):
    return drake.nodes(*[self.__library_path / f for f in Assimp.EXPECTED[self.__version]["libraries"][self.__platform]])

  @property
  def libs(self):
    def clean(library):
      return str(library.path().basename().without_last_extension())[3:]
    return list(map(clean, self.libraries))

  @property
  def base_path(self):
    return self.__base_path

  @property
  def include_path(self):
    return self.__include_path

  @property
  def library_path(self):
    return self.__library_path

  @property
  def url(self):
    return "{base_url}/v{version}.tar.gz".format(
      base_url = self.__base_url,
      version = self.__version,
    )
