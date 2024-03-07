import asyncio
from time import monotonic
from typing import Callable

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# Определение модели ответа
class TestResponse(BaseModel):
    elapsed: float


# Асинхронный мьютекс для обеспечения единственности выполнения work()
lock = asyncio.Lock()


# Функция, имитирующая полезную работу
async def work() -> None:
    await asyncio.sleep(3)


# Обработчик для вашего метода
@app.get("/test", response_model=TestResponse)
async def handler() -> TestResponse:
    ts1 = monotonic()
    async with lock:  # Убедимся, что work() выполняется без параллельности
        await work()
    ts2 = monotonic()
    return TestResponse(elapsed=ts2 - ts1)
