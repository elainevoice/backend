from api.models.gen_forward import GenForward


class TacoTronAdapter:
    def __init__(self):
        pass

    @staticmethod
    def generate_wav(text, model):
        # Removing trailing newlines (\n on the end of a string) for error prevention
        if "\\" in r"%r" % text:
            text = text.rstrip()
            text = text.replace("\n", " ")

        gen_forward = GenForward(text, model)
        save_path = gen_forward.generate_wav()
        return save_path
