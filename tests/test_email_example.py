import importlib.util
from pathlib import Path
from types import ModuleType


def load_email_example() -> ModuleType:
    path = Path(__file__).parents[1] / "examples" / "send_email_report.py"
    spec = importlib.util.spec_from_file_location("send_email_report", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_email_example_supports_cid_and_data_uri_images() -> None:
    example = load_email_example()

    cid_message = example.build_message(
        example.build_report(),
        "sender@example.com",
        "recipient@example.com",
        image_mode="cid",
    )
    cid_source = cid_message.as_string()
    assert "cid:reportmail-chart-1" in cid_source
    assert "Content-ID: <reportmail-chart-1>" in cid_source
    assert "Content-Disposition: inline" in cid_source

    data_uri_message = example.build_message(
        example.build_report(),
        "sender@example.com",
        "recipient@example.com",
        image_mode="data-uri",
    )
    assert "data:image/png;base64," in data_uri_message.as_string()
    assert "Content-ID: <reportmail-chart-1>" not in data_uri_message.as_string()
