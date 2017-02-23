class FileWriter:
    def __init__(self, file_path, caches):
        super().__init__()
        self.file_path = file_path
        self.caches = [c for c in caches if len(c.videos) != 0]

    def write_file(self):
        lines = [str(len(self.caches))]
        for c in self.caches:
            lines.append(str(c.c_id) + " " + " ".join(list(map(lambda v: str(v.id), c.videos))))
        with open(self.file_path, 'w') as f:
            [f.write(line + '\n') for line in lines]
