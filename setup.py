from setuptools import setup, find_packages


setup(
    name='graphkit',
    version='0.2',
    description="Process data based on JSON schema.",
    long_description="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ],
    keywords='schema jsonschema json data conversion graph rdf linkeddata',
    author='Friedrich Lindenberg',
    author_email='friedrich@pudo.org',
    url='http://github.com/pudo/graphkit',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'test']),
    namespace_packages=[],
    package_data={
        '': ['graphkit/schemas/*.yaml']
    },
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    install_requires=[
        'normality',
        'jsonschema',
        'jsongraph',
        'jsonmapping',
        'requests>=2.0',
        'unicodecsv',
        'pyyaml'
    ],
    tests_require=[
        'nose',
        'coverage',
        'wheel'
    ],
    entry_points={
        'graphkit.steps': [
            'csv:read = graphkit.pipe.csv:CSVRead',
            'csv:write = graphkit.pipe.csv:CSVWrite'
        ]
    }
)
