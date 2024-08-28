import pytest
import tempfile
from pathlib import Path
from ayon_tools.tools import \
    compare_dicts, merge_dicts, import_subclasses_from_string_module, import_module_from_string, \
    import_subclasses_from_path_module, import_module_from_path, show_dict_diffs

def test_compare_dicts_equal():
    dict1 = {"key1": "value1", "key2": "value2"}
    dict2 = {"key1": "value1", "key2": "value2"}
    assert compare_dicts(dict1, dict2)

def test_compare_dicts_not_equal():
    dict1 = {"key1": "value1", "key2": "value2"}
    dict2 = {"key1": "value1", "key2": "different_value"}
    assert not compare_dicts(dict1, dict2)

# def test_compare_dicts_ignore_keys():
#     dict1 = {"key1": "value1", "key2": "value2"}
#     dict2 = {"key1": "value1", "key2": "different_value"}
#     assert compare_dicts(dict1, dict2, ignore_keys="key2")

def test_compare_dicts_nested_dicts():
    dict1 = {"key1": {"subkey1": "subvalue1"}}
    dict2 = {"key1": {"subkey1": "subvalue1"}}
    assert compare_dicts(dict1, dict2)

def test_compare_dicts_nested_dicts_not_equal():
    dict1 = {"key1": {"subkey1": "subvalue1"}}
    dict2 = {"key1": {"subkey1": "different_subvalue"}}
    assert not compare_dicts(dict1, dict2)

def test_merge_dicts_basic():
    dict1 = {"key1": "value1"}
    dict2 = {"key2": "value2"}
    expected = {"key1": "value1", "key2": "value2"}
    result = merge_dicts(dict1, dict2)
    assert result == expected

def test_merge_dicts_nested():
    dict1 = {"key1": {"subkey1": "value1"}}
    dict2 = {"key1": {"subkey2": "value2"}}
    expected = {"key1": {"subkey1": "value1", "subkey2": "value2"}}
    result = merge_dicts(dict1, dict2)
    assert result == expected

# def test_merge_dicts_skip_keys():
#     dict1 = {"key1": "value1", "key2": "value2"}
#     dict2 = {"key2": "new_value2", "key3": "value3"}
#     expected = {"key1": "value1", "key2": "new_value2", "key3": "value3"}
#     result = merge_dicts(dict1, dict2, skip_keys=["key2"])
#     assert result == {"key1": "value1", "key3": "value3"}


def test_import_module_from_string():
    module_code = """
def foo():
    return "bar"
"""
    module_name = "test_module"
    module = import_module_from_string(module_code, module_name)
    assert hasattr(module, "foo")
    assert module.foo() == "bar"


# def test_import_subclasses_from_string_module():
#     module_code = """
# class Parent:
#     pass
#
# class Child(Parent):
#     pass
#
# class Unrelated:
#     pass
# """
#     module_name = "test_module"
#     subclasses = list(
#         import_subclasses_from_string_module(module_code, module_name, parent_class=type("Parent", (), {})))
#     assert len(subclasses) == 1
#     assert subclasses[0].__name__ == "Child"


def test_import_module_from_path():
    code = "def foo(): return 'bar'"
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmpfile:
        tmpfile.write(code.encode())
        tmpfile_path = Path(tmpfile.name)

    module = import_module_from_path(tmpfile_path)
    assert hasattr(module, "foo")
    assert module.foo() == "bar"


# def test_import_subclasses_from_path_module():
#     code = """
# class Parent:
#     pass
#
# class Child(Parent):
#     pass
#
# class Unrelated:
#     pass
# """
#     with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmpfile:
#         tmpfile.write(code.encode())
#         tmpfile_path = Path(tmpfile.name)
#
#     subclasses = list(import_subclasses_from_path_module(tmpfile_path, parent_class=type("Parent", (), {})))
#     assert len(subclasses) == 1
#     assert subclasses[0].__name__ == "Child"

# def test_show_dict_diffs(capsys):
#     dict1 = {"key1": "value1", "key2": "value2"}
#     dict2 = {"key1": "value1", "key2": "different_value", "key3": "extra_value"}
#
#     show_dict_diffs(dict1, dict2)
#
#     captured = capsys.readouterr()
#
#     assert "Missing fields" in captured.out
#     assert "Extra field" in captured.out
#     assert "Changed values" in captured.out