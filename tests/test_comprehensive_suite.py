#!/usr/bin/env python3

import asyncio
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from server import BaseballStatsMCPServer

class ComprehensiveTestSuite:
    def __init__(self):
        self.server = BaseballStatsMCPServer()
        self.test_results = []
        self.passed = 0
        self.failed = 0
        
    async def run_all_tests(self):
        print("🏟️  Baseball Stats MCP Server - Comprehensive Test Suite")
        print("=" * 80)
        print("Testing all 32 tools with Aaron Judge and Logan Webb as examples\n")
        
        # Test all pitching analysis tools (18 tools)
        await self.test_pitching_analysis_tools()
        
        # Test all batting analysis tools (7 tools)
        await self.test_batting_analysis_tools()
        
        # Test all defensive metrics tools (3 tools)
        await self.test_defensive_metrics_tools()
        
        # Test visualization tools (1 tool)
        await self.test_visualization_tools()
        
        # Test comparison tools (2 tools)
        await self.test_comparison_tools()
        
        # Test news and information tools (1 tool)
        await self.test_news_information_tools()
        
        # Print final results
        self.print_final_results()
    
    async def test_pitching_analysis_tools(self):
        print("🎯 Testing Pitching Analysis Tools (18 tools)")
        print("-" * 50)
        
        # Test 1: Basic pitcher stats
        await self.test_tool(
            "get_pitcher_basic_stats",
            self.server.get_pitcher_basic_stats,
            {"pitcher_name": "Logan Webb", "season": "2024"},
            "Basic pitching statistics for Logan Webb"
        )
        
        # Test 2: Pitch breakdown
        await self.test_tool(
            "get_pitch_breakdown",
            self.server.get_pitch_breakdown,
            {"pitcher_name": "Logan Webb", "season": "2024"},
            "Pitch breakdown for Logan Webb"
        )
        
        # Test 3: Pitch efficiency metrics
        await self.test_tool(
            "get_pitch_efficiency_metrics",
            self.server.get_pitch_efficiency_metrics,
            {"pitcher_name": "Logan Webb", "season": "2024"},
            "Pitch efficiency metrics for Logan Webb"
        )
        
        # Test 4: Pitch quality metrics
        await self.test_tool(
            "get_pitch_quality_metrics",
            self.server.get_pitch_quality_metrics,
            {"pitcher_name": "Logan Webb", "season": "2024"},
            "Pitch quality metrics for Logan Webb"
        )
        
        # Test 5: Pitch usage and tunneling
        await self.test_tool(
            "get_pitch_usage_tunneling",
            self.server.get_pitch_usage_tunneling,
            {"pitcher_name": "Logan Webb", "season": "2024"},
            "Pitch usage and tunneling for Logan Webb"
        )
        
        # Test 6: Pitch location and command
        await self.test_tool(
            "get_pitch_location_command",
            self.server.get_pitch_location_command,
            {"pitcher_name": "Logan Webb", "season": "2024"},
            "Pitch location and command for Logan Webb"
        )
        
        # Test 7: Specialized pitch analysis - Fastball
        await self.test_tool(
            "get_specialized_pitch_analysis (Fastball)",
            self.server.get_specialized_pitch_analysis,
            {"pitcher_name": "Logan Webb", "season": "2024", "pitch_type": "Fastball"},
            "Specialized fastball analysis for Logan Webb"
        )
        
        # Test 8: Specialized pitch analysis - Slider
        await self.test_tool(
            "get_specialized_pitch_analysis (Slider)",
            self.server.get_specialized_pitch_analysis,
            {"pitcher_name": "Logan Webb", "season": "2024", "pitch_type": "Slider"},
            "Specialized slider analysis for Logan Webb"
        )
        
        # Test 9: Specialized pitch analysis - Changeup
        await self.test_tool(
            "get_specialized_pitch_analysis (Changeup)",
            self.server.get_specialized_pitch_analysis,
            {"pitcher_name": "Logan Webb", "season": "2024", "pitch_type": "Changeup"},
            "Specialized changeup analysis for Logan Webb"
        )
        
        # Test 10: Run prevention metrics
        await self.test_tool(
            "get_run_prevention_metrics",
            self.server.get_run_prevention_metrics,
            {"pitcher_name": "Logan Webb", "season": "2024"},
            "Run prevention metrics for Logan Webb"
        )
        
        # Test 11: Contact quality metrics
        await self.test_tool(
            "get_contact_quality_metrics",
            self.server.get_contact_quality_metrics,
            {"pitcher_name": "Logan Webb", "season": "2024"},
            "Contact quality metrics for Logan Webb"
        )
        
        # Test 12: Win probability metrics
        await self.test_tool(
            "get_win_probability_metrics",
            self.server.get_win_probability_metrics,
            {"pitcher_name": "Logan Webb", "season": "2024"},
            "Win probability metrics for Logan Webb"
        )
        
        # Test 13: Plate discipline metrics
        await self.test_tool(
            "get_plate_discipline_metrics",
            self.server.get_plate_discipline_metrics,
            {"pitcher_name": "Logan Webb", "season": "2024"},
            "Plate discipline metrics for Logan Webb"
        )
        
        # Test 14: Spin aerodynamics metrics
        await self.test_tool(
            "get_spin_aerodynamics_metrics",
            self.server.get_spin_aerodynamics_metrics,
            {"pitcher_name": "Logan Webb", "season": "2024"},
            "Spin aerodynamics metrics for Logan Webb"
        )
        
        # Test 15: Biomechanics and release metrics
        await self.test_tool(
            "get_biomechanics_release_metrics",
            self.server.get_biomechanics_release_metrics,
            {"pitcher_name": "Logan Webb", "season": "2024"},
            "Biomechanics and release metrics for Logan Webb"
        )
        
        # Test 16: Advanced tunneling metrics
        await self.test_tool(
            "get_advanced_tunneling_metrics",
            self.server.get_advanced_tunneling_metrics,
            {"pitcher_name": "Logan Webb", "season": "2024"},
            "Advanced tunneling metrics for Logan Webb"
        )
        
        # Test 17: Deception and perceptual metrics
        await self.test_tool(
            "get_deception_perceptual_metrics",
            self.server.get_deception_perceptual_metrics,
            {"pitcher_name": "Logan Webb", "season": "2024"},
            "Deception and perceptual metrics for Logan Webb"
        )
        
        # Test 18: Pitch shape classification
        await self.test_tool(
            "get_pitch_shape_classification",
            self.server.get_pitch_shape_classification,
            {"pitcher_name": "Logan Webb", "season": "2024"},
            "Pitch shape classification for Logan Webb"
        )
        
        # Test 19: Contact quality by pitch
        await self.test_tool(
            "get_contact_quality_by_pitch",
            self.server.get_contact_quality_by_pitch,
            {"pitcher_name": "Logan Webb", "season": "2024"},
            "Contact quality by pitch for Logan Webb"
        )
        
        # Test 20: Biomechanics tech metrics
        await self.test_tool(
            "get_biomechanics_tech_metrics",
            self.server.get_biomechanics_tech_metrics,
            {"pitcher_name": "Logan Webb", "season": "2024"},
            "Biomechanics tech metrics for Logan Webb"
        )
        
        print()
    
    async def test_batting_analysis_tools(self):
        print("⚾ Testing Batting Analysis Tools (7 tools)")
        print("-" * 50)
        
        # Test 21: Basic batter stats
        await self.test_tool(
            "get_batter_basic_stats",
            self.server.get_batter_basic_stats,
            {"batter_name": "Aaron Judge", "season": "2024"},
            "Basic batting statistics for Aaron Judge"
        )
        
        # Test 22: Batter contact quality
        await self.test_tool(
            "get_batter_contact_quality",
            self.server.get_batter_contact_quality,
            {"batter_name": "Aaron Judge", "season": "2024"},
            "Contact quality metrics for Aaron Judge"
        )
        
        # Test 23: Batter plate discipline
        await self.test_tool(
            "get_batter_plate_discipline",
            self.server.get_batter_plate_discipline,
            {"batter_name": "Aaron Judge", "season": "2024"},
            "Plate discipline metrics for Aaron Judge"
        )
        
        # Test 24: Batter expected outcomes
        await self.test_tool(
            "get_batter_expected_outcomes",
            self.server.get_batter_expected_outcomes,
            {"batter_name": "Aaron Judge", "season": "2024"},
            "Expected outcomes for Aaron Judge"
        )
        
        # Test 25: Batter batted ball profile
        await self.test_tool(
            "get_batter_batted_ball_profile",
            self.server.get_batter_batted_ball_profile,
            {"batter_name": "Aaron Judge", "season": "2024"},
            "Batted ball profile for Aaron Judge"
        )
        
        # Test 26: Batter speed metrics
        await self.test_tool(
            "get_batter_speed_metrics",
            self.server.get_batter_speed_metrics,
            {"batter_name": "Aaron Judge", "season": "2024"},
            "Speed metrics for Aaron Judge"
        )
        
        # Test 27: Batter clutch performance
        await self.test_tool(
            "get_batter_clutch_performance",
            self.server.get_batter_clutch_performance,
            {"batter_name": "Aaron Judge", "season": "2024"},
            "Clutch performance for Aaron Judge"
        )
        
        print()
    
    async def test_defensive_metrics_tools(self):
        print("🥎 Testing Defensive Metrics Tools (3 tools)")
        print("-" * 50)
        
        # Test 28: Pitcher defensive metrics
        await self.test_tool(
            "get_pitcher_defensive_metrics",
            self.server.get_pitcher_defensive_metrics,
            {"pitcher_name": "Logan Webb", "season": "2024"},
            "Defensive metrics for Logan Webb"
        )
        
        # Test 29: Batter defensive metrics
        await self.test_tool(
            "get_batter_defensive_metrics",
            self.server.get_batter_defensive_metrics,
            {"batter_name": "Aaron Judge", "season": "2024"},
            "Defensive metrics for Aaron Judge"
        )
        
        # Test 30: Defensive comparison
        await self.test_tool(
            "get_defensive_comparison",
            self.server.get_defensive_comparison,
            {"player_names": ["Aaron Judge", "Logan Webb"], "season": "2024"},
            "Defensive comparison between Aaron Judge and Logan Webb"
        )
        
        print()
    
    async def test_visualization_tools(self):
        print("📊 Testing Visualization Tools (1 tool)")
        print("-" * 50)
        
        # Test 31: Generate pitch plot - Movement
        await self.test_tool(
            "generate_pitch_plot (Movement)",
            self.server.generate_pitch_plot,
            {"pitcher_name": "Logan Webb", "chart_type": "movement", "season": "2024"},
            "Movement chart for Logan Webb"
        )
        
        # Test 31b: Generate pitch plot - Velocity
        await self.test_tool(
            "generate_pitch_plot (Velocity)",
            self.server.generate_pitch_plot,
            {"pitcher_name": "Logan Webb", "chart_type": "velocity", "season": "2024"},
            "Velocity chart for Logan Webb"
        )
        
        # Test 31c: Generate pitch plot - Location
        await self.test_tool(
            "generate_pitch_plot (Location)",
            self.server.generate_pitch_plot,
            {"pitcher_name": "Logan Webb", "chart_type": "location", "season": "2024"},
            "Location chart for Logan Webb"
        )
        
        print()
    
    async def test_comparison_tools(self):
        print("🔍 Testing Comparison Tools (2 tools)")
        print("-" * 50)
        
        # Test 32: Pitcher comparison
        await self.test_tool(
            "get_pitcher_comparison",
            self.server.get_pitcher_comparison,
            {"pitcher_names": ["Logan Webb", "Aaron Judge"], "season": "2024"},
            "Comparison between Logan Webb and Aaron Judge"
        )
        
        # Test 33: Pitch sequence analysis
        await self.test_tool(
            "get_pitch_sequence_analysis",
            self.server.get_pitch_sequence_analysis,
            {"pitcher_name": "Logan Webb", "season": "2024"},
            "Pitch sequence analysis for Logan Webb"
        )
        
        print()
    
    async def test_news_information_tools(self):
        print("📰 Testing News and Information Tools (1 tool)")
        print("-" * 50)
        
        # Test 34: Scrape pitcher news
        await self.test_tool(
            "scrape_pitcher_news",
            self.server.scrape_pitcher_news,
            {"pitcher_name": "Logan Webb"},
            "Latest news about Logan Webb"
        )
        
        print()
    
    async def test_tool(self, tool_name, method, args, description):
        print(f"Testing: {tool_name}")
        print(f"Description: {description}")
        
        try:
            result = await method(args)
            
            if result and len(result) > 0:
                # Check if result contains text content
                has_content = False
                for content in result:
                    if hasattr(content, 'text') and content.text:
                        has_content = True
                        break
                
                if has_content:
                    print(f"✅ PASSED - {tool_name}")
                    self.passed += 1
                    self.test_results.append({
                        "tool": tool_name,
                        "status": "PASSED",
                        "description": description
                    })
                else:
                    print(f"❌ FAILED - {tool_name} - No content returned")
                    self.failed += 1
                    self.test_results.append({
                        "tool": tool_name,
                        "status": "FAILED",
                        "description": description,
                        "error": "No content returned"
                    })
            else:
                print(f"❌ FAILED - {tool_name} - Empty result")
                self.failed += 1
                self.test_results.append({
                    "tool": tool_name,
                    "status": "FAILED",
                    "description": description,
                    "error": "Empty result"
                })
                
        except Exception as e:
            print(f"❌ FAILED - {tool_name} - Error: {str(e)}")
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
        print("🏁 TEST SUITE COMPLETED")
        print("=" * 80)
        print(f"Total Tests: {self.passed + self.failed}")
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"Success Rate: {(self.passed / (self.passed + self.failed) * 100):.1f}%")
        
        if self.failed > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if result["status"] == "FAILED":
                    print(f"  - {result['tool']}: {result.get('error', 'Unknown error')}")
        
        print("\n✅ PASSED TESTS:")
        for result in self.test_results:
            if result["status"] == "PASSED":
                print(f"  - {result['tool']}")
        
        print("\n" + "=" * 80)

async def main():
    test_suite = ComprehensiveTestSuite()
    await test_suite.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())
