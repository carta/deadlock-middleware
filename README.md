# deadlock-middleware
A middleware to automatically retry requests in the case of a deadlock.

Note: only tested with django postgres psycopg2

Deadlocks are a common problem with web applications. A deadlock occurs when multiple agents are waiting on locks held by the each other in a way that cannot be resolved. As an example:

```
T1 | T2
A --> B
B --> A
```

Transaction 1 is waiting on B which is locked by transaction 2. When transaction 2 tries to lock A, these transactions are in a deadlock and are both waiting on eachother. The deadlock detection in the database will kill transaction 2 at this point.

The simple solution for transaction 2 is to simply retry its transaction now. The resulting order will be:

```
T1 | T2
A -->
B -->
  --> B
  --> A
```

From the MySQL docs:

> Deadlocks are a classic problem in transactional databases, but they are not dangerous unless they are so frequent that you cannot run certain transactions at all. Normally, you must write your applications so that they are always prepared to re-issue a transaction if it gets rolled back because of a deadlock.

https://dev.mysql.com/doc/refman/8.0/en/innodb-deadlocks-handling.html

This middleware automatically retries requests that fail due to a deadlock.

To setup:

1. Add `deadlock_middleware` to `INSTALLED_APPS`.
2. Add `deadlock_middleware.DeadlockRetryMiddleware` to `MIDDLEWARES`.
3. Add `DEADLOCK_RETRY_ATTEMPTS` (int) to django `settings.py`. The default is 2 (1 retry).
