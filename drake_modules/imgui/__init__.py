from .. import Module
import drake

class imgui(Module):

  EXPECTED = {
    "1.53": {
      "headers": ["imgui.h"],
      "sources": ["imgui.cpp", "imgui_draw.cpp"],
      "libraries": {
        "linux": ["libimgui.so", "libingui_draw.so"]
      },
      "others": []
    }
  }

  def __init__(self,
               version,
               base_url = None,
               platform = "linux",
               dest = drake.Path("imgui"),
               expected_headers = None):
    super().__init__("imgui")
    self.__base_url = base_url or "https://github.com/ocornut/imgui/archive"
    self.__version = version
    self.__platform = "linux"
    self.__tar = drake.Node(dest  / "v{version}.tar.gz".format(version = self.__version))
    self.__path = dest / "imgui-{version}".format(version = self.__version)
    self.__include_path = self.__path
    self.__source_path = self.__path
    self.__library_path = self.__path
    self.__cmake_lists = drake.Node(self.__path / "CMakeLists.txt")
    self.__makefile = drake.Node(self.__path / "Makefile")
    drake.HTTPDownload(url = self.url, dest = self.__tar)
    drake.Extractor(tarball = self.__tar,
                    targets = map(lambda f: str(f.name_absolute())[len(str(dest)) + 1:],
                                  self.headers + self.sources))
    for index, cpp in enumerate(self.sources):
      drake.ShellCommand(
        sources = [cpp],
        targets = [self.libraries[index]],
        command = [
          'g++', '-shared', '-fPIC', str(cpp.path().basename()), '-o',
          str(self.libraries[index].path().basename())
        ],
        cwd = self.__path)

  @property
  def headers(self):
    return drake.nodes(*[self.__include_path / f for f in imgui.EXPECTED[self.__version]["headers"]])

  @property
  def sources(self):
    return drake.nodes(*[self.__source_path / f for f in imgui.EXPECTED[self.__version]["sources"]])

  @property
  def libraries(self):
    return drake.nodes(*[self.__library_path / f for f in imgui.EXPECTED[self.__version]["libraries"][self.__platform]])

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
