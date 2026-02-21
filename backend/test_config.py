"""
Unit tests for configuration module.

Tests configuration loading, validation, and accessor methods.
"""

import os
import pytest
from unittest.mock import patch
from config import Config, ConfigurationError


class TestConfigValidation:
    """Test configuration validation."""
    
    def test_valid_configuration(self):
        """Test that valid configuration passes validation."""
        # This should not raise an exception if .env is properly configured
        try:
            Config.validate()
        except ConfigurationError:
            pytest.fail("Valid configuration should not raise ConfigurationError")
    
    def test_missing_database_url(self):
        """Test that missing DATABASE_URL raises ConfigurationError."""
        with patch.dict(os.environ, {'DATABASE_URL': ''}, clear=False):
            # Reload config values
            with patch.object(Config, 'DATABASE_URL', ''):
                with pytest.raises(ConfigurationError) as exc_info:
                    Config.validate()
                assert "DATABASE_URL" in str(exc_info.value)
    
    def test_invalid_database_url_scheme(self):
        """Test that invalid DATABASE_URL scheme raises ConfigurationError."""
        with patch.object(Config, 'DATABASE_URL', 'postgres://invalid'):
            with pytest.raises(ConfigurationError) as exc_info:
                Config.validate()
            assert "mysql://" in str(exc_info.value)
    
    def test_missing_jwt_secret_key(self):
        """Test that missing JWT_SECRET_KEY raises ConfigurationError."""
        with patch.object(Config, 'JWT_SECRET_KEY', ''):
            with pytest.raises(ConfigurationError) as exc_info:
                Config.validate()
            assert "JWT_SECRET_KEY" in str(exc_info.value)
    
    def test_short_jwt_secret_key(self):
        """Test that short JWT_SECRET_KEY raises ConfigurationError."""
        with patch.object(Config, 'JWT_SECRET_KEY', 'short'):
            with pytest.raises(ConfigurationError) as exc_info:
                Config.validate()
            assert "32 characters" in str(exc_info.value)
    
    def test_invalid_jwt_expiry_hours(self):
        """Test that invalid JWT_EXPIRY_HOURS raises ConfigurationError."""
        with patch.object(Config, 'JWT_EXPIRY_HOURS', 0):
            with pytest.raises(ConfigurationError) as exc_info:
                Config.validate()
            assert "JWT_EXPIRY_HOURS" in str(exc_info.value)
    
    def test_invalid_flask_port(self):
        """Test that invalid FLASK_PORT raises ConfigurationError."""
        with patch.object(Config, 'FLASK_PORT', 99999):
            with pytest.raises(ConfigurationError) as exc_info:
                Config.validate()
            assert "FLASK_PORT" in str(exc_info.value)


class TestConfigAccessors:
    """Test configuration accessor methods."""
    
    def test_get_database_config(self):
        """Test get_database_config returns correct structure."""
        db_config = Config.get_database_config()
        assert 'url' in db_config
        assert db_config['url'] == Config.DATABASE_URL
    
    def test_get_jwt_config(self):
        """Test get_jwt_config returns correct structure."""
        jwt_config = Config.get_jwt_config()
        assert 'secret_key' in jwt_config
        assert 'algorithm' in jwt_config
        assert 'expiry_hours' in jwt_config
        assert jwt_config['secret_key'] == Config.JWT_SECRET_KEY
        assert jwt_config['algorithm'] == 'HS256'
        assert jwt_config['expiry_hours'] == Config.JWT_EXPIRY_HOURS
    
    def test_get_flask_config(self):
        """Test get_flask_config returns correct structure."""
        flask_config = Config.get_flask_config()
        assert 'env' in flask_config
        assert 'debug' in flask_config
        assert 'host' in flask_config
        assert 'port' in flask_config
        assert flask_config['env'] == Config.FLASK_ENV
        assert flask_config['debug'] == Config.FLASK_DEBUG
    
    def test_get_cors_config(self):
        """Test get_cors_config returns correct structure."""
        cors_config = Config.get_cors_config()
        assert 'origins' in cors_config
        assert 'supports_credentials' in cors_config
        assert isinstance(cors_config['origins'], list)
        assert cors_config['supports_credentials'] is True
    
    def test_get_cookie_config(self):
        """Test get_cookie_config returns correct structure."""
        cookie_config = Config.get_cookie_config()
        assert 'secure' in cookie_config
        assert 'httponly' in cookie_config
        assert 'samesite' in cookie_config
        assert 'max_age' in cookie_config
        assert cookie_config['httponly'] is True
        assert cookie_config['samesite'] == 'Strict'
        assert cookie_config['max_age'] == Config.JWT_EXPIRY_HOURS * 3600


class TestConfigEnvironmentChecks:
    """Test environment checking methods."""
    
    def test_is_production(self):
        """Test is_production returns correct value."""
        with patch.object(Config, 'FLASK_ENV', 'production'):
            assert Config.is_production() is True
        
        with patch.object(Config, 'FLASK_ENV', 'development'):
            assert Config.is_production() is False
    
    def test_is_development(self):
        """Test is_development returns correct value."""
        with patch.object(Config, 'FLASK_ENV', 'development'):
            assert Config.is_development() is True
        
        with patch.object(Config, 'FLASK_ENV', 'production'):
            assert Config.is_development() is False


class TestConfigDefaults:
    """Test configuration default values."""
    
    def test_jwt_algorithm_default(self):
        """Test JWT_ALGORITHM has correct default."""
        assert Config.JWT_ALGORITHM == 'HS256'
    
    def test_cookie_httponly_default(self):
        """Test COOKIE_HTTPONLY has correct default."""
        assert Config.COOKIE_HTTPONLY is True
    
    def test_cookie_samesite_default(self):
        """Test COOKIE_SAMESITE has correct default."""
        assert Config.COOKIE_SAMESITE == 'Strict'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
