from pd_factory.idempotency import make_idempotency_key

def test_input_revision_order_does_not_change_key():
    a = make_idempotency_key(stage="x", episode_id="e", input_revisions=["b", "a"], config_revision="c")
    b = make_idempotency_key(stage="x", episode_id="e", input_revisions=["a", "b"], config_revision="c")
    assert a == b

def test_config_change_changes_key():
    a = make_idempotency_key(stage="x", episode_id="e", input_revisions=["a"], config_revision="c1")
    b = make_idempotency_key(stage="x", episode_id="e", input_revisions=["a"], config_revision="c2")
    assert a != b
