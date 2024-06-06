#!/usr/bin/env python3
""" Auth module
"""
from flask import request
from typing import List, TypeVar

class Auth:
    """Class to manage API authentication"""
  
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Public method to determine  authentication """
        if path is None or excluded_paths is None:
            return True
        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
                return False
    return True

    def authorization_header(self, request=None) -> str:
        """Public method to get the authorization header"""
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Public method to get the current user"""
        return None

