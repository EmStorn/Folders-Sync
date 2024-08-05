import pytest
from unittest.mock import patch
from modules.user_inputs import path_input_validation, sync_interval_validation, get_path_input, get_sync_interval_input

# Tests for path_input_validation() function
def test_valid_folder(tmp_path):
    valid_folder_path = str(tmp_path)
    result = path_input_validation(valid_folder_path)
    assert result == valid_folder_path

def test_invalid_folder_path():
    invalid_path = "not/a/valid/path"
    result = path_input_validation(invalid_path)
    assert result is None

def test_path_not_a_directory(tmp_path):
    file_path = tmp_path / "test_file.txt"
    file_path.write_text('text for testing')
    result = path_input_validation(str(file_path))
    assert result is None

# Test for sync_interval_validation() function
@pytest.mark.parametrize(
        "input_value, expected_result",
        [
            ("60", "60"),
            ("1000000", "1000000"),
            ("1.5", None),
            ("1,5", None),
            ("0", None),
            ("-60", None),
            ("-1000000", None),
            ("text_input", None),
        ]
)
def test_sync_interval_validation(input_value, expected_result):
    result = sync_interval_validation(input_value)
    assert result == expected_result

# Tests for get_path_input() function
def test_get_path_valid_input(tmp_path):
    valid_path = str(tmp_path)
    with patch('builtins.input', return_value=valid_path):
        result = get_path_input("testing")
        assert result == valid_path

def test_get_path_invalid_input(tmp_path):
    invalid_path = "not/a/valid/path"
    with patch('builtins.input', side_effect=[invalid_path, str(tmp_path)]):
        result = get_path_input("testing")
        assert result == str(tmp_path)

# Tests for get_sync_input() function
def test_get_sync_interval_valid_input():
    valid_interval = '60'
    with patch('builtins.input', return_value=valid_interval):
        result = get_sync_interval_input()
        assert result == int(valid_interval)

def test_get_sync_interval_invalid_input_text():
    invalid_interval_text = 'abc'
    valid_interval = '60'
    with patch('builtins.input', side_effect=[invalid_interval_text, valid_interval]):
        result = get_sync_interval_input()
        assert result == int(valid_interval)

def test_get_sync_interval_invalid_input_negative():
    invalid_interval_negative = '-5'
    valid_interval = '60'
    with patch('builtins.input', side_effect=[invalid_interval_negative, valid_interval]):
        result = get_sync_interval_input()
        assert result == int(valid_interval)