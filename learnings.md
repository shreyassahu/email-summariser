# LEARNINGS.md

## Day 1 — Async, Concurrency & FastAPI Foundations

- `async def` declares a coroutine — a function that can pause at `await` points and let other coroutines run
- `await` means "I'm waiting on I/O. Event loop, go do something else and come back to me when this finishes"
- Process → Thread → Coroutine, heaviest to lightest. Processes are isolated, threads share memory, coroutines share a thread
- Each FastAPI request runs as a coroutine in a single-threaded event loop
- More cores = more true parallelism, less forced context switching. Fewer cores = more switching to share CPU time
- Cooperative scheduling (coroutines): tasks yield voluntarily at `await`. Preemptive scheduling (OS): hardware timer forcibly interrupts tasks
- OS must use preemptive scheduling because it can't trust programs to yield. Coroutines work inside your app because you trust your own code
- Never put blocking/CPU-heavy work inside an async function without offloading it — it freezes the entire event loop
- Coroutines are for I/O-bound concurrency. Processes are for CPU-bound parallelism
- Coroutines are cheaper than threads because they lie in user space and don't cross user space to go to kernel space.
- A port is a number (0-65535) that routes incoming network requests to the right program on a machine. It's just a door number — your app stands behind one, and requests addressed to that number get delivered to your app. Ports below 1024 are privileged (OS root only). Standard conventions: HTTPS = 443, HTTP = 80, Postgres = 5432. In production, a reverse proxy (like Railway or Nginx) listens on 443 and forwards to your app's assigned port internally.

## Day 2 — Webhooks, Pydantic & Postmark

- A webhook is an external service POSTing data to your endpoint — you don't call them, they call you
- Pydantic validates incoming data shape and types before your code uses it — catches missing/wrong fields at the door instead of mysterious bugs later
- Never name your Python file the same as a standard library module (e.g. `email.py`) — Python imports your file instead of the built-in
- Nested quotes in f-strings: use single quotes inside double quotes when accessing dict keys like `{body['key']}`
- Postmark inbound webhook sends email as JSON with fields like `From`, `Subject`, `TextBody`
