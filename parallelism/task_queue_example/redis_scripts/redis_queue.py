import pickle
import uuid
from typing import Any, Callable, Tuple


class SimpleTask(object):
    """
    Represents a task that can be enqueued and processed later.
    """

    def __init__(self, task_callable: Callable, *args) -> None:
        """
        Initializes a new instance of the SimpleTask class.

        Parameters
        ----------
        task_callable : Callable
            The function or callable object to execute when the task is processed.
        args : Tuple[Any]
            Positional arguments to pass to the callable when executed.
        """
        self.id: str = str(uuid.uuid4())
        self.task_callable: Callable = task_callable
        self.args: Tuple[Any] = args

    def process_task(self) -> Any:
        """
        Executes the task with the provided arguments.

        Returns
        -------
        Any
            The result of the task execution.
        """
        return self.task_callable(*self.args)


class SimpleQueue(object):
    """
    Represents a simple queue system for enqueuing and dequeuing tasks using Redis.
    """

    def __init__(self, connection, name: str) -> None:
        """
        Initialize the SimpleQueue instance.

        Parameters
        ----------
        connection : Redis
            The Redis connection interface.
        name : str
            The name of the queue.
        """
        self.connection = connection
        self.name: str = name

    def enqueue(self, task_callable: Callable, *args) -> str:
        """
        Enqueue a task to the queue. See `https://redis.io/docs/latest/commands/lpush/` for an example.

        Parameters
        ----------
        task_callable : Callable
            The task to enqueue.
        args : Tuple[Any]
            The arguments to pass to the task.

        Returns
        -------
        str
            The ID of the task.
        """
        task = SimpleTask(task_callable, *args)
        serialized_task = pickle.dumps(task, protocol=pickle.HIGHEST_PROTOCOL)
        # Enqueue the task to the queue
        self.connection.lpush(self.name, serialized_task)
        return task.id

    def dequeue(self) -> SimpleTask:
        """
        Dequeue a task from the queue. See `https://redis.io/docs/latest/commands/brpop/` for an example.

        Returns
        -------
        SimpleTask
            The task that was dequeued and processed.
        """
        # Dequeue the task from the queue
        _, serialized_task = self.connection.brpop(self.name)
        task = pickle.loads(serialized_task)
        task.process_task()
        return task

    def size(self) -> int:
        """
        Get the size of the queue. See `https://redis.io/docs/latest/commands/llen/` for an example.

        Returns
        -------
        int
            The size of the queue.
        """
        return self.connection.llen(self.name)
