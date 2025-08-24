#!/usr/bin/env python3

import asyncio
import json
from server import BaseballStatsMCPServer

async def test_server():
    server = BaseballStatsMCPServer()
    
    print("Testing Baseball Stats MCP Server...\n")
    
    test_cases = [
        {
            "name": "Basic Pitcher Stats",
            "method": server.get_pitcher_basic_stats,
            "args": {"pitcher_name": "Jacob deGrom", "season": "2024"}
        },
        {
            "name": "Pitch Breakdown",
            "method": server.get_pitch_breakdown,
            "args": {"pitcher_name": "Gerrit Cole", "season": "2024"}
        },
        {
            "name": "Efficiency Metrics",
            "method": server.get_pitch_efficiency_metrics,
            "args": {"pitcher_name": "Shohei Ohtani", "season": "2024"}
        },
        {
            "name": "Pitch Quality Metrics",
            "method": server.get_pitch_quality_metrics,
            "args": {"pitcher_name": "Max Scherzer", "season": "2024"}
        },
        {
            "name": "Pitch Usage & Tunneling",
            "method": server.get_pitch_usage_tunneling,
            "args": {"pitcher_name": "Clayton Kershaw", "season": "2024"}
        },
        {
            "name": "Pitch Location & Command",
            "method": server.get_pitch_location_command,
            "args": {"pitcher_name": "Jacob deGrom", "season": "2024"}
        },
        {
            "name": "Specialized Fastball Analysis",
            "method": server.get_specialized_pitch_analysis,
            "args": {"pitcher_name": "Gerrit Cole", "season": "2024", "pitch_type": "Fastball"}
        },
        {
            "name": "Specialized Slider Analysis",
            "method": server.get_specialized_pitch_analysis,
            "args": {"pitcher_name": "Max Scherzer", "season": "2024", "pitch_type": "Slider"}
        },
        {
            "name": "Run Prevention Metrics",
            "method": server.get_run_prevention_metrics,
            "args": {"pitcher_name": "Jacob deGrom", "season": "2024"}
        },
        {
            "name": "Contact Quality Metrics",
            "method": server.get_contact_quality_metrics,
            "args": {"pitcher_name": "Gerrit Cole", "season": "2024"}
        },
        {
            "name": "Win Probability Metrics",
            "method": server.get_win_probability_metrics,
            "args": {"pitcher_name": "Max Scherzer", "season": "2024"}
        },
        {
            "name": "Plate Discipline Metrics",
            "method": server.get_plate_discipline_metrics,
            "args": {"pitcher_name": "Clayton Kershaw", "season": "2024"}
        },
        {
            "name": "Pitch Sequence Analysis",
            "method": server.get_pitch_sequence_analysis,
            "args": {"pitcher_name": "Clayton Kershaw", "season": "2024"}
        },
        {
            "name": "Pitcher Comparison",
            "method": server.get_pitcher_comparison,
            "args": {
                "pitcher_names": ["Jacob deGrom", "Gerrit Cole", "Max Scherzer"],
                "season": "2024",
                "metrics": ["whiff_rate", "chase_rate", "barrel_pct"]
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"=== Testing: {test_case['name']} ===")
        try:
            result = await test_case["method"](test_case["args"])
            for content in result:
                if hasattr(content, 'text'):
                    print(content.text[:500] + "..." if len(content.text) > 500 else content.text)
                else:
                    print(f"Content: {content}")
            print("\n" + "="*50 + "\n")
        except Exception as e:
            print(f"Error testing {test_case['name']}: {e}\n")
    
    print("Server testing completed!")

if __name__ == "__main__":
    asyncio.run(test_server())
