from .. import Module
import drake

class GLFW(Module):

  EXPECTED = {
    "3.2.1": {
      "headers": ["GLFW/glfw3.h"],
      "libraries": {
        "linux": ["libglfw3.a"]
      },
      "others": []
    }
  }

  def __init__(self,
               version,
               base_url = None,
               platform = "linux",
               dest = drake.Path("GLFW"),
               expected_headers = None):
    super().__init__("GLFW")
    self.__base_url = base_url or "https://github.com/glfw/glfw/releases/download"
    self.__version = version
    self.__platform = "linux"
    self.__zip = drake.node(dest  / "{version}.zip".format(version = self.__version))
    self.__path = dest / "glfw-{version}".format(version = self.__version)
    self.__include_path = self.__path / "include"
    self.__library_path = self.__path / "src"
    self.__cmake_lists = drake.Node(self.__path / "CMakeLists.txt")
    self.__makefile = drake.Node(self.__path / "Makefile")
    drake.HTTPDownload(url = self.url, dest = self.__zip)
    drake.Extractor(tarball = self.__zip,
                    targets = [
                      str(self.__cmake_lists.name_absolute())[5:]
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
      command = ['make', 'glfw'],
      cwd = self.__path)

  @property
  def headers(self):
    return drake.nodes(*[self.__include_path / f for f in GLFW.EXPECTED[self.__version]["headers"]])

  @property
  def libraries(self):
    return drake.nodes(*[self.__library_path / f for f in GLFW.EXPECTED[self.__version]["libraries"][self.__platform]])

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
    return "{base_url}/{version}/glfw-{version}.zip".format(
      base_url = self.__base_url,
      version = self.__version,
    )
