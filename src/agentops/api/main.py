from fastapi import FastAPI

from agentops.api.routes import router


def create_app() -> FastAPI:
    app = FastAPI(
        title="AgentOps",
        description=(
            "Autonomous business process analysis "
            "and investigation API."
        ),
        version="0.1.0",
    )

    app.include_router(router)

    return app


app = create_app()