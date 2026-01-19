# tests/test_create_map_poster.py
import networkx as nx
from shared import TEST_CITY, TEST_COUNTRY, TEST_COORDS, TEST_DIST, TEST_THEME
from src.create_map_poster import generate_output_filename, process_create_poster


def test_generate_output_file(tmp_path):
    output_file = generate_output_filename(TEST_CITY, TEST_THEME, tmp_path)
    assert output_file.endswith(".png")
    assert TEST_CITY.lower().replace(' ', '_') in output_file


def test_process_create_poster_valid_input(mocker, tmp_path):
    # Mock dependencies
    graph = nx.MultiDiGraph()
    mock_graph_from_point = mocker.patch("osmnx.graph_from_point", return_value=graph)
    mock_features_from_point = mocker.patch("osmnx.features_from_point", return_value=None)
    mock_get_edge_colors_by_type = mocker.patch("src.create_map_poster.get_edge_colors_by_type", return_value=None)
    mock_get_edge_widths_by_type = mocker.patch("src.create_map_poster.get_edge_widths_by_type", return_value=None)
    mock_plot_graph = mocker.patch("src.create_map_poster.ox.plot_graph")
    mock_plt_savefig = mocker.patch("matplotlib.pyplot.savefig")

    # Define parameters
    output_file = generate_output_filename(TEST_CITY, TEST_THEME, tmp_path)

    # Call the function
    process_create_poster(TEST_CITY, TEST_COUNTRY, TEST_COORDS, TEST_DIST, output_file, TEST_THEME)

    # Assertions
    mock_graph_from_point.assert_called_once_with(TEST_COORDS, dist=TEST_DIST, dist_type='bbox', network_type='all')
    mock_features_from_point.assert_has_calls([
        mocker.call(TEST_COORDS, tags={'natural': 'water', 'waterway': 'riverbank'}, dist=TEST_DIST),
        mocker.call(TEST_COORDS, tags={'leisure': 'park', 'landuse': 'grass'}, dist=TEST_DIST)
    ])
    mock_get_edge_colors_by_type.assert_called_once()
    mock_get_edge_widths_by_type.assert_called_once()
    mock_plt_savefig.assert_called_once_with(str(output_file), dpi=300, facecolor="#FFFFFF")
