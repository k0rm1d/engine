#include "GLFW.hh"

#include <GLFW/glfw3.h>

namespace tachyon::rendering
{
  auto
  glfw() -> GLFW const&
  {
    static GLFW glfw;
    return glfw;
  }

  struct GLFW::Impl
  {
    Impl()
    {
      glfwInit();
    }

    ~Impl()
    {
      glfwTerminate();
    }

    auto
    extensions() const -> Extensions const&
    {
      if (!this->_extensions.empty())
        return this->_extensions;

      uint32_t count = 0;
      const char** exts = glfwGetRequiredInstanceExtensions(&count);
      if (exts == nullptr || count == 0)
        throw std::runtime_error("Couldn't get any extension");

      this->_extensions = Extensions(exts, exts + count);
      return this->_extensions;
    }

  private:
    mutable GLFW::Extensions _extensions;
  };

  GLFW::GLFW()
    : _impl(new Impl)
  {
  }

  GLFW::~GLFW()
  {
  }

  auto
  GLFW::extensions() const -> Extensions const&
  {
    return this->_impl->extensions();
  }
}
