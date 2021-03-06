"""
bempp.assembly. \
        helmholtz
        laplace
        modified_helmholtz
        maxwell

These are subdivided into
  * boundary_operator
  * potential_operator

The first contains single_layer, double_layer, conj_double_layer, hypersingular
The second contains single_layer, double_layer

There should be a bempp.assembly.local_operators
  with identity, maxwell_identity, laplace_something

Finally, bempp.assembly.maxwell:
     electric_field (aka single_layer), magnetic_field (double_layer)

"""
from bempp.assembly import Context


def test_scalar_space_creation():
    from bempp.grid import sample as sample_grid
    grid = sample_grid()

    context = Context()
    for dtype in ['float32', 'complex128']:
        context.basis_type = dtype
        constant = context.scalar_space(grid, order=0)
        assert constant.dtype == dtype


def test_dirichlet_tut_operators():
    from bempp.grid import sample as sample_grid
    grid = sample_grid()

    context = Context(basis_type='float32')
    constant = context.scalar_space(grid, order=0)
    linear = context.scalar_space(grid, order=1)

    double_layer = context.operators.laplace.boundary.double_layer(
        constant, linear, constant)
    single_layer = context.operators.laplace.boundary.single_layer(
        constant, linear, constant)
    identity = context.operators.local.identity(constant, linear, constant)

    assert double_layer.basis_type == context.basis_type
    assert single_layer.basis_type == context.basis_type
    assert identity.basis_type == context.basis_type

    assert single_layer.domain.is_compatible(constant)
    assert single_layer.range.is_compatible(linear)
    assert single_layer.dual_to_range.is_compatible(constant)


def test_boundary_op_operations():
    from py.test import raises
    from bempp.grid import sample as sample_grid
    grid = sample_grid()

    context = Context(basis_type='float32')
    constant = context.scalar_space(grid, order=0)
    linear = context.scalar_space(grid, order=1)

    double_layer = context.operators.laplace.boundary.double_layer(
        constant, linear, constant)
    single_layer = context.operators.laplace.boundary.single_layer(
        constant, linear, constant)

    sumop = double_layer + single_layer
    assert sumop != double_layer
    assert sumop != single_layer

    # Something about incompatible domains.
    # But that still checks that the operation is passed on to C++
    with raises(ValueError):
        double_layer * single_layer

    scalop = 3.0 * double_layer
    assert scalop != double_layer
    scalop = double_layer * 3.0
    assert scalop != double_layer

    divop = double_layer / 3.0
    assert divop != double_layer

    # Raised inside C++. Means we went though correct branch.
    with raises(RuntimeError):
        scalop = 1.0j * double_layer
