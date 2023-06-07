"""A collection of functions with various AST properties for use in
test_code_properties.py
"""


class ExampleClass:

    def recursive_direct(self, x: int) -> int:
        """A recursive method that calls on itself directly.
        """
        if x < 0:
            return 0
        return self.recursive_direct(x - 1)

    def recursive_calls_direct(self, x: int) -> int:
        """A method that calls on a directly recursive method.
        """
        return self.recursive_direct(x)

    def recursive_indirect_a(self, x: int) -> int:
        """A method that calls on another method which calls on this one
        """
        if x < 0:
            return 0
        return self.recursive_indirect_b(x - 1)

    def recursive_indirect_b(self, x: int) -> int:
        """A method that calls on another method which calls on this one
        """
        if x < 0:
            return 0
        return self.recursive_indirect_a(x - 2)

    def recursive_calls_indirect(self, x: int) -> int:
        """A method that calls on an indirectly recursive function.
        """
        return self.recursive_indirect_a(x)

    def empty_pass(self) -> None:
        pass

    def empty_docstring(self) -> None:
        """A method that is empty aside from its docstring."""

    def empty_with_comments(self) -> None:
        """A method that is empty aside from its docstring and comments."""
        # Comment 1
        # Comment 2

    def loop_for(self) -> None:
        """A method with a for-loop."""
        for i in range(10):
            print(i)

    def loop_while(self) -> None:
        """A method with a while-loop."""
        i = 0
        while i > 0:
            i += 1

    def loop_calls_for(self) -> None:
        """A method that calls a function with a for-loop"""
        loop_for()

    def loop_calls_while(self) -> None:
        """A method that calls a function with a while-loop"""
        loop_while()

    def sort_call(self) -> None:
        """A method that calls list.sort()"""
        lst = [1, 2, 3]
        lst.sort()

    def sorted_call(self) -> None:
        """A method that calls sorted()"""
        sorted([1, 2, 3])

    def assert_call(self) -> None:
        """A method that uses assert."""
        assert 1 > 0


class ExampleSubclass(ExampleClass):
    def recursive_calls_inherited(self, x: int) -> int:
        """A method that calls on an inherited recursive method.
        """
        return self.recursive_direct(x)


def recursive_direct(x: int) -> int:
    """A recursive function that calls on itself directly.
    """
    if x < 0:
        return 0
    return recursive_direct(x - 1)


def recursive_calls_direct(x: int) -> int:
    """A function that calls on a directly recursive function.
    """
    return recursive_direct(x)


def recursive_indirect_a(x: int) -> int:
    """A function that calls on another function which calls on this one
    """
    if x < 0:
        return 0
    return recursive_indirect_b(x - 1)


def recursive_indirect_b(x: int) -> int:
    """A function that calls on another function which calls on this one
    """
    if x < 0:
        return 0
    return recursive_indirect_a(x - 2)


def recursive_calls_indirect(x: int) -> int:
    """A function that calls on an indirectly recursive function.
    """
    return recursive_indirect_a(x)


def empty_pass() -> None:
    pass


def empty_docstring() -> None:
    """A function that is empty aside from its docstring."""


def empty_with_comments() -> None:
    """A function that is empty aside from its docstring and comments."""
    # Comment 1
    # Comment 2


def loop_for() -> None:
    """A function with a for-loop."""
    for i in range(10):
        print(i)


def loop_while() -> None:
    """A function with a while-loop."""
    i = 0
    while i > 0:
        i += 1


def loop_calls_for() -> None:
    """A function that calls a function with a for-loop"""
    loop_for()


def loop_calls_while() -> None:
    """A function that calls a function with a while-loop"""
    loop_while()


def sort_call() -> None:
    """A function that calls list.sort()"""
    lst = [1, 2, 3]
    lst.sort()


def sorted_call() -> None:
    """A function that calls sorted()"""
    sorted([1, 2, 3])


def assert_call() -> None:
    """A function that uses assert."""
    assert 1 > 0
