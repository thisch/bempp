<%
codims = [('0','codim_zero'),('1','codim_one'),('2','codim_two')]
%>

from bempp.utils cimport unique_ptr
from bempp.grid.codim_template cimport codim_zero,codim_one,codim_two


from bempp.grid.entity_iterator cimport c_EntityIterator

% for (codim, codim_template) in codims:
from bempp.grid.entity_iterator cimport EntityIterator${codim}
% endfor

cdef extern from "bempp/grid/grid_view.hpp" namespace "Bempp":
    cdef cppclass c_GridView "Bempp::GridView":
        int dim() const
        int dimWorld() const
        size_t entityCount(int codim) const
        unique_ptr[c_EntityIterator[codim]] entityIterator[codim]() const 

cdef class GridView:
    cdef unique_ptr[c_GridView] impl_ 
    cpdef size_t entity_count(self,int codim)
% for (codim,codim_template) in codims:
    cpdef EntityIterator${codim} _entity_iterator${codim}(self)
% endfor
cdef GridView _grid_view_from_unique_ptr(unique_ptr[c_GridView]& c_view)
