## About
The original bound_timeout decorator was custom written and had the following problems:

1. It doesn't allow for values to be returned on the decorated function
2. It technically runs functions twice in order to get the error message
   if there's no timeout (otherwise the error message is formatted incorrectly.)
3. It doesn't work on Windows (which would be nice, though not necessary)

Some approaches to a timeout decorator won't work consistently on MarkUs, however.
This file contains notes about a few timeout decorators that were tried and their
performance.

### Decorator comparisons

As a legend for what the symbols mean:

- ❌ Does not work
- ✔ Works
- ❓ Not tested yet
- ⚠ There's some problem here

The criteria are as follows:

- ❓ **Works on MarkUs**
- ❓ **Retains original error message if there was no timeout**
- ❓ **Allows for values to be returned on MarkUs**
- ❓ **Works on iOS**
- ❓ **Works on Windows**
- ❓ **Works with pytest.raises**

Additionally, the specific error message

#### The older (original / custom) bound_timeout
Error message says the amount of time that elapsed, but provides no other context.

- ✔ **Works on MarkUs**
- ✔ **Retains original error message if there was no timeout**
- ❌ **Allows for values to be returned on MarkUs**
- ❌ **Works on iOS**
- ❌ **Works on Windows**
- ✔ **Works with pytest.raises**

#### wrapt_timeout_decorator.timeout
Error message says the amount of time that elapsed, and gives a trace for where the code was
when the interrupt/timeout occurred.

- ✔ **Works on MarkUs**
- ✔ **Retains original error message if there was no timeout**
- ✔ **Allows for values to be returned on MarkUs**
- ✔ **Works on iOS**
- ✔ **Works on Windows**
- ✔ **Works with pytest.raises**

#### timeout_decorator
Error message simply says that the test timed out, but provides no information
regarding the time elapsed or any other context.

- ✔ **Works on MarkUs**
- ✔ **Retains original error message if there was no timeout**
- ✔ **Allows for values to be returned on MarkUs**
- ✔ **Works on iOS**
- ❌ **Works on Windows**: Required SIGALRM which isn't available on Windows
- ✔ **Works with pytest.raises**

#### pytest.mark.timeout
No error message was produced properly, so could not be copied.

Note: It's possible that `pytest.mark.timeout` only works for pytests and not for
any other functions that need to be wrapped.

- ❌ **Works on MarkUs**
- ✔ **Retains original error message if there was no timeout**
- ✔ **Allows for values to be returned on MarkUs**
- ⚠ **Works on iOS**: The error message produced was from wrapt_timeout_decorator rather than pytest's.
- ❓ **Works on Windows**
- ✔ **Works with pytest.raises**