import pytest
from base_agent import BaseAgent


def test_base_agent_initialization():
    agent = BaseAgent()
    assert agent is not None


def test_base_agent_client_property():
    agent = BaseAgent()
    assert agent.client is not None


def test_base_agent_run_method():
    agent = BaseAgent()
    result = agent.run()
    assert result is not None
