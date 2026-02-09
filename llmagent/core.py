"""Compatibility layer exposing the functions used by tests.

This module re-exports `get_file_content` from `functions.get_file_content`.
"""
from functions.get_file_content import get_file_content

__all__ = ["get_file_content"]
