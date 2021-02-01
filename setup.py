from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import os
import numpy
from distutils import sysconfig
#import numpy.distutils.intelccompiler
import numpy.distutils.ccompiler
import platform as plt
import sys
import pathlib
import subprocess

def pkgconfig(package, kw):
    flag_map = {'-I': 'include_dirs', '-L': 'library_dirs', '-l': 'libraries'}
    exitcode, output = subprocess.getstatusoutput(
        'pkg-config --cflags --libs {}'.format(package))
    if exitcode == 0:
        for token in output.strip().split():
            kw.setdefault(flag_map.get(token[:2]), []).append(token[2:])
        return kw
    else:
        print(output)

os.system('rm pyMilne.*.so pyMilne.*.cpp')
p = pathlib.Path(sys.executable)
root_dir = str(pathlib.Path(*p.parts[0:-2]))


if(plt.system() == 'Darwin'):
    #root_dir = '/opt/local/'
    CC = 'clang'
    CXX= 'clang++'
    link_opts = ["-stdlib=libc++","-bundle","-undefined","dynamic_lookup", "-fopenmp"]
else:
    #root_dir = '/usr/'
    CC = 'gcc'
    CXX= 'g++'
    link_opts = ["-shared", "-fopenmp"]

os.environ["CC"] = CC
os.environ["CXX"] = CXX

from distutils import sysconfig
sysconfig.get_config_vars()['CFLAGS'] = ''
sysconfig.get_config_vars()['OPT'] = ''
sysconfig.get_config_vars()['PY_CFLAGS'] = ''
sysconfig.get_config_vars()['PY_CORE_CFLAGS'] = ''
sysconfig.get_config_vars()['CC'] =  CC
sysconfig.get_config_vars()['CXX'] = CXX
sysconfig.get_config_vars()['BASECFLAGS'] = ''
sysconfig.get_config_vars()['CCSHARED'] = ''
sysconfig.get_config_vars()['LDSHARED'] = CC
sysconfig.get_config_vars()['CPP'] = CXX
sysconfig.get_config_vars()['CPPFLAGS'] = ''
sysconfig.get_config_vars()['BLDSHARED'] = ''
sysconfig.get_config_vars()['CONFIGURE_LDFLAGS'] = ''
sysconfig.get_config_vars()['LDFLAGS'] = ''
sysconfig.get_config_vars()['PY_LDFLAGS'] = ''



comp_flags=['-Ofast','-std=c++14','-march=native','-fPIC','-fopenmp', '-I./src', '-DNDEBUG']


pymilne_src = ["pyMilne.pyx"]
pymilne_inc = ["./",numpy.get_include()]

extension_kwargs = {
    'sources': pymilne_src,
    'include_dirs': pymilne_inc,
}


extension_kwargs = pkgconfig('eigen3', extension_kwargs)
extension_kwargs = pkgconfig('fftw3', extension_kwargs)

extension = Extension("pyMilne",
                      language="c++",
                      extra_compile_args=comp_flags,
                      extra_link_args=link_opts,
                      **extension_kwargs)

extension.cython_directives = {'language_level': "3"}

setup(
    name = 'pyMilne',
    version = '1.0',
    author = 'J. de la Cruz Rodriguez (ISP-SU 2020)',
    ext_modules=[extension],
    cmdclass = {'build_ext': build_ext}
)

