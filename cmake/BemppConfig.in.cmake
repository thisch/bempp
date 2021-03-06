# - Config file for the BEM++ package
set(Bempp_CMAKE_DIR "${CMAKE_CURRENT_LIST_DIR}")
if(NOT Bempp_BINARY_DIR)
    message(STATUS "Linking to BEM++ package in ${Bempp_CMAKE_DIR}")
endif()
if(NOT TARGET libbempp AND NOT Bempp_BINARY_DIR)
    include("${Bempp_CMAKE_DIR}/BemppTargets.cmake")
endif()

set(BEMPP_LIBRARY libbempp)
set(BEMPP_INCLUDE_DIRS @ALL_INCLUDE_DIRS@)
set(BEMPP_DIRICHLET_TUTOTIAL tutorial_dirichlet)
set(BEMPP_PYTHON_INCLUDE_DIRS @PYTHON_INCLUDE_DIRS@ @NUMPY_INCLUDE_DIRS@)
set(BEMPP_CXX_FLAGS "@CXX11_FLAGS@ @BLAS_CMAKE_C_FLAGS@ @ARMADILLO_CXX_FLAGS@")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${BEMPP_CXX_FLAGS}")
if(NOT "@BEMPP_PREFIX_PATH@" STREQUAL "" AND EXISTS "@BEMPP_PREFIX_PATH@")
    # Adds other libraries, say Trilinos
    list(APPEND CMAKE_PREFIX_PATH @BEMPP_PREFIX_PATH@)
    if(EXISTS "@BEMPP_PREFIX_PATH@/lib")
        link_directories("@BEMPP_PREFIX_PATH@/lib")
    endif()
    if(EXISTS "@BEMPP_PREFIX_PATH@/lib64")
        link_directories("@BEMPP_PREFIX_PATH@/lib64")
    endif()
endif()
