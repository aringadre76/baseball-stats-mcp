#!/usr/bin/env python3

import asyncio
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from server import BaseballStatsMCPServer
from test_config import TEST_CONFIG, TEST_CATEGORIES, TOOL_TEST_PARAMS

class ComprehensiveTestRunner:
    def __init__(self):
        self.server = BaseballStatsMCPServer()
        self.test_results = []
        self.passed = 0
        self.failed = 0
        self.total_tools = len(TEST_CONFIG["tools"])
        
    async def run_comprehensive_tests(self):
        print("Baseball Stats MCP Server - Comprehensive Test Runner")
        print("=" * 80)
        print(f"Testing all {self.total_tools} tools with comprehensive validation")
        print("Using Aaron Judge and Logan Webb as example players\n")
        
        # Test all categories
        for category, tools in TEST_CATEGORIES.items():
            await self.test_category(category, tools)
        
        # Print final results
        self.print_final_results()
        
        # Generate detailed report
        self.generate_detailed_report()
    
    async def test_category(self, category, tools):
        print(f"Testing {category.title()} Tools ({len(tools)} tools)")
        print("-" * 60)
        
        for tool_name in tools:
            await self.test_single_tool(tool_name)
        
        print()
    
    async def test_single_tool(self, tool_name):
        if tool_name not in TEST_CONFIG["tools"]:
            print(f"SKIPPED - {tool_name} - Not configured")
            return
        
        tool_config = TEST_CONFIG["tools"][tool_name]
        test_params = TOOL_TEST_PARAMS.get(tool_name, {})
        
        print(f"Testing: {tool_name}")
        print(f"Category: {tool_config['category']}")
        print(f"Description: {tool_config['description']}")
        print(f"Required Keywords: {', '.join(tool_config['required_keywords'])}")
        print(f"Min Match %: {tool_config['min_match_percentage']}%")
        
        try:
            # Get the method from the server
            method = getattr(self.server, tool_name)
            
            # Run the tool
            result = await method(test_params)
            
            # Validate the result
            validation_result = self.validate_tool_result(
                tool_name, result, tool_config
            )
            
            if validation_result["passed"]:
                print(f"PASSED - {tool_name}")
                print(f"Keyword Match: {validation_result['match_percentage']:.1f}%")
                print(f"Found: {', '.join(validation_result['found_keywords'])}")
                if validation_result['missing_keywords']:
                    print(f"Missing: {', '.join(validation_result['missing_keywords'])}")
                
                self.passed += 1
                self.test_results.append({
                    "tool": tool_name,
                    "category": tool_config['category'],
                    "status": "PASSED",
                    "match_percentage": validation_result['match_percentage'],
                    "found_keywords": validation_result['found_keywords'],
                    "missing_keywords": validation_result['missing_keywords'],
                    "description": tool_config['description']
                })
            else:
                print(f"FAILED - {tool_name}")
                print(f"Keyword Match: {validation_result['match_percentage']:.1f}%")
                print(f"Found: {', '.join(validation_result['found_keywords'])}")
                print(f"Missing: {', '.join(validation_result['missing_keywords'])}")
                print(f"Reason: {validation_result['failure_reason']}")
                
                self.failed += 1
                self.test_results.append({
                    "tool": tool_name,
                    "category": tool_config['category'],
                    "status": "FAILED",
                    "match_percentage": validation_result['match_percentage'],
                    "found_keywords": validation_result['found_keywords'],
                    "missing_keywords": validation_result['missing_keywords'],
                    "failure_reason": validation_result['failure_reason'],
                    "description": tool_config['description']
                })
                
        except Exception as e:
            print(f"ERROR - {tool_name} - Exception: {str(e)}")
            self.failed += 1
            self.test_results.append({
                "tool": tool_name,
                "category": tool_config['category'],
                "status": "ERROR",
                "error": str(e),
                "description": tool_config['description']
            })
        
        print()
    
    def validate_tool_result(self, tool_name, result, tool_config):
        """Validate tool result against expected keywords and requirements"""
        
        if not result or len(result) == 0:
            return {
                "passed": False,
                "match_percentage": 0.0,
                "found_keywords": [],
                "missing_keywords": tool_config['required_keywords'],
                "failure_reason": "Empty result"
            }
        
        # Extract text content
        text_content = ""
        for content in result:
            if hasattr(content, 'text') and content.text:
                text_content += content.text + " "
        
        if not text_content:
            return {
                "passed": False,
                "match_percentage": 0.0,
                "found_keywords": [],
                "missing_keywords": tool_config['required_keywords'],
                "failure_reason": "No text content"
            }
        
        # Check for expected keywords
        found_keywords = []
        missing_keywords = []
        
        for keyword in tool_config['required_keywords']:
            if keyword.lower() in text_content.lower():
                found_keywords.append(keyword)
            else:
                missing_keywords.append(keyword)
        
        # Calculate match percentage
        match_percentage = (len(found_keywords) / len(tool_config['required_keywords'])) * 100
        
        # Check if it meets minimum requirements
        passed = match_percentage >= tool_config['min_match_percentage']
        
        failure_reason = None
        if not passed:
            failure_reason = f"Insufficient keyword matches: {match_percentage:.1f}% < {tool_config['min_match_percentage']}%"
        
        return {
            "passed": passed,
            "match_percentage": match_percentage,
            "found_keywords": found_keywords,
            "missing_keywords": missing_keywords,
            "failure_reason": failure_reason
        }
    
    def print_final_results(self):
        print("=" * 80)
        print("COMPREHENSIVE TEST SUITE COMPLETED")
        print("=" * 80)
        print(f"Total Tools Tested: {self.total_tools}")
        print(f"PASSED: {self.passed}")
        print(f"FAILED: {self.failed}")
        print(f"Success Rate: {(self.passed / self.total_tools * 100):.1f}%")
        
        # Category breakdown
        print("\nResults by Category:")
        for category, tools in TEST_CATEGORIES.items():
            category_passed = sum(1 for r in self.test_results if r['category'] == category and r['status'] == 'PASSED')
            category_total = len(tools)
            category_rate = (category_passed / category_total * 100) if category_total > 0 else 0
            print(f"  {category.title()}: {category_passed}/{category_total} ({category_rate:.1f}%)")
        
        print("\n" + "=" * 80)
    
    def generate_detailed_report(self):
        """Generate a detailed test report"""
        print("\nDETAILED TEST REPORT")
        print("=" * 80)
        
        # Failed tests
        if self.failed > 0:
            print("\nFAILED TESTS:")
            for result in self.test_results:
                if result["status"] == "FAILED":
                    print(f"\n  Tool: {result['tool']}")
                    print(f"  Category: {result['category']}")
                    print(f"  Description: {result['description']}")
                    print(f"  Match %: {result.get('match_percentage', 'N/A')}%")
                    print(f"  Found Keywords: {', '.join(result.get('found_keywords', []))}")
                    print(f"  Missing Keywords: {', '.join(result.get('missing_keywords', []))}")
                    print(f"  Failure Reason: {result.get('failure_reason', 'Unknown')}")
        
        # Error tests
        error_tests = [r for r in self.test_results if r["status"] == "ERROR"]
        if error_tests:
            print("\nERROR TESTS:")
            for result in error_tests:
                print(f"\n  Tool: {result['tool']}")
                print(f"  Category: {result['category']}")
                print(f"  Description: {result['description']}")
                print(f"  Error: {result.get('error', 'Unknown')}")
        
        # Passed tests summary
        print("\nPASSED TESTS SUMMARY:")
        for category, tools in TEST_CATEGORIES.items():
            category_passed = [r for r in self.test_results if r['category'] == category and r['status'] == 'PASSED']
            if category_passed:
                print(f"\n  {category.title()}:")
                for result in category_passed:
                    match_pct = result.get('match_percentage', 0)
                    print(f"    {result['tool']}: {match_pct:.1f}% match")
        
        print("\n" + "=" * 80)

async def main():
    test_runner = ComprehensiveTestRunner()
    await test_runner.run_comprehensive_tests()

if __name__ == "__main__":
    asyncio.run(main())
