"""
This module defines the permission scopes for different user roles in the system.

The roles and their corresponding scopes are:
- sysadmin: Has full access, including admin, manage, write, and read permissions.
- user: Has read and write permissions.

Constants:
    ROLE_SCOPES (dict): A dictionary mapping each role to a list of permission scopes.
"""

ROLE_SCOPES = {"sysadmin": ["admin", "manage", "write", "read"], "user": ["read", "write"]}
