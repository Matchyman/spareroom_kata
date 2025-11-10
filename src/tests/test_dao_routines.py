import pytest
from src.dao.daoRoutines import DaoRoutines


@pytest.mark.asyncio
async def test_get_data():
    dao = DaoRoutines()
    data = await dao.get_data()
    assert isinstance(data, dict)
    # pricing.json should contain at least these keys
    assert set(["a", "b", "c", "d"]).issubset(set(data.keys()))


@pytest.mark.asyncio
async def test_get_data_by_item():
    dao = DaoRoutines()
    item = await dao.get_data_by_item("a")
    assert isinstance(item, dict)
    assert item.get("price") == 50
