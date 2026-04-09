from pydantic import BaseModel, ConfigDict

def parse_model(data: dict, model_cls):
    # try:
    #     return model_cls.model_validate(data)
    # except Exception as e:
    #     print("Model Parse Failed:", e)
    #     return None
    try:
        return model_cls.model_validate(data, strict=True)
    except Exception as e:
        return None
    # try:
    #     if not hasattr(model_cls, 'model_config'):
    #         model_cls.model_config = ConfigDict(extra='allow')
    #     return model_cls.model_validate(data)
    # except Exception as e:
    #     print("Model Parse Failed:", e)
    #     return None