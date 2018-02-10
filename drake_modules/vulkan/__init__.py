from .. import Module
import drake

class Vulkan(Module):

  EXPECTED = {
    "1.0.65.0": {
      "headers": ["vulkan/vulkan.h", "vulkan/vulkan.hpp"],
      "libraries": {
        "linux": ["libvulkan.so"]
      },
      "others": [
        ("binary_path", "glslangValidator"),
      ]
    }
  }

  def __init__(self,
               version,
               base_url = None,
               platform = "linux",
               dest = drake.Path("vulkan"),
               expected_headers = None):
    super().__init__("Vulkan")
    self.__base_url = base_url or "https://sdk.lunarg.com/sdk/download"
    self.__version = version
    self.__platform = "linux"
    self.__run = drake.Node(dest / "install.run")
    self.__base_path = dest / "VulkanSDK"
    self.__path = self.__base_path / "{version}/x86_64".format(version = self.__version)
    self.__include_path = self.__path / "include"
    self.__library_path = self.__path / "lib"
    self.__binary_path = self.__path / "bin"

    drake.HTTPDownload(url = self.url, dest = self.__run)
    drake.ShellCommand(sources = [self.__run],
                       targets = self.headers + self.libraries + self.others,
                       command = ['bash', str(self.__run), '--target', str(self.base_path)])

  @property
  def headers(self):
    return drake.nodes(*[self.__include_path / f for f in Vulkan.EXPECTED[self.__version]["headers"]])

  @property
  def libraries(self):
    return drake.nodes(*[self.__library_path / f for f in Vulkan.EXPECTED[self.__version]["libraries"][self.__platform]])

  @property
  def libs(self):
    def clean(library):
      return str(library.path().basename().without_last_extension())[3:]
    return list(map(clean, self.libraries))

  @property
  def base_path(self):
    return self.__base_path

  @property
  def binary_path(self):
    return self.__binary_path

  @property
  def others(self):
    return drake.nodes(*[
      getattr(self, path) / f for path, f in Vulkan.EXPECTED[self.__version]["others"]
    ])

  @property
  def include_path(self):
    return self.__include_path

  @property
  def library_path(self):
    return self.__library_path

  @property
  def glslangValidator(self):
    return drake.Node(self.__binary_path / "glslangValidator")

  @property
  def url(self):
    return "{base_url}/{version}/{platform}/vulkansdk-{platform}-x86_64-{version}.run".format(
      base_url = self.__base_url,
      version = self.__version,
      platform = self.__platform)

  def __str__(self):
    return "Vulkan(include_path = {}, library_path = {}, libraries = {}, libs = {})".format(
      self.include_path, self.library_path, self.libraries, self.libs)
