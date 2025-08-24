#!/usr/bin/env python3

import asyncio
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from server import BaseballStatsMCPServer

class DataValidationTestSuite:
    def __init__(self):
        self.server = BaseballStatsMCPServer()
        self.test_results = []
        self.passed = 0
        self.failed = 0
        
    async def run_data_validation_tests(self):
        print("Baseball Stats MCP Server - Data Validation Test Suite")
        print("=" * 80)
        print("Validating data quality and content for all tools\n")
        
        # Test core pitching tools with data validation
        await self.test_pitching_data_quality()
        
        # Test core batting tools with data validation
        await self.test_batting_data_quality()
        
        # Test visualization tools with data validation
        await self.test_visualization_data_quality()
        
        # Test comparison tools with data validation
        await self.test_comparison_data_quality()
        
        # Print final results
        self.print_final_results()
    
    async def test_pitching_data_quality(self):
        print("Testing Pitching Data Quality (Core Tools)")
        print("-" * 50)
        
        # Test 1: Basic pitcher stats - validate content
        await self.test_tool_data_quality(
            "get_pitcher_basic_stats",
            self.server.get_pitcher_basic_stats,
            {"pitcher_name": "Logan Webb", "season": "2024"},
            "Basic pitching statistics for Logan Webb",
            ["ERA", "WHIP", "K/9", "BB/9", "IP", "W", "L"]
        )
        
        # Test 2: Pitch breakdown - validate pitch types
        await self.test_tool_data_quality(
            "get_pitch_breakdown",
            self.server.get_pitch_breakdown,
            {"pitcher_name": "Logan Webb", "season": "2024"},
            "Pitch breakdown for Logan Webb",
            ["Fastball", "Slider", "Changeup", "velocity", "spin_rate"]
        )
        
        # Test 3: Pitch efficiency metrics - validate advanced stats
        await self.test_tool_data_quality(
            "get_pitch_efficiency_metrics",
            self.server.get_pitch_efficiency_metrics,
            {"pitcher_name": "Logan Webb", "season": "2024"},
            "Pitch efficiency metrics for Logan Webb",
            ["whiff_rate", "chase_rate", "barrel_pct", "CSW%"]
        )
        
        # Test 4: Pitch quality metrics - validate movement data
        await self.test_tool_data_quality(
            "get_pitch_quality_metrics",
            self.server.get_pitch_quality_metrics,
            {"pitcher_name": "Logan Webb", "season": "2024"},
            "Pitch quality metrics for Logan Webb",
            ["IVB", "HB", "spin_rate", "spin_efficiency"]
        )
        
        print()
    
    async def test_batting_data_quality(self):
        print("Testing Batting Data Quality (Core Tools)")
        print("-" * 50)
        
        # Test 1: Basic batter stats - validate content
        await self.test_tool_data_quality(
            "get_batter_basic_stats",
            self.server.get_batter_basic_stats,
            {"batter_name": "Aaron Judge", "season": "2024"},
            "Basic batting statistics for Aaron Judge",
            ["AVG", "OBP", "SLG", "OPS", "HR", "RBI", "BB", "SO"]
        )
        
        # Test 2: Batter contact quality - validate Statcast data
        await self.test_tool_data_quality(
            "get_batter_contact_quality",
            self.server.get_batter_contact_quality,
            {"batter_name": "Aaron Judge", "season": "2024"},
            "Contact quality metrics for Aaron Judge",
            ["exit_velocity", "launch_angle", "barrel_pct", "hard_hit_pct"]
        )
        
        # Test 3: Batter plate discipline - validate approach metrics
        await self.test_tool_data_quality(
            "get_batter_plate_discipline",
            self.server.get_batter_plate_discipline,
            {"batter_name": "Aaron Judge", "season": "2024"},
            "Plate discipline metrics for Aaron Judge",
            ["O-Swing%", "Z-Swing%", "Contact%", "CSW%"]
        )
        
        print()
    
    async def test_visualization_data_quality(self):
        print("Testing Visualization Data Quality")
        print("-" * 50)
        
        # Test 1: Movement chart - validate chart generation
        await self.test_tool_data_quality(
            "generate_pitch_plot (Movement)",
            self.server.generate_pitch_plot,
            {"pitcher_name": "Logan Webb", "chart_type": "movement", "season": "2024"},
            "Movement chart for Logan Webb",
            ["plotly", "chart", "movement", "data"]
        )
        
        # Test 2: Velocity chart - validate chart generation
        await self.test_tool_data_quality(
            "generate_pitch_plot (Velocity)",
            self.server.generate_pitch_plot,
            {"pitcher_name": "Logan Webb", "chart_type": "velocity", "season": "2024"},
            "Velocity chart for Logan Webb",
            ["plotly", "chart", "velocity", "data"]
        )
        
        print()
    
    async def test_comparison_data_quality(self):
        print("Testing Comparison Data Quality")
        print("-" * 50)
        
        # Test 1: Pitcher comparison - validate comparison data
        await self.test_tool_data_quality(
            "get_pitcher_comparison",
            self.server.get_pitcher_comparison,
            {"pitcher_names": ["Logan Webb", "Aaron Judge"], "season": "2024"},
            "Comparison between Logan Webb and Aaron Judge",
            ["comparison", "Logan Webb", "Aaron Judge", "metrics"]
        )
        
        print()
    
    async def test_tool_data_quality(self, tool_name, method, args, description, expected_keywords):
        print(f"Testing: {tool_name}")
        print(f"Description: {description}")
        print(f"Expected Keywords: {', '.join(expected_keywords)}")
        
        try:
            result = await method(args)
            
            if result and len(result) > 0:
                # Extract text content
                text_content = ""
                for content in result:
                    if hasattr(content, 'text') and content.text:
                        text_content += content.text + " "
                
                if text_content:
                    # Check for expected keywords
                    found_keywords = []
                    missing_keywords = []
                    
                    for keyword in expected_keywords:
                        if keyword.lower() in text_content.lower():
                            found_keywords.append(keyword)
                        else:
                            missing_keywords.append(keyword)
                    
                    # Calculate keyword match percentage
                    match_percentage = (len(found_keywords) / len(expected_keywords)) * 100
                    
                    if match_percentage >= 60:  # At least 60% of keywords must be found
                        print(f"PASSED - {tool_name}")
                        print(f"Keyword Match: {match_percentage:.1f}% ({len(found_keywords)}/{len(expected_keywords)})")
                        print(f"Found: {', '.join(found_keywords)}")
                        if missing_keywords:
                            print(f"Missing: {', '.join(missing_keywords)}")
                        
                        self.passed += 1
                        self.test_results.append({
                            "tool": tool_name,
                            "status": "PASSED",
                            "description": description,
                            "match_percentage": match_percentage,
                            "found_keywords": found_keywords,
                            "missing_keywords": missing_keywords
                        })
                    else:
                        print(f"FAILED - {tool_name} - Insufficient keyword matches")
                        print(f"Keyword Match: {match_percentage:.1f}% ({len(found_keywords)}/{len(expected_keywords)})")
                        print(f"Found: {', '.join(found_keywords)}")
                        print(f"Missing: {', '.join(missing_keywords)}")
                        
                        self.failed += 1
                        self.test_results.append({
                            "tool": tool_name,
                            "status": "FAILED",
                            "description": description,
                            "error": f"Insufficient keyword matches: {match_percentage:.1f}%",
                            "match_percentage": match_percentage,
                            "found_keywords": found_keywords,
                            "missing_keywords": missing_keywords
                        })
                else:
                    print(f"FAILED - {tool_name} - No text content returned")
                    self.failed += 1
                    self.test_results.append({
                        "tool": tool_name,
                        "status": "FAILED",
                        "description": description,
                        "error": "No text content returned"
                    })
            else:
                print(f"FAILED - {tool_name} - Empty result")
                self.failed += 1
                self.test_results.append({
                    "tool": tool_name,
                    "status": "FAILED",
                    "description": description,
                    "error": "Empty result"
                })
                
        except Exception as e:
            print(f"FAILED - {tool_name} - Error: {str(e)}")
            self.failed += 1
            self.test_results.append({
                "tool": tool_name,
                "status": "FAILED",
                "description": description,
                "error": str(e)
            })
        
        print()
    
    def print_final_results(self):
        print("=" * 80)
        print("DATA VALIDATION TEST SUITE COMPLETED")
        print("=" * 80)
        print(f"Total Tests: {self.passed + self.failed}")
        print(f"PASSED: {self.passed}")
        print(f"FAILED: {self.failed}")
        print(f"Success Rate: {(self.passed / (self.passed + self.failed) * 100):.1f}%")
        
        if self.failed > 0:
            print("\nFAILED TESTS:")
            for result in self.test_results:
                if result["status"] == "FAILED":
                    print(f"  - {result['tool']}: {result.get('error', 'Unknown error')}")
                    if 'match_percentage' in result:
                        print(f"    Keyword Match: {result['match_percentage']:.1f}%")
        
        print("\nPASSED TESTS:")
        for result in self.test_results:
            if result["status"] == "PASSED":
                print(f"  - {result['tool']}")
                if 'match_percentage' in result:
                    print(f"    Keyword Match: {result['match_percentage']:.1f}%")
        
        print("\n" + "=" * 80)

async def main():
    test_suite = DataValidationTestSuite()
    await test_suite.run_data_validation_tests()

if __name__ == "__main__":
    asyncio.run(main())
