# import all gumpy submodules that should be loaded automatically
import Utils.gumpy.gumpy.classification
import Utils.gumpy.gumpy.data
import Utils.gumpy.gumpy.plot
import Utils.gumpy.gumpy.signal
import Utils.gumpy.gumpy.utils
import Utils.gumpy.gumpy.features
import Utils.gumpy.gumpy.split

# fetch into gumpy-scope so that users don't have to specify the entire
# namespace
from Utils.gumpy.gumpy.classification import classify

# retrieve the gumpy version (required for package manager)
from Utils.gumpy.gumpy.version import __version__
