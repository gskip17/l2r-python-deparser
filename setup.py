import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "l2r-python-deparser",
    version = "0.0.1",
    author = "Grant Skipper",
    author_email = "gskipper@iu.edu",
    description = ("Packet Sniffer and Parser for L2R - not just a pcap dissector :D"),
    license = "BSD",
    long_description=read('README.md'),
    include_package_data = True,
      install_requires=[
          "kaitaistruct",
          "scapy",
          "enum34"
      ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
