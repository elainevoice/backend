from api.models.gen_forward import GenForward


class TacoTronAdapter():
    def __init__(self):
        pass

    def generate_wav(self, text):
        gen_forward = GenForward(text)
        save_path = gen_forward.generate_wav()
        print('====================')
        print(save_path)
        print('====================')
        return save_path
