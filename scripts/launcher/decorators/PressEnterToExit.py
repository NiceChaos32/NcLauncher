def press_enter(s, c):
    def decorator(func):
        def wrapper(*args, **kwargs):
            func(s, c)
            _press_enter = input("\nPress Enter to continue...")
        return wrapper
    return decorator