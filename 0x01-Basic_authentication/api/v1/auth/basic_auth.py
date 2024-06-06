#!/usr/bin/env python3
""" BasicAuth module
"""
import base64
from typing import TypeVar, Tuple
from api.v1.auth.auth import Auth
from models.user import User

class BasicAuth(Auth):
    """ BasicAuth class inherits from Auth """

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """ Extracts the Base64 part of the Authorization header """
        if authorization_header is None or not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """ Decodes the Base64 string """
        if base64_authorization_header is None or not isinstance(base64_authorization_header, str):
            return None
        try:
            base64_bytes = base64_authorization_header.encode('utf-8')
            decoded_bytes = base64.b64decode(base64_bytes)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """ Extracts user email and password from the Base64 decoded value """
        if decoded_base64_authorization_header is None or not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        user_email, user_pwd = decoded_base64_authorization_header.split(':', 1)
        return user_email, user_pwd

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ Returns the User instance based on email and password """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        if not users:
            return None
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """ Retrieves the User instance for a request """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        base64_auth = self.extract_base64_authorization_header(auth_header)
        if base64_auth is None:
            return None
        decoded_auth = self.decode_base64_authorization_header(base64_auth)
        if decoded_auth is None:
            return None
        user_email, user_pwd = self.extract_user_credentials(decoded_auth)
        if user_email is None or user_pwd is None:
            return None
        return self.user_object_from_credentials(user_email, user_pwd)

