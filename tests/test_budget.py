import pytest
from pd_factory.budget import BudgetExceeded, BudgetLedger, BudgetPolicy

def test_soft_warning_and_hard_block():
    ledger = BudgetLedger(BudgetPolicy(soft_limit=10, hard_limit=20))
    assert ledger.reserve(11) == "soft_limit_warning"
    with pytest.raises(BudgetExceeded):
        ledger.reserve(10)
