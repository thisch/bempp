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

#ifndef bempp_sparse_inverse_hpp
#define bempp_sparse_inverse_hpp

#include "../common/common.hpp"
#include "../common/shared_ptr.hpp"

class Epetra_CrsMatrix;

namespace Bempp {

/** \relates DiscreteSparseBoundaryOperator
 *  \brief Return the inverse of a *block-diagonal* sparse matrix \p mat.
 *
 *  In practice, \p mat might be the mass matrix of a space of discontinuous
 *  functions.
 *
 *  Be aware that explicit inversion of \f$A\f$ is usually not the most
 *  accurate way to solve the equation \f$A^{-1} X = B\f$.
 */
shared_ptr<Epetra_CrsMatrix> sparseInverse(const Epetra_CrsMatrix &mat);

} // namespace Bempp

#endif
