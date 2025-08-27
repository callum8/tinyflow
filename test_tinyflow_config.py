import pytest
from tinyflow_config import Orchestrate

# Test that Orchestrate builds the transform dictionary correctly from the YAML file

def test_orchestrate_dict1_builds_correctly():
    str_uuid = '5cd854ff-0036-4826-969c-1a61710d8d97'
    orch = Orchestrate('ConfigYAML.yaml', str_uuid)
    assert isinstance(orch.dict1, dict)
    assert len(orch.dict1) > 0
    # Check for a known UUID from the config
    assert '1451040e-2e8c-478c-91c4-c936153469a7' in orch.dict1

# Test lookup_task returns the correct query string

def test_lookup_task_returns_query():
    str_uuid = '5cd854ff-0036-4826-969c-1a61710d8d97'
    orch = Orchestrate('ConfigYAML.yaml', str_uuid)
    query = orch.lookup_task('1451040e-2e8c-478c-91c4-c936153469a7s')
    assert isinstance(query, str)
    assert 'copy' in query or 'select' in query
