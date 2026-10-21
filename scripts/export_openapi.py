"""Write openapi.json from the FastAPI app, or (--check) verify the committed file is current."""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.ops_studio.api.main import app  # noqa: E402

TARGET = ROOT / "openapi.json"


def main():
    spec = app.openapi()
    text = json.dumps(spec, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if "--check" in sys.argv:
        if not TARGET.exists():
            print("openapi.json is missing; run: python scripts/export_openapi.py")
            sys.exit(1)
        committed = json.loads(TARGET.read_text(encoding="utf-8"))
        if committed != spec:
            print("openapi.json is out of date; run: python scripts/export_openapi.py")
            sys.exit(1)
        print("openapi.json is up to date")
        return
    TARGET.write_bytes(text.encode("utf-8"))
    print(f"wrote {TARGET.name}")


if __name__ == "__main__":
    main()
