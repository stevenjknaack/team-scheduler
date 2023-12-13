# test-tutorial
This is my take away when I learn testing idea, especially in Python.
## Pytest
Always good to go to the official document first:
- [official document](https://flask.palletsprojects.com/en/3.0.x/testing/)

Great blogs for `pytest` idea and `TDD`...
- [blogs about fixture, pytest, a little bit TDD idea](https://realpython.com/pytest-python-testing/)
- [Hand by hand tutorial on how run pytest, flags, read test result](https://www.tutorialspoint.com/pytest/index.htm)
- [Similar to the previous one, on how to read and run tests, but with more code snippet](https://www.guru99.com/pytest-tutorial.html)

## Key Concepts
- `Decorators` are a syntactic element in Python that modify the operation of a function.
- `Exceptions` are signals that are emitted when an error occurs during the execution of a program. Importantly, exceptions are Python objects that have a specific type that is specified by the code that raises the exception. For example, if one tries to open a non-existent file using open(), it will raise a FileNotFoundError exception, whereas if one tries to divide by zero the Python interpreter will raise a ZeroDivisionError exception.
- `Context` managers are a syntatic element that are usually used to control resources like file or database handles, but can also be used to monitor and control the operation of a set of functions, which will be useful when we are looking for specific exceptions.

## Parametric Tests
If there are no parameters, pytest will look for test files (beginning with 'test_' or ending with '_test') in the current directory and all subdirectories and run them. You can also specify a file name, directory name, or a list of these name. But it's possible to turn one more options:
- `@pytest.mark.parametize` will only run the tests with this parameter.
## Test Design Idea
- we need to try to cause the program to make errors.
## Run Tests
Basic commands:
- pytest <test_file_name>.py

return more information:

- pytest <test_file_name>.py -v
- pytest <test_file_name>.py --verbose

## Tests Results
Here're possible test results:
- `PASSED (.)`: The test was successful.
- `FAILED (F)`: The test failed (or XPASS + strict).
- `SKIPPED (s)`: The test was skipped. You can use the @pytest.mark.skip() or pytest.mark.skipif() decorators to instruct pytest to skip the test.
- `xfail (x)`: The test is expected to fail. Use @pytest.mark.xfail().
- `XPASS (X)`: The test unexpectedly passed.
-`ERROR (E)`: There was an error during the test.
  
