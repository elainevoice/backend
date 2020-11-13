from api.models.gen_forward import GenForward


class TacoTronAdapter:
    def __init__(self):
        pass

    @staticmethod
    def generate_wav(text):
        gen_forward = GenForward(text)
        save_path = gen_forward.generate_wav()
        return save_path
