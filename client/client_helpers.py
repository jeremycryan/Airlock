#!/usr/bin/env python
import os
import sys

def source_path(relative):
    return "airlockgraphics/"+relative #TODO make this better if we want an executable
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)
