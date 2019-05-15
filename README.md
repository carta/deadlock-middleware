# deadlock-middleware
A middleware to automatically retry requests in the case of a deadlock.

Requires: Django >= 1.11, postgres as database connection, ATOMIC_REQUESTS enabled.

Deadlocks are a common problem with web applications. A deadlock occurs when multiple agents are waiting on locks held by the each other in a way that cannot be resolved. As an example:

```
T1 | T2
A --> B
B --> A
```

Transaction 1 locks A, transaction 2 locks B. When transaction 1 tries to lock B, it waits for transaction 2 which holds the lock. When transaction 2 tries to lock A, these transactions enter a deadlock where both transactions are both waiting on eachother. The deadlock detection in the database will kill one of the two transactions at this point.

The simple solution for the killed transaction is to simply retry. If transaction 2 is killed, the resulting order will be:

```
T1 | T2
A -->
B -->
  --> B
  --> A
```

[From the MySQL docs](https://dev.mysql.com/doc/refman/8.0/en/innodb-deadlocks-handling.html):

> Deadlocks are a classic problem in transactional databases, but they are not dangerous unless they are so frequent that you cannot run certain transactions at all. Normally, you must write your applications so that they are always prepared to re-issue a transaction if it gets rolled back because of a deadlock.

This middleware automatically retries requests that fail due to a deadlock.

To setup:

1. Add `deadlock_middleware` to `INSTALLED_APPS`.
2. Add `deadlock_middleware.DeadlockRetryMiddleware` to `MIDDLEWARES`.
3. Add `DEADLOCK_RETRY_ATTEMPTS` (int) to django `settings.py`. The default is 2 (1 retry).
