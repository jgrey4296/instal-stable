from distutils.core import setup, Extension
import instal
# TODO: sort setup
setup(
    name='instal',
    version=instal.__version__,
    packages=['instal','instal.compiler', 'instal.domainparser', 'instal.factparser',
              'instal.firstprinciples', 'instal.models', 'instal.parser', 'instal.tracers',
              'instal.state'],
    package_data={"" : ["*.so"]},
    url='http://instsuite.github.io/',
    license='GPLv3',
    author='InstAL team @ Univesity of Bath',
    author_email='',
    description='InstAL: Institutional Action Language Framework and Tools',
)
