import asyncio
from datetime import datetime
from typing import Any, Callable


class SimpleAsyncScheduler:
    def __init__(self):
        self.tasks = []
        self._running = False

    async def add_task(self,
                     func: Callable,
                     run_at: datetime,
                     *args: Any,
                     **kwargs: Any) -> None:
        self.tasks.append({
            'func': func,
            'run_at': run_at,
            'args': args,
            'kwargs': kwargs,
            'executed': False
        })
        if not self._running:
            asyncio.create_task(self._run())

    async def _run(self) -> None:
        self._running = True
        try:
            while self._running:
                now = datetime.now()
                next_check = None

                for task in self.tasks:
                    if not task['executed']:
                        if task['run_at'] <= now:
                            try:
                                if asyncio.iscoroutinefunction(task['func']):
                                    await task['func'](*task['args'], **task['kwargs'])
                                else:
                                    task['func'](*task['args'], **task['kwargs'])
                            except Exception as e:
                                print(f"task execute error: {e}")
                            finally:
                                task['executed'] = True
                        else:
                            wait_time = (task['run_at'] - now).total_seconds()
                            if next_check is None or wait_time < next_check:
                                next_check = wait_time

                self.tasks = [t for t in self.tasks if not t['executed']]

                wait_time = min(next_check, 1.0) if next_check is not None else 1.0
                if wait_time > 0:
                    await asyncio.sleep(wait_time)

                if not any(not t['executed'] for t in self.tasks):
                    break
        finally:
            self._running = False

    def stop(self) -> None:
        self._running = False