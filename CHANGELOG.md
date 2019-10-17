# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic
Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Upgrade terraform syntax to 0.12
- Upgrade to Richie 1.11.0

### Fixed

- Load main css from the instart static namespace
- Sass build copy now targets the appropriate path in the production image
- Fix CKeditor static files to work with a CDN

### Security

- Upgrade npm dependencies from vulnerable to safe versions (`lodash`,
  `lodash.mergewith`, `mixin-deep`, `set-value`).

[unreleased]: https://github.com/openfun/instart-learning/master
