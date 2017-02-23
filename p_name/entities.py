class Video:
    def __init__(self, v_id, size):
        super().__init__()
        self.id = v_id
        self.size = size

    def __str__(self, *args, **kwargs):
        return "size: " + str(self.size)


class Endpoint:
    def __init__(self, e_id, ds_latency, cache_connections):
        super().__init__()
        self.ds_latency = ds_latency
        self.cache_connections = cache_connections
        self.id = e_id

    def get_min_latency_cache_connection(self, video: Video):
        filtered_cache_connections = list(
            filter(lambda c: c.cache.place_remained() >= video.size, self.cache_connections))
        return min(filtered_cache_connections,
                   key=lambda c: c.latency) if filtered_cache_connections else CacheConnection(self.ds_latency,
                                                                                               self.ds_latency)

    def get_min_latency_cache_connection_with_video(self, video: Video):
        filtered_cache_connections = list(
            filter(lambda c: video in c.cache.videos, self.cache_connections))
        return min(filtered_cache_connections,
                   key=lambda c: c.latency) if filtered_cache_connections else CacheConnection(self.ds_latency,
                                                                                               self.ds_latency)


class CacheConnection:
    def __init__(self, cache, latency):
        super().__init__()
        self.latency = latency
        self.cache = cache


class Cache:
    def __init__(self, c_id, size):
        super().__init__()
        self.size = size
        self.c_id = c_id
        self.videos = set()

    def add_video(self, video: Video):
        self.videos.add(video)
        if self.place_occupied() > self.size:
            raise Exception('Place exceeded')

    def place_occupied(self):
        return sum(map(lambda v: v.size, self.videos))

    def place_remained(self):
        return self.size - self.place_occupied()


class Requests:
    def __init__(self, endpoint, video, count):
        super().__init__()
        self.count = count
        self.video = video
        self.endpoint = endpoint
        self.rank = 0
        self.best_cache = None
        self.is_valid = False
        self.calc_rank()

    def calc_rank(self):
        best_cache_connection = self.endpoint.get_min_latency_cache_connection(self.video)
        current_best_connection_to_video = self.endpoint.get_min_latency_cache_connection_with_video(self.video)
        self.rank = self.count * (current_best_connection_to_video.latency - best_cache_connection.latency)
        self.best_cache = best_cache_connection.cache
        self.is_valid = True

    def invalid(self, best_cache: Cache, best_video: Video):
        if not self.is_valid:
            return
        my_caches = map(lambda cc: cc.cache, self.endpoint.cache_connections)
        self.is_valid = not (self.best_cache == best_cache or (self.video == best_video and best_cache in my_caches))
