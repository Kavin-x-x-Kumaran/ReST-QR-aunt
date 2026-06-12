"""
Authentication app configuration.

Provides serializers, views, permissions, and models for user authentication.
"""
from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    """Configures authentication app."""
    
    name = 'authentication'
