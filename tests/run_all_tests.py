#!/usr/bin/env python3

"""
Baseball Stats MCP Server - Test Runner
=======================================

This script runs all available test suites for the Baseball Stats MCP Server.

Available Test Suites:
1. Basic Functionality Tests - Tests if all tools run without errors
2. Data Validation Tests - Tests data quality and content validation
3. Comprehensive Tests - Full test suite with detailed reporting

Usage:
    python3 run_all_tests.py                    # Run all test suites
    python3 run_all_tests.py --basic           # Run only basic tests
    python3 run_all_tests.py --validation      # Run only validation tests
    python3 run_all_tests.py --comprehensive   # Run only comprehensive tests
"""

import asyncio
import sys
import os
import argparse
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

def print_header(title):
    print("\n" + "=" * 80)
    print(f" {title}")
    print("=" * 80)

def print_footer():
    print("\n" + "=" * 80)

async def run_basic_tests():
    """Run basic functionality tests"""
    print_header("BASIC FUNCTIONALITY TESTS")
    print("Testing if all tools run without errors...")
    
    try:
        from test_simple_suite import SimpleTestSuite
        test_suite = SimpleTestSuite()
        await test_suite.run_all_tests()
        return True
    except Exception as e:
        print(f"Error running basic tests: {e}")
        return False

async def run_validation_tests():
    """Run data validation tests"""
    print_header("DATA VALIDATION TESTS")
    print("Testing data quality and content validation...")
    
    try:
        from test_data_validation import DataValidationTestSuite
        test_suite = DataValidationTestSuite()
        await test_suite.run_data_validation_tests()
        return True
    except Exception as e:
        print(f"Error running validation tests: {e}")
        return False

async def run_comprehensive_tests():
    """Run comprehensive test suite"""
    print_header("COMPREHENSIVE TEST SUITE")
    print("Running full test suite with detailed reporting...")
    
    try:
        from test_comprehensive_runner import ComprehensiveTestRunner
        test_runner = ComprehensiveTestRunner()
        await test_runner.run_comprehensive_tests()
        return True
    except Exception as e:
        print(f"Error running comprehensive tests: {e}")
        return False

async def run_all_test_suites():
    """Run all test suites"""
    print_header("BASEBALL STATS MCP SERVER - COMPLETE TEST SUITE")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Testing all 32 tools with Aaron Judge and Logan Webb as examples")
    
    results = []
    
    # Run basic tests
    print("\n1. Running Basic Functionality Tests...")
    basic_success = await run_basic_tests()
    results.append(("Basic Functionality", basic_success))
    
    # Run validation tests
    print("\n2. Running Data Validation Tests...")
    validation_success = await run_validation_tests()
    results.append(("Data Validation", validation_success))
    
    # Run comprehensive tests
    print("\n3. Running Comprehensive Test Suite...")
    comprehensive_success = await run_comprehensive_tests()
    results.append(("Comprehensive", comprehensive_success))
    
    # Print summary
    print_header("TEST SUITE SUMMARY")
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    for test_name, success in results:
        status = "PASSED" if success else "FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(success for _, success in results)
    overall_status = "ALL TESTS PASSED" if all_passed else "SOME TESTS FAILED"
    print(f"\nOverall Status: {overall_status}")
    
    print_footer()
    
    return all_passed

def main():
    parser = argparse.ArgumentParser(description="Run Baseball Stats MCP Server tests")
    parser.add_argument("--basic", action="store_true", help="Run only basic tests")
    parser.add_argument("--validation", action="store_true", help="Run only validation tests")
    parser.add_argument("--comprehensive", action="store_true", help="Run only comprehensive tests")
    
    args = parser.parse_args()
    
    if args.basic:
        print("Running Basic Tests Only...")
        asyncio.run(run_basic_tests())
    elif args.validation:
        print("Running Validation Tests Only...")
        asyncio.run(run_validation_tests())
    elif args.comprehensive:
        print("Running Comprehensive Tests Only...")
        asyncio.run(run_comprehensive_tests())
    else:
        print("Running All Test Suites...")
        asyncio.run(run_all_test_suites())

if __name__ == "__main__":
    main()
