# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Added `raw()` function as the primary name for getting formatted text with ANSI escape sequences
- `raw_format()` is now an alias for `raw()` and will remain available for backward compatibility

### Changed

- Improved documentation for library integration use cases (using `raw()` with other libraries like tabulate)

## [3.0.0] - 2024-12-26

### Breaking Changes

- Removed `inputy` feature entirely - use standard `input()` with printy formatting if needed
- Minimum Python version is now 3.10 (dropped support for Python 3.5-3.9)

### Changed

- Migrated from setup.py to pyproject.toml for modern Python packaging
- Replaced Travis CI with GitHub Actions for CI/CD
- Added uv-based Makefile for development workflow
- Updated project infrastructure to modern standards
- Added project logo

### Removed

- Removed `inputy()` function
- Removed `InvalidInputType` exception
- Removed All Contributors configuration
- Removed Travis CI configuration

## [2.2.0] - 2021-02-28

### Added

- Added escape function
- Added background color

## [2.1.0] - 2020-06-13

### Added

- Added pretty printing objects
- Added objects str method correctly printed out
- Added max_digits restriction on inputy
- Added max_decimals restriction on inputy
- Added Dim compatibility again with flag 'D'

## [2.0.1] - 2020-05-01

### Fixed

- Fixed error on rendering default value for inputy's options 


## [2.0.0] - 2020-04-27

### Added

- Added high and low intensity flag colors
- Added list of options for inputy
- Added render_options on inputy
- Added default parameter on inputy

### Changed

- Changes options parameter on inputy
- Changed 'p' flag from Predefined color to Purple Color 

### Removed

- Removed 'D' flag (Dim), not widely supported


## [1.2.1] - 2020-02-14

### Fixed

- Fixed type 'bool' values

## [1.2.0] - 2020-01-13

### Added

- Added support for Windows, printy is now cross-platform

## [1.1.0] - 2020-01-13

### Added

- Added new function 'inputy'

## [1.0.0] - 2020-04-11

### Added

- First official release
