from array import array
from collections.abc import Iterator, Sequence, Generator, Sized, Iterable
from typing import Union, Self, Any
from reprlib import repr
from math import hypot
from operator import xor, index, floordiv, truediv, ge, gt, le, lt
from functools import reduce
from itertools import zip_longest
from fractions import Fraction 

class Vector(object):
    """
    An n-dimensional vector class.
    """
    # Default each element is an 8-byte double precision float 
    typecode = 'd'
    
    def __init__(self, components: Union[Sequence[Union[int, float]], Generator[Union[int, float], None, None]]):
        """
        Initialize an instance of the Vector class.

        Parameters
        ----------
        components : Union[Sequence[Union[int, float]], Generator[Union[int, float], None, None]]
            A collection of integers or floats, either as a sequence or a generator
        """
        self._components = array(self.typecode, components)
        
    @classmethod
    def frombytes(cls, octets: bytes) -> Self:
        """
        Create a new instance of the class from a sequence of bytes.

        1. Extract the first byte from the `octets` byte sequence, which represent the type code that specifies the data type of the vector elements
        2. Convert this byte to a character, which is expected to correspond to a valid type code understood by `array`, e.g., 'd' for double precision float
        3. Create a memory view from the rest of the bytes (`octets[1:]`), which are the actual data representing the vector components
        4. Create a new instance of the class with the memory view as the `components` argument in the constructor

        Parameters
        ----------
        octets : bytes
            A byte sequence where the first byte is the type code and the
            subsequent bytes are the data to be converted based on that type code
            
        Returns
        -------
        Self
            A new instance of the class
            
        Example
        -------
        >>> typecode = 'd'
        >>> numbers = array(typecode, [1.0, 2.0, 3.0])
        >>> bytes_data = bytes([ord(typecode)]) + numbers.tobytes()
        >>> vector = Vector.frombytes(bytes_data)
        >>> print(vector)
        Vector([1.0, 2.0, 3.0])
        """
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        # Passed to __init__ as components
        return cls(memv)
        
    def __iter__(self) -> Iterator:
        """
        Support for the iterator protocol.

        Returns
        -------
        Iterator
            An iterator over `self._components`
        """
        return iter(self._components)
    
    def __repr__(self) -> str:
        """
        Use `reprlib.repr()` to create a string representation of the instance. The `components`
        is a string, e.g. `array('d', [1.0, 2.0, 3.0, 4.0, ....])`. We use the `str.find` method
        to locate the start of the `[` and only keep the `[1.0, 2.0, 3.0, 4.0, ....]` part of the
        string.

        Returns
        -------
        str
            A limited-length representation of `self._components`
        """
        # By default, maxtuple = 6, maxlist = 6, maxset = 6, which means after 6 elements, the rest are replaced with '...'
        components = repr(self._components)
        components = components[components.find('['):-1]
        return f'Vector({components})'
    
    def __str__(self) -> str:
        """
        User-friendly string representation.

        Returns
        -------
        str
            String representation after converting the components to a tuple.
        """
        return str(tuple(self._components))
    
    def __bytes__(self) -> bytes:
        """
        Convert `self.typecode` to `bytes` and concatenate it with another `bytes` object converted from
        an `array`. A bytes object is an immutable sequence of single byte values. One byte can represent
        a decimal number between 0 and 255.

        Returns
        -------
        bytes
            A bytes object.
        """
        return (bytes([ord(self.typecode)]) + bytes(self._components))
    
    def __bool__(self) -> bool:
        """
        The truth value of the instance, which delegates to the `__abs__` dunder method.

        Returns
        -------
        bool
            _description_
        """
        return bool(abs(self))
    
    # ------------------------------ Unary operators ----------------------------- #
    
    def __abs__(self) -> float:
        """
        Compute the euclidean norm `sqrt(sum(x**2 for x in coordinates))`.

        Returns
        -------
        float
            The euclidean norm of the vector
        """
        return hypot(*self)
    
    def __neg__(self):
        """
        Implement the unary negation operator `-`.
        """
        return Vector(-vector_element for vector_element in self)
    
    def __pos__(self):
        """
        Implement the unary positive operator `+`.
        """
        return Vector(vector_element for vector_element in self)
    
    # ------------------------------ Infix operators ----------------------------- #
    
    def __add__(self, other: Any) -> 'Vector':
        """
        Add two vectors element-wise. If the two vectors have different lengths, the `zip_longest`
        function will fill the shorter vector with 0.0 values to match the length of the longer vector.

        Parameters
        ----------
        other : Any
            The other vector or sequence to add

        Returns
        -------
        Vector
            A new instance of the class
        """
        try:
            pairs = zip_longest(self, other, fillvalue=0.0)
            return Vector(vec_el_a + vec_el_b for vec_el_a, vec_el_b in pairs)
        except TypeError:
            return NotImplemented
        
    def __sub__(self, other: Any) -> 'Vector':
        """
        Subtract two vectors element-wise. If the two vectors have different lengths, the `zip_longest`
        function will fill the shorter vector with 0.0 values to match the length of the longer vector.

        Parameters
        ----------
        other : Any
            The other vector or sequence to subtract

        Returns
        -------
        Vector
            A new instance of the class
        """
        try:
            pairs = zip_longest(self, other, fillvalue=0.0)
            return Vector(vec_el_a - vec_el_b for vec_el_a, vec_el_b in pairs)
        except TypeError:
            return NotImplemented
        
    def __pow__(self, exponent: Union[int, float]) -> 'Vector':
        """
        Compute the power of a vector element-wise.

        Parameters
        ----------
        exponent : Union[int, float]
            The exponent to raise the vector components to

        Returns
        -------
        Vector
            A new instance of the class
        """
        if isinstance(exponent, (int, float)):
            return Vector(pow(vector_element, exponent) for vector_element in self)
        else:
            return NotImplemented
    
    def __mul__(self, scalar: Union[float, int, bool, Fraction]) -> 'Vector':
        """
        Element-wise multiplication of a vector by a scalar.

        Parameters
        ----------
        scalar : Union[float, int, bool, Fraction]
            A scalar value to multiply by

        Returns
        -------
        Vector
            A new instance of the class
        """
        # If scalar cannot be converted to float, not implemented
        try:
            factor = float(scalar)
        except TypeError:
            # Python will try other.__mul__(Vector), which returns TypeError
            return NotImplemented
        return Vector(vector_element * factor for vector_element in self)
    
    def __truediv__(self, other: Union[float, int, bool, Fraction, 'Vector'], floor_division: bool = False) -> 'Vector':
        """
        Element-wise division of a vector by a scalar or another vector.
        If `other` is a vector and vectors have different lengths, the shorter one is padded with ones.

        Parameters
        ----------
        other : Union[float, int, bool, Fraction, Vector]
            A scalar or another vector to divide by
        floor_division : bool
            If True, perform floor division, otherwise perform true division

        Returns
        -------
        Vector
            A new instance of the class with each element divided by the corresponding element of `other` or by `other` if it is a scalar
        """
        if isinstance(other, Vector):
            pairs = zip_longest(self, other, fillvalue=1.0)  # Fill with 1.0 to avoid division by zero
            div_func = floordiv if floor_division else truediv
            return Vector(div_func(vec_el_a, vec_el_b) for vec_el_a, vec_el_b in pairs)
        else:
            try:
                factor = float(other)
            except TypeError:
                return NotImplemented
            div_func = floordiv if floor_division else truediv
            return Vector(div_func(vector_element, factor) for vector_element in self)
    
    def __floordiv__(self, other: Union[float, int, bool, Fraction, 'Vector']) -> 'Vector':
        """
        Element-wise floor division of a vector by a scalar or another vector.
        If `other` is a vector and vectors have different lengths, the shorter one is padded with ones.

        Parameters
        ----------
        other : Union[float, int, bool, Fraction, Vector]
            A scalar or another vector to divide by

        Returns
        -------
        Vector
            A new instance of the class with each element floor-divided by the corresponding element of `other` or by `other` if it is a scalar
        """
        return self.__truediv__(other, floor_division=True)
    
    def __matmul__(self, other: Any) -> float:
        """
        Compute the dot product of two vectors. The dot product is the sum of the products of the
        corresponding elements of the two sequences of numbers. This is a goose typing example, 
        where we allow the `other` operand to be any object that implements the `__len__` and `__iter__`.

        Parameters
        ----------
        other : Any
            The other vector or sequence to compute the dot product with

        Returns
        -------
        float
            The dot product of the two vectors

        Raises
        ------
        ValueError
            If the two vectors have different lengths
        """
        # Check that both operands implement __len__ and __iter__
        if (isinstance(other, Sized) and isinstance(other, Iterable)):
            try:
                # Raise a ValueError when len(self) != len(other) with strict=True
                return sum(vec_el_a * vec_el_b for vec_el_a, vec_el_b in zip(self, other, strict=True))
            except ValueError:
                raise ValueError('@ requires vectors of equal length')
        else:
            return NotImplemented
    
    # Reversed 
    __radd__ = __add__
    __rsub__ = __sub__
    __rpow__ = __pow__
    __rmul__ = __mul__
    __rtruediv__ = __truediv__
    __rfloordiv__ = __floordiv__
    __rmatmul__ = __matmul__
    
    # --------------------------- Comparison operators --------------------------- #
    
    def _cmp(self, other: Union[float, int, bool, Fraction, 'Vector'], comparison_operator: str) -> 'Vector':
        """
        Element-wise comparison of a vector with a scalar or another vector. If the other operand is a vector
        the two vectors must have the same length. If the other operand is a scalar, the comparison is done
        element-wise. The supported comparison operators are: `gt`, `lt`, `ge`, and `le`.
        
        Parameters
        ----------
        other : Union[float, int, bool, Fraction, Vector]
            A scalar or another vector to compare with
        comparison_operator : str
            The comparison operator to use
            
        Returns
        -------
        Vector
            A new instance of the class with the result of the comparison, with values 1.0 for True and 0.0 for False
        """
        match comparison_operator:
            case 'gt':
                cmp = gt
            case 'lt':
                cmp = lt
            case 'ge':
                cmp = ge
            case 'le':
                cmp = le
            case _:
                raise ValueError(f'Unsupported comparison operator: {comparison_operator}')
        
        if isinstance(other, Vector):
            try:
                comparisons = (cmp(vec_el_a, vec_el_b) for vec_el_a, vec_el_b in zip(self, other, strict=True))
            except ValueError:
                raise ValueError(f'operands could not be broadcast with lengths {len(self)} and {len(other)}')
        else:
            try:
                other = float(other)
            except TypeError:
                return NotImplemented
            comparisons = (cmp(vector_element, other) for vector_element in self)
        return Vector(comparisons)
        
    def __gt__(self, other: Union[float, int, bool, Fraction, 'Vector']) -> 'Vector':
        return self._cmp(other, 'gt')

    def __lt__(self, other: Union[float, int, bool, Fraction, 'Vector']) -> 'Vector':
        return self._cmp(other, 'lt')
    
    def __ge__(self, other: Union[float, int, bool, Fraction, 'Vector']) -> 'Vector':
        return self._cmp(other, 'ge')
    
    def __le__(self, other: Union[float, int, bool, Fraction, 'Vector']) -> 'Vector':
        return self._cmp(other, 'le')
    
    # ----------------------------- Sequence protocol ---------------------------- #
    
    def __len__(self) -> int:
        """
        To support the sequence protocol.

        Returns
        -------
        int
            Length of the vector 
        """
        return len(self._components)
    
    def __getitem__(self, key: Union[slice, int]) -> Union[Self, float]:
        """
        To support sequence protocol and slicing operations. The `operator.index`
        function calls `key.__index__()` and raises an error if `key` does not implement
        the `__index__` special method (i.e., it should not be used as an index).

        Parameters
        ----------
        key : Union[slice, int]
            An integer index or a slice object

        Returns
        -------
        Union[Self, float]
            A new instance of the vector that contains the sliced components or a single component
        """
        if isinstance(key, slice):
            cls = type(self)
            # Simply delegate handling of slicing to the _components array
            return cls(self._components[key])
        key_index = index(key)
        return self._components[key_index]
    
    # ---------------------------------- Hashing --------------------------------- #
    
    def __hash__(self) -> int:
        """
        Compute the hash value of the instance. This is an application of map-reduce. At the map stage,
        we apply the `hash` function to each element in the vector. At the reduce stage, we apply the 
        `operator.xor` function to each consecutive pair of hash values, effectively 'reducing' the hash
        values into a single hash value. 
        
        Returns
        -------
        int
            The hash value of the instance
        """
        # This is a generator
        hash_values = (hash(vector_element) for vector_element in self._components)
        return reduce(xor, hash_values, 0)
    
    def __eq__(self, other: Any) -> bool:
        """
        For the two operands to compare equal:
        
        1. They must have the same length
        2. The corresponding elements must be equal
        
        This is also important to have this method in the event of a hash collision.

        Parameters
        ----------
        other : Any
            The other object to compare with

        Returns
        -------
        bool
            True if the two operands are equal, False otherwise
        """
        # Ensure that both operands are instances of Vector
        if isinstance(other, Vector):
            return len(self) == len(other) and all(vec_el_a == vec_el_b for vec_el_a, vec_el_b in zip(self, other))
        else:
            return NotImplemented

def main() -> int:
    
    v1 = Vector([1, 2, 3])
    v2 = Vector([4, 5, 6])
    
    print("Vector v1:", v1)
    print("Vector v2:", v2)
    
    # Vector addition
    print("v1 + v2:", v1 + v2)
    
    # Vector subtraction
    print("v1 - v2:", v1 - v2)
    
    # Scalar multiplication
    print("v1 * 3:", v1 * 3)
    
    # True division
    print("v1 / 2:", v1 / 2)
    
    # Power 
    print("v1 ** 2:", v1 ** 2)
    print("9 ** v1:", 9 ** v1)
    
    # Dot product
    print("v1 @ v2:", v1 @ v2)
    
    # Accessing an element
    print("v1[0]:", v1[0])
    
    # Using bytes to create a new Vector
    bytes_v1 = bytes(v1)
    v1_from_bytes = Vector.frombytes(bytes_v1)
    print("Vector from bytes:", v1_from_bytes)
    
    # Equality check
    print("v1 == v1_from_bytes:", v1 == v1_from_bytes)

    # Boolean context
    print("bool(v1):", bool(v1))
    print("bool(Vector([0, 0, 0])):", bool(Vector([0, 0, 0])))
    
    # Comparison operators
    print("v1 > v2:", v1 > v2)
    print("v1 < v2:", v1 < v2)
    # Other operand not a vector
    print("v1 >= 2:", v1 >= 2)
    print("v1 <= 2:", v1 <= 2)
    print("Fraction(1, 3) < v1:", Fraction(1, 3) < v1)
    
    # Unary operators
    print("+v1:", +v1)
    print("-v1:", -v1)

    return 0

if __name__ == '__main__':
    
    main()
