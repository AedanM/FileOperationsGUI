from functools import wraps
from time import time
from typing import Any


def TimeUtility(repetitions=10000, returnResults=False):
    def TimeMethod(func):
        @wraps(func)
        def Wrap(*args, **kw):
            totalTime = 0
            results = []
            for iteration in range(repetitions):
                ts = time()
                runResult = func(*args, **kw)
                te = time()
                results.append(runResult)
                totalTime += float(te - ts)
                if iteration % (repetitions // 10) == 0:
                    print(f"{iteration}/{repetitions} - {iteration/repetitions * 100}%")
                return results if returnResults else None
            print(
                f"Method {func.__name__} took {totalTime:0.3f}s over {repetitions} reps"
                + f" with an average time of {(totalTime/repetitions) * 1000:2.4f} ms"
            )

        return Wrap

    return TimeMethod


def CheckAgainstList(item: Any, tags: list[str]) -> bool:
    return any(tag in str(item) for tag in tags)
