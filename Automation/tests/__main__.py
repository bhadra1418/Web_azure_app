# automation/tests/__main__.py
import pytest
import sys

exit_code = pytest.main()
sys.exit(exit_code)