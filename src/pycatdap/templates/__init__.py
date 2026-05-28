"""Package marker for pycatdap.templates so files are shipped with the wheel.

Templates are loaded via :func:`importlib.resources.files` from
:mod:`pycatdap.profile.to_html`. This module deliberately has no
runtime code beyond the marker.
"""

from __future__ import annotations
