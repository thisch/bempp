// Copyright (C) 2011-2012 by the BEM++ Authors
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
// THE SOFTWARE.

#include "modified_helmholtz_3d_single_layer_boundary_operator.hpp"

#include "general_elementary_singular_integral_operator_imp.hpp"
#include "synthetic_scalar_integral_operator_builder.hpp"

#include "../common/boost_make_shared_fwd.hpp"

#include "../fiber/explicit_instantiation.hpp"

#include "../fiber/modified_helmholtz_3d_single_layer_potential_kernel_functor.hpp"
#include "../fiber/modified_helmholtz_3d_single_layer_potential_kernel_interpolated_functor.hpp"
#include "../fiber/scalar_function_value_functor.hpp"
#include "../fiber/simple_test_scalar_kernel_trial_integrand_functor.hpp"

#include "../grid/max_distance.hpp"

namespace Bempp
{

template <typename BasisFunctionType, typename KernelType, typename ResultType>
BoundaryOperator<BasisFunctionType, ResultType>
modifiedHelmholtz3dSingleLayerBoundaryOperator(
        const shared_ptr<const Context<BasisFunctionType, ResultType> >& context,
        const shared_ptr<const Space<BasisFunctionType> >& domain,
        const shared_ptr<const Space<BasisFunctionType> >& range,
        const shared_ptr<const Space<BasisFunctionType> >& dualToRange,
        KernelType waveNumber,
        const std::string& label,
        int symmetry,
        bool useInterpolation,
        int interpPtsPerWavelength)
{
    typedef typename ScalarTraits<BasisFunctionType>::RealType CoordinateType;

    typedef Fiber::ModifiedHelmholtz3dSingleLayerPotentialKernelFunctor<KernelType>
            NoninterpolatedKernelFunctor;
    typedef Fiber::ModifiedHelmholtz3dSingleLayerPotentialKernelInterpolatedFunctor<KernelType>
            InterpolatedKernelFunctor;
    typedef Fiber::ScalarFunctionValueFunctor<CoordinateType>
            TransformationFunctor;
    typedef Fiber::SimpleTestScalarKernelTrialIntegrandFunctor<
            BasisFunctionType, KernelType, ResultType> IntegrandFunctor;

    if (!domain || !range || !dualToRange)
        throw std::invalid_argument(
                "modifiedHelmholtz3dSingleLayerBoundaryOperator(): "
                "domain, range and dualToRange must not be null");

    typedef GeneralElementarySingularIntegralOperator<
            BasisFunctionType, KernelType, ResultType> Op;
    shared_ptr<Op> newOp;
    if (useInterpolation)
        newOp.reset(new Op(
                        domain, range, dualToRange, label, symmetry,
                        InterpolatedKernelFunctor(
                            waveNumber,
                            1.1 * maxDistance(*domain->grid(), *dualToRange->grid()),
                            interpPtsPerWavelength),
                        TransformationFunctor(),
                        TransformationFunctor(),
                        IntegrandFunctor()));
    else
        newOp.reset(new Op(
                        domain, range, dualToRange, label, symmetry,
                        NoninterpolatedKernelFunctor(
                            waveNumber),
                        TransformationFunctor(),
                        TransformationFunctor(),
                        IntegrandFunctor()));
    return BoundaryOperator<BasisFunctionType, ResultType>(context, newOp);
}

template <typename BasisFunctionType, typename KernelType, typename ResultType>
BoundaryOperator<BasisFunctionType, ResultType>
modifiedHelmholtz3dSyntheticSingleLayerBoundaryOperator(
        const shared_ptr<const Context<BasisFunctionType, ResultType> >& context,
        const shared_ptr<const Space<BasisFunctionType> >& domain,
        const shared_ptr<const Space<BasisFunctionType> >& range,
        const shared_ptr<const Space<BasisFunctionType> >& dualToRange,
        const shared_ptr<const Space<BasisFunctionType> >& internalTrialSpace,
        const shared_ptr<const Space<BasisFunctionType> >& internalTestSpace,
        KernelType waveNumber,
        const std::string& label,
        int symmetry,
        bool useInterpolation,
        int interpPtsPerWavelength)
{
    BoundaryOperator<BasisFunctionType, ResultType> internalOp =
            modifiedHelmholtz3dSingleLayerBoundaryOperator(
                context, internalTrialSpace, range /* or whatever */,
                internalTestSpace, waveNumber,
                "(" + label + ")_internal", symmetry,
                useInterpolation, interpPtsPerWavelength);
    return makeSyntheticScalarIntegralOperator(
                internalOp, domain, range, dualToRange,
                internalTrialSpace, internalTestSpace,
                label, NO_SYMMETRY);
}

#define INSTANTIATE_NONMEMBER_CONSTRUCTOR(BASIS, KERNEL, RESULT) \
    template BoundaryOperator<BASIS, RESULT> \
    modifiedHelmholtz3dSingleLayerBoundaryOperator( \
        const shared_ptr<const Context<BASIS, RESULT> >&, \
        const shared_ptr<const Space<BASIS> >&, \
        const shared_ptr<const Space<BASIS> >&, \
        const shared_ptr<const Space<BASIS> >&, \
        KERNEL, \
        const std::string&, int, bool, int); \
    template BoundaryOperator<BASIS, RESULT> \
    modifiedHelmholtz3dSyntheticSingleLayerBoundaryOperator( \
        const shared_ptr<const Context<BASIS, RESULT> >&, \
        const shared_ptr<const Space<BASIS> >&, \
        const shared_ptr<const Space<BASIS> >&, \
        const shared_ptr<const Space<BASIS> >&, \
        const shared_ptr<const Space<BASIS> >&, \
        const shared_ptr<const Space<BASIS> >&, \
        KERNEL, \
        const std::string&, int, bool, int)
FIBER_ITERATE_OVER_BASIS_KERNEL_AND_RESULT_TYPES(INSTANTIATE_NONMEMBER_CONSTRUCTOR);

} // namespace Bempp
