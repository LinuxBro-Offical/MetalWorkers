# My Questions

- Why `async def`? Will normal `def` work?

  Answer:
  - Yes, normal `def` works. FastAPI will run `def` path operations in a threadpool automatically.
  - Use `async def` when your handler awaits non-blocking I/O (DB drivers, HTTP clients, file/network I/O) to get better concurrency.
  - Use `def` when:
    - You call blocking libraries (non-async DB clients, heavy CPU-bound work).
    - You prefer simplicity and don’t need to `await` anything.
  - Mixing is fine:
    - `async def` + blocking call → can cause event loop blocking (avoid or wrap in a thread via `fastapi.concurrency.run_in_threadpool`).
    - `def` + async lib → not applicable; use async lib from an `async def` handler.
  - Rule of thumb: if you can `await` your I/O, prefer `async def`; otherwise stay with `def`.

- If I am not using `await`, then are `def` and `async def` the same?

  Answer:
  - Short answer: No.
  - `async def` runs on the event loop; any blocking/CPU work inside will block the loop and reduce concurrency.
  - `def` runs in a threadpool (in FastAPI), so blocking work won’t block the event loop.
  - For trivial handlers both “work,” but `async def` gives no benefit without awaits and can be worse if you do blocking work.
  - Prefer `def` for blocking/CPU tasks; use `async def` when you actually await non-blocking I/O. 

- Why use `router.get` instead of `app.get`?

  Answer:
  - `router.get` is for modular endpoints defined in feature modules (e.g., pages/accounts) using `APIRouter`.
  - You then plug routers into the main app with `app.include_router(router)`.
  - Benefits:
    - Feature isolation and organization per module
    - Set prefix/tags/dependencies once on the router
    - Easier reuse and testing
  - `app.get` is fine for small/main-file routes; prefer `router.get` inside modules. 