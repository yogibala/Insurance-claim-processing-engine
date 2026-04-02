class AdjudicationContext(BaseModel):
    ...

    trace: list = []
    error: str | None = None