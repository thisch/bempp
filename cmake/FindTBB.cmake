# Finds the thread building block library
# Sets the following variables
# - TBB_LIBRARY
# - TBB_LIBRARY_DEBUG
# - TBB_MALLOC_LIBRARY
# - TBB_MALLOC_LIBRARY_DEBUG
# - TBB_INCLUDE_DIR

find_library(TBB_LIBRARY NAMES tbb)
find_library(TBB_LIBRARY_DEBUG NAMES tbb_debug)
find_library(TBB_MALLOC_LIBRARY NAMES tbbmalloc)
find_library(TBB_MALLOC_LIBRARY_DEBUG NAMES tbbmalloc_debug)
find_path(TBB_INCLUDE_DIR tbb.h PATH_SUFFIXES tbb)

include(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(
  TBB
  DEFAULT_MSG
  TBB_LIBRARY TBB_LIBRARY_DEBUG TBB_MALLOC_LIBRARY TBB_MALLOC_LIBRARY_DEBUG
  TBB_INCLUDE_DIR
)

# Unsets values if not found, so we don't end up with mixes of library from one place and another.
if(NOT TBB_FOUND)
  unset(TBB_LIBRARY CACHE)
  unset(TBB_LIBRARY_DEBUG CACHE)
  unset(TBB_MALLOC_LIBRARY CACHE)
  unset(TBB_MALLOC_LIBRARY_DEBUG CACHE)
  unset(TBB_INCLUDE_DIR CACHE)
endif()
