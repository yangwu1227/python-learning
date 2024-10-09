from multiprocessing import Process

from redis_queue_worker import worker

num_processes = 3


def main() -> int:
    processes = []
    for _ in range(num_processes):
        process = Process(target=worker)
        processes.append(process)
        process.start()
    # Wait for all child processes to complete
    for process in processes:
        process.join()

    return 0


if __name__ == "__main__":
    main()
