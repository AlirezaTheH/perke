# Changelog
All notable changes to this project will be documented in this file.

The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]

## [0.4.4] - 2023-06-25
### Added
- Added
  [`resources`](https://github.com/alirezatheh/perke/tree/main/perke/resources)'s
  README.md to distributed package for clearance.

## [0.4.3] - 2023-06-24
### Fixed
- Fixed a bug with
  [`resources`](https://github.com/alirezatheh/perke/tree/main/perke/resources)
  directory

## [0.4.2] - 2023-06-22
### Added
- Added support for Python `3.11`
- Brought Windows tests back

### Changed
- Adopted Perke with all changes in
  [Hazm](https://github.com/roshan-research/hazm) `0.9` release

## [0.4.1] - 2023-03-15
### Fixed
- Fixed a version issue on PyPI


## [0.4.0] - 2023-03-15
### Added
- Added support for Python `3.10`
- Added [Rich](https://github.com/Textualize/rich) integration to beatify CLI
  outputs
- Added [BumpVer](https://github.com/mbarkhau/bumpver) config
- Added publish workflow
- Added [Dependabot](https://docs.github.com/en/code-security/dependabot)
  config
- Added `CHANGELOG.md`

### Changed
- Changed code style to [Black](https://github.com/psf/black)
- Changed documentation theme to [Furo](https://github.com/pradyunsg/furo)
- Updated ReadtheDocs config to version `2`
- Revised documentation
- Changed CI from Travis CI to GitHub workflows

### Removed
- Removed Windows tests since [Hazm](https://github.com/roshan-research/hazm)
  runs on WSL and WSL tests is same as Linux

### Fixed
- Removed type hints from docstrings
- Added `MANIFEST.in` to include extras requirements in source builds
- Fixed an unicode decode error in Windows
- Avoided GitHub rate limit when running tests


## [0.3.5] - 2022-08-19
### Changed
- Improved CLI performance


## [0.3.4] - 2021-08-16
### Added
- First version of CLI added


[Unreleased]: https://github.com/alirezatheh/perke/compare/v0.4.4...HEAD
[0.4.4]: https://github.com/alirezatheh/perke/compare/v0.4.3...v0.4.4
[0.4.3]: https://github.com/alirezatheh/perke/compare/v0.4.2...v0.4.3
[0.4.2]: https://github.com/alirezatheh/perke/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/alirezatheh/perke/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/alirezatheh/perke/compare/v0.3.5...v0.4.0
[0.3.5]: https://github.com/alirezatheh/perke/compare/v0.3.4...v0.3.5
[0.3.4]: https://github.com/alirezatheh/perke/releases/tag/v0.3.4
