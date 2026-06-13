from pd_factory.approval import approval_now

def test_approval_is_exact_revision_and_hash():
    approval = approval_now(
        approval_id="APR-1", target_id="PKG-1", target_revision="v003",
        target_sha256="a" * 64, decision="approved", decided_by="owner",
    )
    assert approval.is_valid_for(target_id="PKG-1", revision="v003", sha256="a" * 64)
    assert not approval.is_valid_for(target_id="PKG-1", revision="v004", sha256="b" * 64)
