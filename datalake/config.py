class _Config(object):
    APPINSIGHTS_INSTRUMENTATIONKEY = None
    DATALAKE_ACQUIRE_TIMEOUT_SECONDS = None
    DATALAKE_AUTH_REQUIRED = None
    DATALAKE_AZURE_BLOB_ACCOUNT_NAME = None
    DATALAKE_AZURE_BLOB_CONTAINER_NAME = None
    DATALAKE_AZURE_BLOB_ENDPOINT = None
    DATALAKE_AZURE_BLOB_SAS_TOKEN = None
    DATALAKE_AZURE_CONTAINER_CPU_COUNT = 1
    DATALAKE_AZURE_CONTAINER_IMAGE_NAME = None
    DATALAKE_AZURE_CONTAINER_LOCATION = None
    DATALAKE_AZURE_CONTAINER_NAME = None
    DATALAKE_AZURE_CONTAINER_OS_TYPE = 'Linux'
    DATALAKE_AZURE_CONTAINER_RAM_GB = 2
    DATALAKE_AZURE_CONTAINER_RSG_NAME = None
    DATALAKE_EXTRACT_TIMEOUT_SECONDS = None
    DEBUG = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = None


class DevelopmentConfig(_Config):
    DATALAKE_ACQUIRE_TIMEOUT = 600
    DATALAKE_AUTH_REQUIRED = False
    DATALAKE_EXTRACT_TIMEOUT = 600
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestConfig(_Config):
    DATALAKE_ACQUIRE_TIMEOUT = 600
    DATALAKE_AUTH_REQUIRED = True
    DATALAKE_EXTRACT_TIMEOUT = 600
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(_Config):
    DATALAKE_ACQUIRE_TIMEOUT = 3600
    DATALAKE_AUTH_REQUIRED = True
    DATALAKE_EXTRACT_TIMEOUT = 3600
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


CONFIGURATIONS = {
    None: _Config,
    "dev": DevelopmentConfig,
    "test": TestConfig,
    "prod": ProductionConfig
}
