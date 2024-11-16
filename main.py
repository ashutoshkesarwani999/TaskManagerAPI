import uvicorn

from core.config import config

if __name__ == "__main__":
    uvicorn.run(
        app="core.server:app",
        host="0.0.0.0",
        port=config.APIPORT,
        reload=True if config.ENVIRONMENT != "production" else False,
        workers=1,
    )