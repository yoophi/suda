import os
import yaml
from flask import Flask as BaseFlask, Config as BaseConfig


class Config(BaseConfig):
    def from_heroku(self):
        # Register database schemes in URLs.
        for key in ['DATABASE_URL']:
            if key in os.environ:
                self['SQLALCHEMY_DATABASE_URI'] = os.environ[key]
                break

        for key in ['SECRET_KEY', 'GOOGLE_ANALYTICS_ID', 'ADMIN_CREDENTIALS', 'SECURITY_PASSWORD_SALT']:
            if key in os.environ:
                self[key] = os.environ[key]

    def from_yaml(self, root_path, config_name=None):
        env = os.environ.get('FLASK_ENV', 'development').upper()
        self['ENVIRONMENT'] = env.lower()

        if not config_name:
            config_name = env

        config_name = config_name.upper()

        for path in ('/etc', os.path.dirname(root_path), root_path,):
            config_file = os.path.join(path, 'config.yml')

            try:
                with open(config_file) as f:
                    c = yaml.load(f)

                # c = c.get(env, c)
                c = c.get(config_name, c)
                import q; q(c)
                import q; q(config_name)

                for key in c.iterkeys():
                    if key.isupper():
                        self[key] = c[key]
            except:
                pass


class Flask(BaseFlask):
    """Extended version of `Flask` that implements custom config class
    and adds `register_middleware` method"""

    def make_config(self, instance_relative=False):
        root_path = self.root_path
        if instance_relative:
            root_path = self.instance_path
        return Config(root_path, self.default_config)

    def register_middleware(self, middleware_class):
        """Register a WSGI middleware on the application
        :param middleware_class: A WSGI middleware implementation
        """
        self.wsgi_app = middleware_class(self.wsgi_app)
