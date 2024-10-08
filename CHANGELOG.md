# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0] - 2024-08-30

- Install requires fastapi >= 0.103.1

## [1.2.0] - 2023-12-11

## Changed

- Internal updates to support newer FastAPI and Pydantic 2.0. FastAPI-Tableau is
  pinned to FastAPI 0.103.1.

## [1.1.2] - 2023-07-11

### Fixed

- FastAPI-Tableau now requires FastAPI <= 0.88.0 to avoid compatibility issues.

## [1.1.1] - 2022-02-23

### Changed

- Changed warning message upon HTTPS failure, with new directions for
  self-signed certificate use.

## [1.1.0] - 2021-11-03

### Added

- This changelog.
- Support for using Pydantic schemas in endpoints that receive input from
  Tableau.
- Added support for verbose debug logging when the environment variable
  `FASTAPITABLEAU_LOG_LEVEL` is set to `DEBUG`.

### Fixed

- Package metadata incorrectly said that the license was "Proprietary", but the
  license is actually MIT.

## [1.0.0] - 2021-09-29

### Added

- The initial release, with support for calling modified FastAPI applications
  from Tableau workbooks.

[Unreleased]: https://github.com/rstudio/fastapitableau/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/rstudio/fastapitableau/compare/v1.1.2...v1.2.0
[1.1.2]: https://github.com/rstudio/fastapitableau/compare/v1.1.1...v1.1.2
[1.1.1]: https://github.com/rstudio/fastapitableau/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/rstudio/fastapitableau/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/rstudio/fastapitableau/releases/tag/v1.0.0
