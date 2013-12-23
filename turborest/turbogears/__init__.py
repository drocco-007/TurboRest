import pkgutil
import turbogears

turbogears.__path__ = pkgutil.extend_path(turbogears.__path__, __name__)
