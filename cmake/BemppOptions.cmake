# Options (can be modified by user)
option(WITH_TESTS "Compile unit tests (can be run with 'make test')" ON)
option(WITH_INTEGRATION_TESTS "Compile integration tests" OFF)
option(WITH_OPENCL "Add OpenCL support for Fiber module" OFF)
option(WITH_CUDA "Add CUDA support for Fiber module" OFF)
option(WITH_ALUGRID "Have or install Alugrid" OFF)
option(WITH_MPI "Whether to compile with MPI" OFF)

option(ENABLE_SINGLE_PRECISION "Enable support for single-precision calculations" ON)
option(ENABLE_DOUBLE_PRECISION "Enable support for double-precision calculations" ON)
option(ENABLE_COMPLEX_KERNELS  "Enable support for complex-valued kernel functions" ON)
option(ENABLE_COMPLEX_BASIS_FUNCTIONS  "Enable support for complex-valued basis functions" ON)
