def parse_model(data: dict, model_cls):
    try:
        return model_cls.model_validate(data)
    except Exception as e:
        print("Model Parse Failed:", e)
        return None