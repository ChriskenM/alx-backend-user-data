#!/usr/bin/env python3
"""
Session Authentication views
"""

from flask import request, abort, jsonify
from models.user import User
from api.v1.app import auth

from . import app_views

@app_views.route('/auth_session/login', methods=['POST', 'GET'], strict_slashes=False)
def session_login():
    """Handles user login using Session Authentication"""
    if request.method == 'GET':
        abort(405)

    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search({'email': email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Creates a session for the user
    session_id = auth.create_session(user[0].id)

    # Sets the session ID as a cookie
    response = jsonify(user[0].to_json())
    response.set_cookie(auth.session_name, session_id)

    return response, 200

    @app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
    def session_logout():
        """Handles user logout"""
        if request.method == 'DELETE':
            if not auth.destroy_session(request):
                abort(404)
            return jsonify({}), 200
