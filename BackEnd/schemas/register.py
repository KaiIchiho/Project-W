def register(name:str,registry:dict):
    def decorator(cls):
        registry[name]=cls
        return cls
    return decorator