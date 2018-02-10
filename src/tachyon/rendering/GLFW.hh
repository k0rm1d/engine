#pragma once

#include <vector>
#include <memory>
#include <experimental/propagate_const>

namespace tachyon::rendering
{
  class GLFW;

  auto
  glfw() -> GLFW const&;

  class GLFW
  {
  public:
    using Extensions = std::vector<char const*>;

  private:
    GLFW();
    ~GLFW();

  public:
    auto
    extensions() const -> Extensions const&;

  private:
    struct Impl;
    std::experimental::propagate_const<std::unique_ptr<Impl>> _impl;

  public:
    friend
    auto
    glfw() -> GLFW const&;
  };
};
