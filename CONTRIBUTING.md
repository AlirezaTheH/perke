# Contributing to Perke
First off, thanks for taking the time to contribute!

The following is a set of guidelines for contributing to Perke. These are
mostly guidelines, not rules. Use your best judgment, and feel free to propose
changes to this document in a pull request.

**Table of Contents**:
- [Code of Conduct](#code-of-conduct)
- [Contribution Ways](#contribution-ways)
  - [Issues](#issues)
    - [Bug Reports](#bug-reports)
    - [Enhancement Suggestions](#enhancement-suggestions)
  - [Pull Requests](#pull-requests)
    - [Bug Fixes](#bug-fixes)
    - [Documentation Changes](#documentation-changes)
    - [Feature Changes](#feature-changes)
    - [Performance Improvements](#performance-improvements)
- [Guidelines](#guidelines)
  - [General](#general)
  - [Markdown](#markdown)
  - [reStructuredText](#restructuredtext)
  - [Git Commit Messages](#git-commit-messages)
  - [Python](#python)
- [Documentation](#documentation)
- [Testing](#testing)

## Code of Conduct
This project and everyone participating in it is governed by the
[Perke Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected
to uphold this code. Please report unacceptable behavior to
[alirezatheh@gmail.com](mailto:alirezatheh@gmail.com).

## Contribution Ways
### Issues
We use issues to keep track of
bugs and enhancements for Perke.

For all issues:
- Make sure you are using the latest version of Perke.

#### Bug Reports
This section guides you through submitting a bug report for Perke. Following
these guidelines helps maintainers, and the community understand your report,
reproduce the behavior, and find related reports.

##### Before Submitting A Bug Report
- Perform a cursory search in
  [issues](https://github.com/alirezatheh/perke/issues) to see if the problem
  has already been reported.
  - If it has, and the issue is still open, add a comment to the existing issue
    instead of opening a new one.
  - If you find a closed issue that seems like it is the same thing that you're
    experiencing, open a new issue and include a link to the original issue in
    the body of your new one.

##### Submitting A Bug Report
Create an issue and provide the following information by filling in
[the template](.github/ISSUE_TEMPLATE/bug_report.md):
- **Title**: Use a clear and descriptive title for the issue to identify the
  problem.
- **Current Behavior**: A clear and concise description of what happens instead
  of the expected behavior.
- **Expected Behavior**: A clear and concise description of what you expected
  to happen.
- **Steps to Reproduce**: Provide a minimal example that reproduces the bug.
- **Additional context**: Add any other context about the problem here.

#### Enhancement Suggestions
This section guides you through submitting an enhancement suggestion for Perke,
including completely new features and minor improvements to existing
functionality. Following these guidelines helps maintainers, and the community
understand your suggestion and find related suggestions.

##### Before Submitting An Enhancement Suggestion
- Perform a cursory search in
  [issues](https://github.com/alirezatheh/perke/issues) to see if the
  enhancement has already been suggested.  If it has, add a comment to the
  existing issue instead of opening a new one.

##### Submitting An Enhancement Suggestion
Create an issue and provide the following information by filling in
[the template](.github/ISSUE_TEMPLATE/feature_request.md):
- **Title**: Use a clear and descriptive title for the issue to identify the
  problem.
- **Summary**: One paragraph explanation of the feature.
- **Motivation**: Why are we doing this? What use cases does it support? What
  is the expected outcome?
- **Alternatives**: A clear and concise description of the alternative
  solutions you've considered. Be sure to explain why Perke's existing
  customizability isn't suitable for this feature.
- **Additional Context**: Add any other context about the feature request here.

### Pull Requests
Pull requests are the heart of collaboration on Perke. you can use pull
requests to fix bugs, change features or documentation or improve performance
of Perke.

The process described here has several goals:
- Maintain Perke's quality
- Fix problems that are important to users
- Engage the community in working toward the best possible Perke
- Enable a sustainable system for Perke's maintainers to review contributions

For all pull requests:
- Since the branch name will appear in the merge message, use a sensible name
  such as 'bug-fix-for-issue-1':
- Follow the [guidelines](#guidelines).
- If the pull request closes an issue, make sure that GitHub knows to
  automatically close the issue when the pull request is merged. For example,
  if the pull request closes issue number `1`, you could use the phrase
  `"Fix #1"` in the pull request description or commit message.
- Provide enough information. Any pull request that does not include enough
  information to be reviewed in a timely manner may be closed.
- After you submit your pull request, verify that all
  [status checks](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/about-status-checks)
  are passing.

#### Bug Fixes
This section guides you through fixing a bug for Perke.

##### Before Submitting A Bug Fix
- Make sure all tests are passing.

##### Submitting A Bug Fix
Create a pull request and provide the following information by filling in
[the template](.github/PULL_REQUEST_TEMPLATE/bug_fix.md):
- **Title**: Use a clear and descriptive title for the issue to identify the
  problem.
- **Identify the Bug**: Link to the issue describing the bug that you're fixing.
  - If there is not yet an issue for your bug, please open a new issue and then
    link to that issue in your pull request.
  > **Note**: In some cases, one person's "bug" is another person's "feature."
  > If the pull request does not address an existing issue with the "bug"
  > label, the maintainers have the final say on whether the current behavior
  > is a bug.
- **Description of the Change**: We must be able to understand your change from
  this description. If we can't get a good idea of what the code will be doing
  from the description here, the pull request may be closed.
- **Alternatives**: Explain what other alternates were considered and why the
  proposed version was selected.
- **Possible Drawbacks**: What are the possible side effects or negative
  impacts of the code change?
- **Release Notes**: Please describe the changes in a single line that explains
  this fix in terms that a user can understand. This text will be used
  in Perke's release notes.
  - If this change is not user-facing or notable enough to be included in
    release notes you may use the strings "Not applicable" or "N/A" here.

#### Documentation Changes
This section guides you through adding, changing or removing documentation
for Perke.

##### Submitting A Documentation Change
Create a pull request and provide the following information by filling in
[the template](.github/PULL_REQUEST_TEMPLATE/documentation_change.md):
- **Title**: Use a clear and descriptive title for the issue to identify the
  problem.
- **Description of the Change**: We must be able to understand the purpose of
  your change from this description. If we can't get a good idea of the
  benefits of the change from the description here, the pull request may be
  closed.
- **Release Notes**: Please describe the changes in a single line that explains
  this improvement in terms that a user can understand. This text will be used
  in Perke's release notes.
  - If this change is not user-facing or notable enough to be included in
    release notes you may use the strings "Not applicable" or "N/A" here.

#### Feature Changes
This section guides you through adding, changing or removing a feature for
Perke.

##### Submitting A Feature Change
Create a pull request and provide the following information by filling in
[the template](.github/PULL_REQUEST_TEMPLATE/feature_change.md):
- **Title**: Use a clear and descriptive title for the issue to identify the
  problem.
- **Identify the Enhancement**: Link to the issue that your change relates to.
  - If there is not yet an issue for your change, please open a new issue and
    then link to that issue in your pull request.
- **Description of the Change**: We must be able to understand your change from
  this description. If we can't get a good idea of what the code will be doing
  from the description here, the pull request may be closed.
- **Alternatives**: Explain what other alternates were considered and why the
  proposed version was selected.
- **Possible Drawbacks**: What are the possible side effects or negative
  impacts of the code change?
- **Release Notes**: Please describe the changes in a single line that explains
  this enhancement in terms that a user can understand. This text will be used
  in Perke's release notes. This text will be used
  in Perke's release notes.
  - If this change is not user-facing or notable enough to be included in
    release notes you may use the strings "Not applicable" or "N/A" here.

#### Performance Improvements
This section guides you through improving performance for Perke.

##### Submitting A Performance Improvement
Create a pull request and provide the following information by filling in
[the template](.github/PULL_REQUEST_TEMPLATE/performance_improvement.md):
- **Title**: Use a clear and descriptive title for the issue to identify the
  problem.
- **Description of the Change**: We must be able to understand your change from
  this description. If we can't get a good idea of what the code will be doing
  from the description here, the pull request may be closed.
- **Quantitative Performance Benefits**: Describe the exact performance
  improvement observed (for example, reduced time to complete an operation,
  reduced memory use, etc.). Describe how you measured this change. Bonus
  points for including graphs that demonstrate the improvement.
- **Possible Drawbacks**: What are the possible side effects or negative
  impacts of the code change?
- **Release Notes**: Please describe the changes in a single line that explains
  this improvement in terms that a user can understand. This text will be used
  in Perke's release notes. This text will be used
  in Perke's release notes.
  - If this change is not user-facing or notable enough to be included in
    release notes you may use the strings "Not applicable" or "N/A" here.

## Guidelines
The primary goal of the guidelines is to improve readability and thereby
the understanding, maintainability and general quality of the code. It
is impossible to cover every specific situation in a general guide so
programmer flexibility in interpreting the guidelines in the spirit in
which they were written is essential. Some of these guidelines can be validated
by Perke's pre-commit hooks.

To install hooks:
```bash
pip install -r requirements/develop.txt
pre-commit install
```

To run hooks manually:
```bash
pre-commit run --all-files
```

### General
- For maximum line length we use `88` as a hard limit and `79` as a soft limit.

### Markdown
- Titles should be capitalized.

### reStructuredText
- Titles should be capitalized.
- For indentation, we use tabs with size `4`.

### Git Commit Messages
- Use the present tense ("Add the feature" not "Added the feature")
- Use the imperative mood ("Move the model to..." not "Moves the models to...")

### Python
- All code should obey **The Zen of Python** principles according to
  [PEP 20](https://www.python.org/dev/peps/pep-0020/).
- Perke uses [Black](https://github.com/psf/black) code style with one
  exception: strings should be single quote except docstring.
- Since Python dropped support for version `2.x`, all code should have type
  hints according to [PEP 484](https://www.python.org/dev/peps/pep-0484/).
- Use the following import conventions:
  ```python
  # For following third parties import like below
  import numpy as np
  import scipy as sp
  import networkx as nx
  import hazm
  import nltk

  # For local imports use absolute path
  from perke.base.extractor import Extractor
  ```
- All codes should have tests. See [testing](#testing).
- All codes should be documented, to the same
  [standard](https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard)
  as NumPy and SciPy with following additions:
  - All public classes, methods and functions should have docstring.
  - All
    [Napoleon docstring sections](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html#docstring-sections)
    are supported.
  - Docstrings should begin with `"""` and terminate with `"""` on its own
    line.
  - For maximum line length we use `79` as hard limit and `72` as a soft limit.
  - The default reStructuredText role in docstrings is `:py:obj:`. Use a single
    backticks for all API names.
  - docstrings must not have any type hints, they'll be automatically extracted
    from objects' signature for documentation.
  - We use reStructuredText to mark up and give semantic meaning to text in
    docstrings. ReStructuredText is lightweight enough to read in raw form,
    such as command line terminal printouts, but is also parsed and rendered
    with Sphinx.

  See [documentation](#documentation).

### Changelog
Perke makes use of a changelog file that is based on
[Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
- For each notable change describe the changes in a single line that explains
  the change in terms that a user can understand.
- Use the past tense ("Added the feature" not "Add the feature").
- Make sure you add your line in a proper subsection, under the `Unreleased`
  section.


## Documentation
Perke makes use of Sphinx document generator, with documents located in the
[`docs`](docs) directory.

To install documentation requirements:
```bash
pip install -r requirements/documentaion.txt
```
To see documentation locally:
```bash
cd docs
make html
open _build/html/index.html
```

## Testing
Perke makes use of the pytest testing framework, with tests located in the
[`tests`](tests) directory.

To install test requirements:
```bash
pip install -r requirements/test.txt
```
To run all tests locally:
```bash
pytest
```
