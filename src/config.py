import yaml
from flask import Flask as BaseFlask, Config as BaseConfig


class Config(BaseConfig):

    def from_yaml(self, config_file, field='FLASK'):
        with open(config_file) as f:
            c = yaml.safe_load(f)

        c = c.get(field, c)

        for key in c.keys():
            if key.isupper():
                self[key] = c[key]


class Flask(BaseFlask):

    def make_config(self, instance_relative=False):
        root_path = self.root_path
        if instance_relative:
            root_path = self.instance_path

        return Config(root_path, self.default_config)

