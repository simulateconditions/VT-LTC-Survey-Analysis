import os, sys
BINARIES_PATHS = [
    os.path.join(sys.frozen_dir, 'lib/opencv_python.libs')
] + BINARIES_PATHS
