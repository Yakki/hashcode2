from p_name.file_parser import FileParser
from p_name.file_writer import FileWriter

filename = "me_at_the_zoo.in".replace(".in", "")

if __name__ == '__main__':
    videos, endpoints, requests, caches = FileParser(filename + ".in").parse_file()

    sorted_requests = sorted(requests, key=lambda r: r.rank, reverse=False)
    while sorted_requests:
        if not sorted_requests[-1].is_valid:
            [r.calc_rank() for r in sorted_requests]
        best_requests = sorted_requests.pop()
        best_requests.best_cache.add_video(best_requests.video)
        [r.invalid(best_requests.best_cache, best_requests.video) for r in sorted_requests]

    FileWriter(filename + ".out", caches).write_file()
