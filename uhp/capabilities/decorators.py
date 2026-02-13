def uhp_capability(func):
    """
    Decorator to mark a function or class as a UHP capability.
    """
    func._is_uhp_capability = True
    return func
