from __future__ import division, absolute_import, print_function, unicode_literals
import subprocess
import os 
import os.path
import sys

SIZES = {'square': ['-resize', '720x720', '-gravity', 'Center', '-crop', '720x720'],
         'large': ['-resize', '1800x1800'],
         'original': []}

def get_pre_params(mission):
    params = []
    if mission in ('SL2', 'SL3', 'SL4'):
        params += ['-fuzz', '20%', '-trim']
    params.append('-normalize')
    if mission in ('SL2', 'SL3', 'SL4'):
        params += ['-color-matrix', '1.12 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 1.0']
    return params

def get_convert_command(in_file, size, mission, out_file):
    params = get_pre_params(mission)
    params += SIZES[size]
    params += ['-unsharp', '0', '-quality', '90']
    return ["convert", in_file] + params + [out_file]

def get_output_path(path, mission, size):
    return os.path.join(path, mission, size.lower())

def process_file(input_file, output_path):
    mission, roll, frame = os.path.basename(input_file).rsplit('.', 1)[0].split('-')
    for size in SIZES.keys():
        path = get_output_path(output_path, mission, size)
        try:
            os.makedirs(path)
        except OSError:
            pass
        output_file = os.path.join(path, "%s-%s-%s.jpg" % (mission, roll, frame))
        cmd = get_convert_command(input_file, size, mission, output_file)
        ret = subprocess.call(cmd)
        if ret != 0:
            print("Failed!")
            sys.exit(ret)

if __name__ == '__main__':
    process_file(sys.argv[1], sys.argv[2])
