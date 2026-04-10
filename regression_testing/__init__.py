"""
Regression Testing Package

This package contains comprehensive regression testing capabilities for GenAI systems,
including gold standard answer comparison, semantic similarity scoring, and quality gates.

Main components:
- regression_testing: Core regression testing framework
- demo_regression_testing: Interactive demo and tutorial
- config.json: Configurable testing thresholds and settings

Usage:
    python -m regression_testing.regression_testing
    or
    from regression_testing import RegressionTestFramework
"""

from .regression_testing import RegressionTestFramework, run_regression_tests, run_quick_regression

__version__ = "1.0.0"
__author__ = "GenAI Testing Tutorial"