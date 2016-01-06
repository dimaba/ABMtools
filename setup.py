from setuptools import setup

setup(name='abmtools',
      version='0.1.1',
      description='Tools for Agent-Based Models',
      long_description='Removes a lot of the basic work you have to do for each model by providing a set of '
                       'standard classes and functions which can be adapted to suit your Agent-Based Model.',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.1',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering',
          'Topic :: Sociology',
      ],
      keywords='agent-based model simulation abm',
      url='http://github.com/dimaba/ABMtools',
      author='dimaba',
      author_email='dimaba14@gmail.com',
      license='MIT',
      packages=['abmtools'],
      zip_safe=True)