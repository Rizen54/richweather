import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = []
for line in open('requirements.txt').readlines():
    req = line.strip()
    if req.startswith('#') or req == '':
        continue
    requirements.append(req)
    
setuptools.setup(
    name="richweather",
    version="0.1.0",
    author="Laryy The Cow",
    author_email="larry@gentoo.org",
    description="A Python-based command-line application that provides real-time weather information.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Rizen54/richweather/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
    entry_points={
        'console_scripts': [
            'richweather=richweather.richweather:main',
        ],
    },
    install_requires=requirements,
)
 
