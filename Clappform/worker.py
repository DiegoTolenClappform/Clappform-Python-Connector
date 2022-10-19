import os
import json
import redis


class Worker:
    """Helper functions to help with using the worker."""

    def __init__(self, env, action_flow, userid, redis_uri):
        self.key = f"{env}_{action_flow}_{userid}"
        self.r = redis.from_url(redis_uri)

    def Get(self, key: str):
        return self.r.get(f"{self.key}_{key}")

    def Set(self, key: str, value):
        return self.r.set(
            f"{self.key}_{key}",
            value,
        )

    def Keys(self):
        return self.r.keys(f"{self.key}_*")

    @classmethod
    def from_getenv(cls, var="WORKER_TASK_OPTIONS"):
        """Get Worker cache client from environment variable."""
        opts = os.getenv(var)
        if opts is None:
            raise TypeError(f"{var} cannot be undefined")
        elif opts == "":
            raise ValueError(f"{var} cannot be an empty")

        opts = json.loads(opts)
        if not isinstance(opts, dict):
            raise TypeError(f"{var} must be a json object")
        for key in ("env", "action_flow", "userid", "redis_uri"):
            if key not in opts:
                raise KeyError(f"{key} not found in {opts}")
        return cls(opts["env"], opts["action_flow"], opts["userid"], opts["redis_uri"])
