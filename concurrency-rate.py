from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from typing import Dict
import time


class RateLimiter:
    def __init__(self, requests_per_second: int):
        self.requests_per_second = requests_per_second
        self.requests: Dict[str, List[float]] = {}
        self.lock = asyncio.Lock()

    async def is_allowed(self, client_id: str) -> bool:
        async with self.lock:
            now = time.time()
            if client_id not in self.requests:
                self.requests[client_id] = []

            # Remove old requests
            self.requests[client_id] = [
                req_time for req_time in self.requests[client_id] if now - req_time < 1
            ]

            if len(self.requests[client_id]) >= self.requests_per_second:
                return False

            self.requests[client_id].append(now)
            return True


rate_limiter = RateLimiter(requests_per_second=5)


@app.get("/rate-limited")
async def rate_limited_endpoint(client_id: str):
    if not await rate_limiter.is_allowed(client_id):
        raise HTTPException(status_code=429, detail="Too many requests")
    return {"message": "Success"}


# Test rate limiting
@pytest.mark.asyncio
async def test_rate_limiting():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Send requests at a rate higher than the limit
        tasks = [
            client.get("/rate-limited", params={"client_id": "test_client"})
            for _ in range(10)
        ]

        responses = await asyncio.gather(*tasks, return_exceptions=True)

        # Count successful and rate-limited responses
        success_count = sum(1 for r in responses if getattr(r, "status_code", 0) == 200)
        rate_limited_count = sum(
            1 for r in responses if getattr(r, "status_code", 0) == 429
        )

        assert success_count == 5  # First 5 requests should succeed
        assert rate_limited_count == 5  # Next 5 should be rate limited
