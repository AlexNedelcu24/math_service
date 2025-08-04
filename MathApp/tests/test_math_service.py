import pytest
from app.services.math_service import MathService


@pytest.mark.asyncio
async def test_pow():
    svc = MathService()
    assert await svc.compute("pow", 3, 2) == 9


@pytest.mark.asyncio
async def test_fib():
    svc = MathService()
    assert await svc.compute("fib", 7) == 13


@pytest.mark.asyncio
async def test_fact():
    svc = MathService()
    assert await svc.compute("fact", 5) == 120


@pytest.mark.asyncio
async def test_invalid():
    svc = MathService()
    with pytest.raises(ValueError):
        await svc.compute("unknown", 3)
