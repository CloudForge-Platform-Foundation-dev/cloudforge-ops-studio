from src.ops_studio.api.main import app


def test_openapi_declares_owner_contact_and_license():
    info = app.openapi()["info"]
    assert info.get("x-owner")
    assert info.get("contact")
    assert info.get("license")


def test_every_operation_has_a_tag():
    for path, methods in app.openapi()["paths"].items():
        for method, operation in methods.items():
            assert operation.get("tags"), f"{method.upper()} {path} has no tags"
