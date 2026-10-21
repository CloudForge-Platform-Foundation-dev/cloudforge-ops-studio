import re

from src.ops_studio.api.main import app

LOOPBACK_HTTP = re.compile(r"^http://(localhost|127\.0\.0\.1)(:[0-9]+)?(/.*)?$")


def _spec():
    return app.openapi()


def test_openapi_declares_owner_contact_and_license():
    info = _spec()["info"]
    assert info.get("x-owner")
    assert info.get("contact")
    assert info.get("license")


def test_openapi_declares_governance_metadata():
    info = _spec()["info"]
    assert info.get("x-domain") == "ops"
    assert info.get("x-governance-id") == "CFG-OPS-001"


def test_every_operation_has_a_globally_defined_tag():
    spec = _spec()
    defined = {tag["name"] for tag in spec.get("tags", [])}
    for path, methods in spec["paths"].items():
        for method, operation in methods.items():
            label = f"{method.upper()} {path}"
            assert operation.get("tags"), f"{label} has no tags"
            assert set(operation["tags"]) <= defined, f"{label} uses an undefined tag"


def test_every_operation_declares_security_explicitly():
    for path, methods in _spec()["paths"].items():
        for method, operation in methods.items():
            assert "security" in operation, f"{method.upper()} {path} has no security declaration"


def test_servers_are_https_or_loopback_http():
    servers = _spec().get("servers", [])
    assert servers
    for server in servers:
        url = server["url"]
        assert url.startswith("https://") or LOOPBACK_HTTP.match(url), url
