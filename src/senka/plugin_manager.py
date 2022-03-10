from typing import List
import importlib
import os
import re
from traceback import format_exception
from sys import exc_info
import toml

class PluginManager():
  @classmethod
  def get_plugins(cls, chain:str, setting_toml_path:str) -> List:
    try:
      obj = toml.load(setting_toml_path)
      plugins = []
      for module_name in obj['senka']['plugin']['senka_plugin']:
        module = importlib.import_module(f"{module_name}.{module_name}", "module_name")
        dir = re.sub("_(.)",lambda x:x.group(1).upper(), module_name)
        dir = dir[0].upper() + dir[1:]
        plugin_class = getattr(module, dir)
        if plugin_class.chain.lower() == chain.lower(): plugins.append(plugin_class)
      return plugins
    except Exception as e:
      etype, value, tb= exc_info()
      info= format_exception(etype, value, tb)[-2]
      raise RuntimeError(f"Failed to get plugin. plugin name: {module_name}. Exception in{info}")