#!/usr/bin/env python3

from eessi.core import main

# Node type [build, test]
# Arch: [x86_64, arm]

# Usage:
# 1. Request infrastructure. Build node(s). Type + arch(s)
#    Returns DNS names of nodes created.
# 2. Build compatibility layer on arch(s). Implies build node for arch(s).
#    Returns filename of the downloaded tarballs/False.
#    On success, fetches a tarball of the compatibility layer and places it in the output directory.
# 3. Build software on arch(s). Implies build node for arch(s). Fetches compatibility layer from EESSI.
#    On success, fetches a tarball of the software layer and places it in the output directory.
#    Returns filename of the downloaded tarballs/False.
# 4. Build stack. Builds compatibility layer and uses that layer to build software.
#    On success, fetches a tarball of both the compatibility layer and the software layer and places it in the output directory.
#    Returns filename of the downloaded tarballs/False.
# 5. Status. Parses terraform status and shows nodes in a readable fashion.
# 6. Destroy infrastructure. Wipes all nodes.
# 7. Cleanup. Destroys infrastructure, removes all cached files.

if __name__ == "__main__":
    main()
