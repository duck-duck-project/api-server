# ✈️ Telegram Bot Template

---

Simple template for telegram bot development.

### ✨ Includes DI middleware to pass any argument right into the handlers.

In the [main.py](./src/main.py):

```python
dependency_inject_middleware = DependencyInjectMiddleware(
    user_repository=user_repository,
    # you can pass your objects here
)


# and access them in the handlers
async def on_start(
        message: Message,
        user_repository: UserRepository,
) -> None:
    ...
```

---

### ⚙️ Also includes config parsing template.
