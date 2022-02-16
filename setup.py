from setuptools import setup, find_packages

setup(
    name="appsvc-code-profiler",
    version="1.0.0",
    description="Azure Linux App Service Code Profiler package",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        'click',
        'rich'
    ],
    entry_points={
        "console_scripts": [
            "code-profiler = appsvc_profiler:main"
        ]
    },
)