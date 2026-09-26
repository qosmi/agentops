from agentops.llm.fake import FakeLLMProvider


def test_fake_llm_returns_response() -> None:
    llm = FakeLLMProvider(
        response="This is a test response."
    )

    result = llm.generate(
        system_prompt="You are an analyst.",
        user_prompt="Analyze this.",
    )

    assert result == "This is a test response."
