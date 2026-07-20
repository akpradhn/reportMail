import matplotlib
import pytest

matplotlib.use("Agg")
from matplotlib import pyplot as plt  # noqa: E402

from reportmail import Chart, Report, UnsupportedChartError


def test_chart_embeds_png_without_closing_by_default() -> None:
    figure, axis = plt.subplots()
    axis.plot([1, 2], [2, 3])
    html = Report("Chart").add(Chart(figure, title="Trend <weekly>", alt='Chart "alt"')).render()
    assert "data:image/png;base64," in html
    assert "Trend &lt;weekly&gt;" in html
    assert "Chart &quot;alt&quot;" in html
    assert plt.fignum_exists(figure.number)
    plt.close(figure)


def test_invalid_chart_object_and_format() -> None:
    with pytest.raises(UnsupportedChartError, match="matplotlib"):
        Report("Bad").add(Chart(object())).render()
    figure = plt.figure()
    chart = Chart(figure)
    chart.image_format = "gif"  # type: ignore[assignment]
    with pytest.raises(UnsupportedChartError, match="format"):
        Report("Bad").add(chart).render()
    plt.close(figure)
