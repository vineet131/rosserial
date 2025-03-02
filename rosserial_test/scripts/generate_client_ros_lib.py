__usage__ = """
make_libraries generates the rosserial library files.  It
is passed the output folder. This version does not copy a ros.h,
as that is provided by the test harnesses. For use only by the
rosserial_test CMake setup.
"""

import rospkg
from rosserial_client.make_library import *
from os import path, sep, walk
import re
import sys

ROS_TO_EMBEDDED_TYPES = {
    'bool'    :   ('bool',              1, PrimitiveDataType, []),
    'byte'    :   ('int8_t',            1, PrimitiveDataType, []),
    'int8'    :   ('int8_t',            1, PrimitiveDataType, []),
    'char'    :   ('uint8_t',           1, PrimitiveDataType, []),
    'uint8'   :   ('uint8_t',           1, PrimitiveDataType, []),
    'int16'   :   ('int16_t',           2, PrimitiveDataType, []),
    'uint16'  :   ('uint16_t',          2, PrimitiveDataType, []),
    'int32'   :   ('int32_t',           4, PrimitiveDataType, []),
    'uint32'  :   ('uint32_t',          4, PrimitiveDataType, []),
    'int64'   :   ('int64_t',           8, PrimitiveDataType, []),
    'uint64'  :   ('uint64_t',          4, PrimitiveDataType, []),
    'float32' :   ('float',             4, PrimitiveDataType, []),
    'float64' :   ('double',             4, PrimitiveDataType, []),
    'time'    :   ('ros::Time',         8, TimeDataType, ['ros/time']),
    'duration':   ('ros::Duration',     8, TimeDataType, ['ros/duration']),
    'string'  :   ('char*',             0, StringDataType, []),
    'Header'  :   ('std_msgs::Header',  0, MessageDataType, ['std_msgs/Header'])
}

# need correct inputs
if (len(sys.argv) < 2):
    print(__usage__)
    exit()

# output path
path = path.join(sys.argv[1], 'rosserial')
print("\nExporting to %s" % path)

rospack = rospkg.RosPack()
rosserial_client_copy_files(rospack, path + sep)
rosserial_generate(rospack, path, ROS_TO_EMBEDDED_TYPES)

# Rewrite includes to find headers in a subdirectory. This is important in the context of
# test nodes as we must distinguish the rosserial client headers from roscpp headers of
# the same name.
for dname, dirs, files in walk(path):
    for fname in files:
        fpath = path.join([dname, fname])
        with open(fpath) as f:
            s = f.read()
        with open(fpath, "w") as f:
            f.write(re.sub('^#include "([^"]+)"',
                           '#include "rosserial/\\1"',
                           s, flags=re.MULTILINE))


