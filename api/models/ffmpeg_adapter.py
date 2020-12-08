import ffmpeg


class FfmpegAdapter:
    def __init__(self, bytes, path, new_path):
        self.bytes = bytes
        self.path = path
        self.new_path = new_path

    def run(self):
        with open(self.path, mode="wb+") as f:
            f.write(self.bytes)
            f.close()
        stream = ffmpeg.input(self.path)
        output = stream.output(self.new_path, format="wav")
        output.run()
