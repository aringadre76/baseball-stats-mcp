#!/usr/bin/env python3

# Test Configuration for Baseball Stats MCP Server
# This file defines test cases and validation criteria for all tools

TEST_CONFIG = {
    "pitchers": {
        "primary": "Logan Webb",
        "secondary": "Aaron Judge",  # Also a pitcher in some contexts
        "season": "2024"
    },
    "batters": {
        "primary": "Aaron Judge",
        "secondary": "Mike Trout",
        "season": "2024"
    },
    "tools": {
        # Pitching Analysis Tools (18 tools)
        "get_pitcher_basic_stats": {
            "category": "pitching",
            "required_keywords": ["ERA", "WHIP", "K/9", "BB/9", "IP", "W", "L"],
            "min_match_percentage": 85,
            "description": "Basic pitching statistics"
        },
        "get_pitch_breakdown": {
            "category": "pitching",
            "required_keywords": ["Fastball", "Slider", "Changeup", "velocity", "spin_rate"],
            "min_match_percentage": 80,
            "description": "Pitch breakdown and characteristics"
        },
        "get_pitch_efficiency_metrics": {
            "category": "pitching",
            "required_keywords": ["whiff_rate", "chase_rate", "barrel_pct", "CSW%"],
            "min_match_percentage": 75,
            "description": "Pitch efficiency metrics"
        },
        "get_pitch_quality_metrics": {
            "category": "pitching",
            "required_keywords": ["IVB", "HB", "spin_rate", "spin_efficiency"],
            "min_match_percentage": 75,
            "description": "Pitch quality and movement metrics"
        },
        "get_pitch_usage_tunneling": {
            "category": "pitching",
            "required_keywords": ["usage", "tunneling", "release", "deception"],
            "min_match_percentage": 75,
            "description": "Pitch usage and tunneling analysis"
        },
        "get_pitch_location_command": {
            "category": "pitching",
            "required_keywords": ["zone", "command", "location", "edge"],
            "min_match_percentage": 75,
            "description": "Pitch location and command metrics"
        },
        "get_specialized_pitch_analysis": {
            "category": "pitching",
            "required_keywords": ["analysis", "characteristics", "movement", "velocity"],
            "min_match_percentage": 75,
            "description": "Specialized pitch type analysis"
        },
        "get_run_prevention_metrics": {
            "category": "pitching",
            "required_keywords": ["ERA+", "FIP", "xFIP", "SIERA"],
            "min_match_percentage": 75,
            "description": "Run prevention metrics"
        },
        "get_contact_quality_metrics": {
            "category": "pitching",
            "required_keywords": ["HR/FB%", "GB%", "FB%", "Hard Hit%"],
            "min_match_percentage": 75,
            "description": "Contact quality metrics"
        },
        "get_win_probability_metrics": {
            "category": "pitching",
            "required_keywords": ["WAR", "WPA", "RE24", "leverage"],
            "min_match_percentage": 75,
            "description": "Win probability metrics"
        },
        "get_plate_discipline_metrics": {
            "category": "pitching",
            "required_keywords": ["O-Swing%", "Z-Swing%", "Contact%", "CSW%"],
            "min_match_percentage": 75,
            "description": "Plate discipline metrics"
        },
        "get_spin_aerodynamics_metrics": {
            "category": "pitching",
            "required_keywords": ["spin", "aerodynamics", "SSW", "movement"],
            "min_match_percentage": 75,
            "description": "Spin aerodynamics metrics"
        },
        "get_biomechanics_release_metrics": {
            "category": "pitching",
            "required_keywords": ["biomechanics", "release", "extension", "mechanics"],
            "min_match_percentage": 75,
            "description": "Biomechanics and release metrics"
        },
        "get_advanced_tunneling_metrics": {
            "category": "pitching",
            "required_keywords": ["tunneling", "deception", "release", "break"],
            "min_match_percentage": 75,
            "description": "Advanced tunneling metrics"
        },
        "get_deception_perceptual_metrics": {
            "category": "pitching",
            "required_keywords": ["deception", "perception", "velocity", "timing"],
            "min_match_percentage": 75,
            "description": "Deception and perceptual metrics"
        },
        "get_pitch_shape_classification": {
            "category": "pitching",
            "required_keywords": ["shape", "classification", "movement", "pattern"],
            "min_match_percentage": 75,
            "description": "Pitch shape classification"
        },
        "get_contact_quality_by_pitch": {
            "category": "pitching",
            "required_keywords": ["contact", "quality", "pitch", "launch"],
            "min_match_percentage": 75,
            "description": "Contact quality by pitch type"
        },
        "get_biomechanics_tech_metrics": {
            "category": "pitching",
            "required_keywords": ["biomechanics", "technology", "kinematics", "analysis"],
            "min_match_percentage": 75,
            "description": "Biomechanics tech metrics"
        },
        
        # Batting Analysis Tools (7 tools)
        "get_batter_basic_stats": {
            "category": "batting",
            "required_keywords": ["AVG", "OBP", "SLG", "OPS", "HR", "RBI", "BB", "SO"],
            "min_match_percentage": 85,
            "description": "Basic batting statistics"
        },
        "get_batter_contact_quality": {
            "category": "batting",
            "required_keywords": ["exit_velocity", "launch_angle", "barrel_pct", "hard_hit_pct"],
            "min_match_percentage": 75,
            "description": "Contact quality metrics"
        },
        "get_batter_plate_discipline": {
            "category": "batting",
            "required_keywords": ["O-Swing%", "Z-Swing%", "Contact%", "CSW%"],
            "min_match_percentage": 75,
            "description": "Plate discipline metrics"
        },
        "get_batter_expected_outcomes": {
            "category": "batting",
            "required_keywords": ["xBA", "xSLG", "xwOBA", "expected"],
            "min_match_percentage": 75,
            "description": "Expected outcome metrics"
        },
        "get_batter_batted_ball_profile": {
            "category": "batting",
            "required_keywords": ["GB%", "FB%", "LD%", "spray", "profile"],
            "min_match_percentage": 75,
            "description": "Batted ball profile"
        },
        "get_batter_speed_metrics": {
            "category": "batting",
            "required_keywords": ["sprint", "speed", "baserunning", "stolen"],
            "min_match_percentage": 75,
            "description": "Speed and baserunning metrics"
        },
        "get_batter_clutch_performance": {
            "category": "batting",
            "required_keywords": ["WPA", "clutch", "leverage", "RISP"],
            "min_match_percentage": 75,
            "description": "Clutch performance metrics"
        },
        
        # Defensive Metrics Tools (3 tools)
        "get_pitcher_defensive_metrics": {
            "category": "defensive",
            "required_keywords": ["fielding", "defense", "range", "DRS"],
            "min_match_percentage": 75,
            "description": "Pitcher defensive metrics"
        },
        "get_batter_defensive_metrics": {
            "category": "defensive",
            "required_keywords": ["fielding", "defense", "range", "UZR"],
            "min_match_percentage": 75,
            "description": "Batter defensive metrics"
        },
        "get_defensive_comparison": {
            "category": "defensive",
            "required_keywords": ["comparison", "defense", "fielding", "metrics"],
            "min_match_percentage": 75,
            "description": "Defensive comparison"
        },
        
        # Visualization Tools (1 tool)
        "generate_pitch_plot": {
            "category": "visualization",
            "required_keywords": ["plotly", "chart", "data", "visualization"],
            "min_match_percentage": 75,
            "description": "Pitch visualization charts"
        },
        
        # Comparison Tools (2 tools)
        "get_pitcher_comparison": {
            "category": "comparison",
            "required_keywords": ["comparison", "pitchers", "metrics", "analysis"],
            "min_match_percentage": 75,
            "description": "Pitcher comparison"
        },
        "get_pitch_sequence_analysis": {
            "category": "comparison",
            "required_keywords": ["sequence", "pitch", "analysis", "pattern"],
            "min_match_percentage": 75,
            "description": "Pitch sequence analysis"
        },
        
        # News and Information Tools (1 tool)
        "scrape_pitcher_news": {
            "category": "information",
            "required_keywords": ["news", "analysis", "information", "update"],
            "min_match_percentage": 75,
            "description": "Latest news and analysis"
        }
    }
}

# Test categories for organization
TEST_CATEGORIES = {
    "pitching": [
        "get_pitcher_basic_stats",
        "get_pitch_breakdown",
        "get_pitch_efficiency_metrics",
        "get_pitch_quality_metrics",
        "get_pitch_usage_tunneling",
        "get_pitch_location_command",
        "get_specialized_pitch_analysis",
        "get_run_prevention_metrics",
        "get_contact_quality_metrics",
        "get_win_probability_metrics",
        "get_plate_discipline_metrics",
        "get_spin_aerodynamics_metrics",
        "get_biomechanics_release_metrics",
        "get_advanced_tunneling_metrics",
        "get_deception_perceptual_metrics",
        "get_pitch_shape_classification",
        "get_contact_quality_by_pitch",
        "get_biomechanics_tech_metrics"
    ],
    "batting": [
        "get_batter_basic_stats",
        "get_batter_contact_quality",
        "get_batter_plate_discipline",
        "get_batter_expected_outcomes",
        "get_batter_batted_ball_profile",
        "get_batter_speed_metrics",
        "get_batter_clutch_performance"
    ],
    "defensive": [
        "get_pitcher_defensive_metrics",
        "get_batter_defensive_metrics",
        "get_defensive_comparison"
    ],
    "visualization": [
        "generate_pitch_plot"
    ],
    "comparison": [
        "get_pitcher_comparison",
        "get_pitch_sequence_analysis"
    ],
    "information": [
        "scrape_pitcher_news"
    ]
}

# Test parameters for each tool
TOOL_TEST_PARAMS = {
    "get_pitcher_basic_stats": {
        "pitcher_name": "Logan Webb",
        "season": "2024"
    },
    "get_pitch_breakdown": {
        "pitcher_name": "Logan Webb",
        "season": "2024"
    },
    "get_pitch_efficiency_metrics": {
        "pitcher_name": "Logan Webb",
        "season": "2024"
    },
    "get_pitch_quality_metrics": {
        "pitcher_name": "Logan Webb",
        "season": "2024"
    },
    "get_pitch_usage_tunneling": {
        "pitcher_name": "Logan Webb",
        "season": "2024"
    },
    "get_pitch_location_command": {
        "pitcher_name": "Logan Webb",
        "season": "2024"
    },
    "get_specialized_pitch_analysis": {
        "pitcher_name": "Logan Webb",
        "season": "2024",
        "pitch_type": "Fastball"
    },
    "get_run_prevention_metrics": {
        "pitcher_name": "Logan Webb",
        "season": "2024"
    },
    "get_contact_quality_metrics": {
        "pitcher_name": "Logan Webb",
        "season": "2024"
    },
    "get_win_probability_metrics": {
        "pitcher_name": "Logan Webb",
        "season": "2024"
    },
    "get_plate_discipline_metrics": {
        "pitcher_name": "Logan Webb",
        "season": "2024"
    },
    "get_spin_aerodynamics_metrics": {
        "pitcher_name": "Logan Webb",
        "season": "2024"
    },
    "get_biomechanics_release_metrics": {
        "pitcher_name": "Logan Webb",
        "season": "2024"
    },
    "get_advanced_tunneling_metrics": {
        "pitcher_name": "Logan Webb",
        "season": "2024"
    },
    "get_deception_perceptual_metrics": {
        "pitcher_name": "Logan Webb",
        "season": "2024"
    },
    "get_pitch_shape_classification": {
        "pitcher_name": "Logan Webb",
        "season": "2024"
    },
    "get_contact_quality_by_pitch": {
        "pitcher_name": "Logan Webb",
        "season": "2024"
    },
    "get_biomechanics_tech_metrics": {
        "pitcher_name": "Logan Webb",
        "season": "2024"
    },
    "get_batter_basic_stats": {
        "batter_name": "Aaron Judge",
        "season": "2024"
    },
    "get_batter_contact_quality": {
        "batter_name": "Aaron Judge",
        "season": "2024"
    },
    "get_batter_plate_discipline": {
        "batter_name": "Aaron Judge",
        "season": "2024"
    },
    "get_batter_expected_outcomes": {
        "batter_name": "Aaron Judge",
        "season": "2024"
    },
    "get_batter_batted_ball_profile": {
        "batter_name": "Aaron Judge",
        "season": "2024"
    },
    "get_batter_speed_metrics": {
        "batter_name": "Aaron Judge",
        "season": "2024"
    },
    "get_batter_clutch_performance": {
        "batter_name": "Aaron Judge",
        "season": "2024"
    },
    "get_pitcher_defensive_metrics": {
        "pitcher_name": "Logan Webb",
        "season": "2024"
    },
    "get_batter_defensive_metrics": {
        "batter_name": "Aaron Judge",
        "season": "2024"
    },
    "get_defensive_comparison": {
        "player_names": ["Aaron Judge", "Logan Webb"],
        "season": "2024"
    },
    "generate_pitch_plot": {
        "pitcher_name": "Logan Webb",
        "chart_type": "movement",
        "season": "2024"
    },
    "get_pitcher_comparison": {
        "pitcher_names": ["Logan Webb", "Aaron Judge"],
        "season": "2024"
    },
    "get_pitch_sequence_analysis": {
        "pitcher_name": "Logan Webb",
        "season": "2024"
    },
    "scrape_pitcher_news": {
        "pitcher_name": "Logan Webb"
    }
}
