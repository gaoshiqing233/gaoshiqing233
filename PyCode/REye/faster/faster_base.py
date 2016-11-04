#!/usr/bin/env python
# encoding: utf-8
from concurrent.futures import ThreadPoolExecutor, as_completed
MAX_WORKERS = 10


class Faster(object):

    futures = set()
    canceled = False

    def __init__(self, worker, works):
        self.worker = worker
        self.works = works

    def run(self):
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            for work in self.works:
                future = executor.submit(self.worker, work)
                self.futures.add(future)
            done = self._process(self.futures)
            print(done)

            if self.canceled:
                executor.shutdown()

    def _process(self):

        done = 0
        results = self._wait_for(self.futures)

        if not self.canceled:
            for result in (result for ok, result in results if ok and result is not None):
                done += 1

        return done

    def _wait_for(self):
        results = []

        try:
            for future in as_completed(self.futures):
                err = future.exception()

                if err is None:
                    ok, result = future.result()

                    if not ok:
                        pass

                    elif result is not None:
                        pass
                    results.append((ok, result))
        except Exception:
            self.canceled = True

            for future in self.futures:
                future.cancel()
