import pytest
from school_map import find_shortest_path, get_locations, is_valid_location , school_map

class TestSchoolNavigation:
    def test_find_shortest_path_success(self):
        result = find_shortest_path(school_map, "Main Gate", "Lab")
        assert result["status"] == "success"
        assert result["path"] == ["Main Gate", "Block A", "Library", "Lab"]
        assert result["distance"] == 15

    def test_find_shortest_path_no_path(self):
        result = find_shortest_path(school_map, "Playground", "Admin")
        assert result["status"] == "error"
        assert result["path"] == []
        assert result["distance"] == 0

    def test_invalid_locations(self):
        result = find_shortest_path(school_map, "Gym", "Pool")
        assert result["status"] == "error"
        assert result["path"] == []
        assert result["distance"] == 0

    def test_get_locations(self):
        locations = get_locations()
        assert len(locations) == 6
        assert "Main Gate" in locations
        assert "Lab" in locations

    def test_validate_location(self):
        assert is_valid_location("Library") == True
        assert is_valid_location("Swimming Pool") == False

    def test_same_start_end(self):
        result = find_shortest_path(school_map, "Main Gate", "Main Gate")
        assert result["status"] == "success"
        assert result["path"] == ["Main Gate"]
        assert result["distance"] == 0
