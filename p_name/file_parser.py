from p_name.entities import CacheConnection, Cache, Video, Endpoint, Requests


class FileParser:
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.file = None
        self.v_count, self.e_count, self.r_count, self.c_count, self.c_size = 0, 0, 0, 0, 0

    def create_cache_connections(self, connections_count, caches):
        cache_connections = []
        for i in range(0, connections_count):
            cache_id, latency = self.next_line()
            cache_connections.append(CacheConnection(caches[int(cache_id)], int(latency)))
        return cache_connections

    def parse_file(self):
        with open(self.file_path, 'r', encoding="utf8") as f:
            self.file = f
            caches, endpoints, requests, videos = self.read_lines()
        return videos, endpoints, requests, caches

    def read_lines(self):
        self.read_counts_line()
        caches = [Cache(i, self.c_size) for i in range(0, int(self.c_count))]
        videos = [Video(i, int(size)) for i, size in enumerate(self.next_line())]
        endpoints = self.read_endpoints(caches)
        requests = self.read_requests(endpoints, videos)
        return caches, endpoints, requests, videos

    def read_requests(self, endpoints, videos):
        requests = []
        for r_id in range(0, self.r_count):
            v_id, e_id, count = self.next_line()
            requests.append(Requests(endpoints[int(e_id)], videos[int(v_id)], int(count)))
        return requests

    def read_endpoints(self, caches):
        endpoints = []
        for e_id in range(0, self.e_count):
            latency, e_c_count = self.next_line()
            endpoints.append(Endpoint(e_id, int(latency), self.create_cache_connections(int(e_c_count), caches)))
        return endpoints

    def read_counts_line(self):
        v_count, e_count, r_count, c_count, c_size = tuple(self.next_line())
        self.v_count, self.e_count, self.r_count, self.c_count, self.c_size = int(v_count), int(e_count), int(
            r_count), int(c_count), int(
            c_size)

    def next_line(self):
        return tuple(self.file.readline().strip().split(" "))
