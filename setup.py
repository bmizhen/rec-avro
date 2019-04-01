from setuptools import find_packages, setup
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / 'README.md').read_text()

setup(
    name='rec-avro',
    version='0.0.3',
    description='Avro schema and data converters supporting storing arbitrary nested python data structures.',
    long_description=README,
    long_description_content_type='text/markdown',
    keywords = "avro json schema nested",
    url='https://github.com/bmizhen/rec-avro',
    author='Boris Mizhen',
    author_email='rec-avro@boriska.com',
    python_requires='>=3',
    license='MIT',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['fastavro', 'pytest']
)

