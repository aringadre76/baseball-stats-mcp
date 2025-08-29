#!/usr/bin/env python3

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import sys

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel,
    ServerCapabilities,
    ToolsCapability
)

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseballStatsMCPServer:
    def __init__(self):
        self.server = Server("baseball-stats-mcp")
        self.firecrawl_token = os.getenv("FIRECRAWL_TOKEN", "")
        self.baseball_api_key = os.getenv("BASEBALL_API_KEY", "")
        
        self.setup_server()
    
    def setup_server(self):
        print(f"Setting up MCP server with tools...", file=sys.stderr)
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            tools = [
                Tool(
                    name="get_pitcher_basic_stats",
                    description="Get basic pitching statistics for a specific pitcher",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pitcher_name": {"type": "string", "description": "Full name of the pitcher"},
                            "season": {"type": "string", "description": "Season year (e.g., '2024')"}
                        },
                        "required": ["pitcher_name"]
                    }
                ),
                Tool(
                    name="get_pitch_breakdown",
                    description="Get detailed breakdown of pitch types, velocities, and movement including spin rate, spin axis, IVB, HB, and movement vs. average",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pitcher_name": {"type": "string", "description": "Full name of the pitcher"},
                            "season": {"type": "string", "description": "Season year (e.g., '2024')"},
                            "pitch_type": {"type": "string", "description": "Specific pitch type to analyze (optional)"}
                        },
                        "required": ["pitcher_name"]
                    }
                ),
                Tool(
                    name="get_pitch_efficiency_metrics",
                    description="Get advanced efficiency metrics including whiff rate, chase rate, barrel percentage, CSW%, putaway%, xBA, xSLG, xwOBA, and run value",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pitcher_name": {"type": "string", "description": "Full name of the pitcher"},
                            "season": {"type": "string", "description": "Season year (e.g., '2024')"},
                            "metric_type": {"type": "string", "description": "Type of efficiency metric to focus on"}
                        },
                        "required": ["pitcher_name"]
                    }
                ),
                Tool(
                    name="generate_pitch_plot",
                    description="Generate advanced pitch visualization charts including movement, velocity, and location",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pitcher_name": {"type": "string", "description": "Full name of the pitcher"},
                            "season": {"type": "string", "description": "Season year (e.g., '2024')"},
                            "chart_type": {"type": "string", "description": "Type of chart: 'movement', 'velocity', 'location', 'heatmap'"},
                            "pitch_type": {"type": "string", "description": "Specific pitch type to visualize (optional)"}
                        },
                        "required": ["pitcher_name", "chart_type"]
                    }
                ),
                Tool(
                    name="get_pitcher_comparison",
                    description="Compare multiple pitchers across various advanced metrics",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pitcher_names": {"type": "array", "items": {"type": "string"}, "description": "List of pitcher names to compare"},
                            "season": {"type": "string", "description": "Season year (e.g., '2024')"},
                            "metrics": {"type": "array", "items": {"type": "string"}, "description": "Metrics to compare (e.g., ['whiff_rate', 'chase_rate', 'barrel_pct'])"}
                        },
                        "required": ["pitcher_names"]
                    }
                ),
                Tool(
                    name="get_pitch_sequence_analysis",
                    description="Analyze pitch sequencing patterns and effectiveness",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pitcher_name": {"type": "string", "description": "Full name of the pitcher"},
                            "season": {"type": "string", "description": "Season year (e.g., '2024')"},
                            "count_situation": {"type": "string", "description": "Specific count situation to analyze (optional)"}
                        },
                        "required": ["pitcher_name"]
                    }
                ),
                Tool(
                    name="get_pitch_quality_metrics",
                    description="Get comprehensive pitch quality metrics including spin rate, spin axis, spin efficiency, IVB, HB, and movement vs. average",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pitcher_name": {"type": "string", "description": "Full name of the pitcher"},
                            "season": {"type": "string", "description": "Season year (e.g., '2024')"},
                            "pitch_type": {"type": "string", "description": "Specific pitch type to analyze (optional)"}
                        },
                        "required": ["pitcher_name"]
                    }
                ),
                Tool(
                    name="get_pitch_usage_tunneling",
                    description="Get pitch usage percentages, release point consistency, and tunneling metrics for different pitch types",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pitcher_name": {"type": "string", "description": "Full name of the pitcher"},
                            "season": {"type": "string", "description": "Season year (e.g., '2024')"},
                            "pitch_type": {"type": "string", "description": "Specific pitch type to analyze (optional)"}
                        },
                        "required": ["pitcher_name"]
                    }
                ),
                Tool(
                    name="get_pitch_location_command",
                    description="Get pitch location and command metrics including edge%, zone%, meatball%, and called strike%",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pitcher_name": {"type": "string", "description": "Full name of the pitcher"},
                            "season": {"type": "string", "description": "Season year (e.g., '2024')"},
                            "pitch_type": {"type": "string", "description": "Specific pitch type to analyze (optional)"}
                        },
                        "required": ["pitcher_name"]
                    }
                ),
                Tool(
                    name="get_specialized_pitch_analysis",
                    description="Get specialized analysis for specific pitch types including fastball ride, breaking ball sweep, changeup velocity differential, and sinker characteristics",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pitcher_name": {"type": "string", "description": "Full name of the pitcher"},
                            "season": {"type": "string", "description": "Season year (e.g., '2024')"},
                            "pitch_type": {"type": "string", "description": "Specific pitch type to analyze (e.g., 'Fastball', 'Slider', 'Changeup', 'Sinker')"}
                        },
                        "required": ["pitcher_name", "pitch_type"]
                    }
                ),
                Tool(
                    name="get_run_prevention_metrics",
                    description="Get comprehensive run prevention metrics including ERA+, FIP, xFIP, SIERA, and other ERA alternatives",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pitcher_name": {"type": "string", "description": "Full name of the pitcher"},
                            "season": {"type": "string", "description": "Season year (e.g., '2024')"}
                        },
                        "required": ["pitcher_name"]
                    }
                ),
                Tool(
                    name="get_contact_quality_metrics",
                    description="Get detailed contact quality and batted ball metrics including HR/FB%, GB%/FB%/LD%, Hard Hit%, Barrel%, and expected outcomes",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pitcher_name": {"type": "string", "description": "Full name of the pitcher"},
                            "season": {"type": "string", "description": "Season year (e.g., '2024')"}
                        },
                        "required": ["pitcher_name"]
                    }
                ),
                Tool(
                    name="get_win_probability_metrics",
                    description="Get win probability and value metrics including WAR, WPA, RE24, and leverage statistics",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pitcher_name": {"type": "string", "description": "Full name of the pitcher"},
                            "season": {"type": "string", "description": "Season year (e.g., '2024')"}
                        },
                        "required": ["pitcher_name"]
                    }
                ),
                Tool(
                    name="get_plate_discipline_metrics",
                    description="Get comprehensive plate discipline metrics including O-Swing%, Z-Swing%, SwStr%, CSW%, Contact%, and First Pitch Strike%",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pitcher_name": {"type": "string", "description": "Full name of the pitcher"},
                            "season": {"type": "string", "description": "Season year (e.g., '2024')"}
                        },
                        "required": ["pitcher_name"]
                    }
                ),
                Tool(
                    name="get_spin_aerodynamics_metrics",
                    description="Get advanced spin and aerodynamics metrics including Seam-Shifted Wake (SSW), True Spin Axis vs. Observed Movement, and Magnus vs. Non-Magnus movement",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pitcher_name": {"type": "string", "description": "Full name of the pitcher"},
                            "season": {"type": "string", "description": "Season year (e.g., '2024')"},
                            "pitch_type": {"type": "string", "description": "Specific pitch type to analyze (optional)"}
                        },
                        "required": ["pitcher_name"]
                    }
                ),
                Tool(
                    name="get_biomechanics_release_metrics",
                    description="Get comprehensive biomechanics and release characteristics including extension, release points, and delivery mechanics",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pitcher_name": {"type": "string", "description": "Full name of the pitcher"},
                            "season": {"type": "string", "description": "Season year (e.g., '2024')"}
                        },
                        "required": ["pitcher_name"]
                    }
                ),
                Tool(
                    name="get_advanced_tunneling_metrics",
                    description="Get advanced pitch tunneling metrics including release distance, tunnel point, tunnel differential, and break tunneling ratio",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pitcher_name": {"type": "string", "description": "Full name of the pitcher"},
                            "season": {"type": "string", "description": "Season year (e.g., '2024')"},
                            "pitch_comparison": {"type": "string", "description": "Pitch types to compare for tunneling (e.g., 'Fastball-Slider')"}
                        },
                        "required": ["pitcher_name"]
                    }
                ),
                Tool(
                    name="get_deception_perceptual_metrics",
                    description="Get deception and perceptual metrics including effective velocity, perceived velocity, and time to plate analysis",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pitcher_name": {"type": "string", "description": "Full name of the pitcher"},
                            "season": {"type": "string", "description": "Season year (e.g., '2024')"}
                        },
                        "required": ["pitcher_name"]
                    }
                ),
                Tool(
                    name="get_pitch_shape_classification",
                    description="Get advanced pitch shape classification including movement clusters, axis tilt, and Stuff+ modeling",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pitcher_name": {"type": "string", "description": "Full name of the pitcher"},
                            "season": {"type": "string", "description": "Season year (e.g., '2024')"},
                            "pitch_type": {"type": "string", "description": "Specific pitch type to analyze (optional)"}
                        },
                        "required": ["pitcher_name"]
                    }
                ),
                Tool(
                    name="get_contact_quality_by_pitch",
                    description="Get detailed contact quality analysis by specific pitch types including launch angle patterns and bat speed matchups",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pitcher_name": {"type": "string", "description": "Full name of the pitcher"},
                            "season": {"type": "string", "description": "Season year (e.g., '2024')"},
                            "pitch_type": {"type": "string", "description": "Specific pitch type to analyze (optional)"}
                        },
                        "required": ["pitcher_name"]
                    }
                ),
                Tool(
                    name="get_biomechanics_tech_metrics",
                    description="Get cutting-edge biomechanics and technology metrics including Hawkeye data, kinematic sequencing, and grip analysis",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pitcher_name": {"type": "string", "description": "Full name of the pitcher"},
                            "season": {"type": "string", "description": "Season year (e.g., '2024')"}
                        },
                        "required": ["pitcher_name"]
                    }
                ),
                Tool(
                    name="scrape_pitcher_news",
                    description="Scrape latest news and analysis about a specific pitcher using Firecrawl",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pitcher_name": {"type": "string", "description": "Full name of the pitcher"},
                            "news_sources": {"type": "array", "items": {"type": "string"}, "description": "News sources to search (e.g., ['mlb.com', 'fangraphs.com'])"}
                        },
                        "required": ["pitcher_name"]
                    }
                ),
                Tool(
                    name="get_batter_basic_stats",
                    description="Get basic batting statistics for a specific batter including traditional and advanced metrics",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "batter_name": {"type": "string", "description": "Full name of the batter"},
                            "season": {"type": "string", "description": "Season year (e.g., '2024')"}
                        },
                        "required": ["batter_name"]
                    }
                ),
                Tool(
                    name="get_batter_contact_quality",
                    description="Get comprehensive contact quality metrics including Statcast Core data, launch angle, exit velocity, and expected outcomes",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "batter_name": {"type": "string", "description": "Full name of the batter"},
                            "season": {"type": "string", "description": "Season year (e.g., '2024')"},
                            "metric_type": {"type": "string", "description": "Type of contact quality metric to focus on"}
                        },
                        "required": ["batter_name"]
                    }
                ),
                Tool(
                    name="get_batter_plate_discipline",
                    description="Get comprehensive plate discipline metrics including O-Swing%, Z-Swing%, SwStr%, CSW%, and contact rates",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "batter_name": {"type": "string", "description": "Full name of the batter"},
                            "season": {"type": "string", "description": "Season year (e.g., '2024')"}
                        },
                        "required": ["batter_name"]
                    }
                ),
                Tool(
                    name="get_batter_expected_outcomes",
                    description="Get expected outcome metrics including xBA, xSLG, xwOBA, and run value data",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "batter_name": {"type": "string", "description": "Full name of the batter"},
                            "season": {"type": "string", "description": "Season year (e.g., '2024')"}
                        },
                        "required": ["batter_name"]
                    }
                ),
                Tool(
                    name="get_batter_batted_ball_profile",
                    description="Get detailed batted ball profile including GB%, FB%, LD%, Pull%, Center%, Oppo%, and spray chart data",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "batter_name": {"type": "string", "description": "Full name of the batter"},
                            "season": {"type": "string", "description": "Season year (e.g., '2024')"}
                        },
                        "required": ["batter_name"]
                    }
                ),
                Tool(
                    name="get_batter_speed_metrics",
                    description="Get baserunning and speed metrics including sprint speed, stolen base success rate, and baserunning value",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "batter_name": {"type": "string", "description": "Full name of the batter"},
                            "season": {"type": "string", "description": "Season year (e.g., '2024')"}
                        },
                        "required": ["batter_name"]
                    }
                ),
                Tool(
                    name="get_batter_clutch_performance",
                    description="Get clutch performance metrics including WPA, RE24, and performance in high-leverage situations",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "batter_name": {"type": "string", "description": "Full name of the batter"},
                            "season": {"type": "string", "description": "Season year (e.g., '2024')"}
                        },
                        "required": ["batter_name"]
                    }
                ),
                Tool(
                    name="get_pitcher_defensive_metrics",
                    description="Get comprehensive defensive metrics for pitchers including fielding percentage, range factor, and defensive runs saved",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pitcher_name": {"type": "string", "description": "Full name of the pitcher"},
                            "season": {"type": "string", "description": "Season year (e.g., '2024')"}
                        },
                        "required": ["pitcher_name"]
                    }
                ),
                Tool(
                    name="get_batter_defensive_metrics",
                    description="Get comprehensive defensive metrics for batters including fielding percentage, range factor, defensive runs saved, and position-specific metrics",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "batter_name": {"type": "string", "description": "Full name of the batter"},
                            "season": {"type": "string", "description": "Season year (e.g., '2024')"},
                            "position": {"type": "string", "description": "Specific defensive position to analyze (optional)"}
                        },
                        "required": ["batter_name"]
                    }
                ),
                Tool(
                    name="get_defensive_comparison",
                    description="Compare defensive metrics between multiple players or positions",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "player_names": {"type": "array", "items": {"type": "string"}, "description": "List of player names to compare"},
                            "season": {"type": "string", "description": "Season year (e.g., '2024')"},
                            "position": {"type": "string", "description": "Specific defensive position to compare (optional)"}
                        },
                        "required": ["player_names"]
                    }
                )
            ]
            return tools
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            try:
                if name == "get_pitcher_basic_stats":
                    return await self.get_pitcher_basic_stats(arguments)
                elif name == "get_pitch_breakdown":
                    return await self.get_pitch_breakdown(arguments)
                elif name == "get_pitch_efficiency_metrics":
                    return await self.get_pitch_efficiency_metrics(arguments)
                elif name == "generate_pitch_plot":
                    return await self.generate_pitch_plot(arguments)
                elif name == "get_pitcher_comparison":
                    return await self.get_pitcher_comparison(arguments)
                elif name == "get_pitch_sequence_analysis":
                    return await self.get_pitch_sequence_analysis(arguments)
                elif name == "get_pitch_quality_metrics":
                    return await self.get_pitch_quality_metrics(arguments)
                elif name == "get_pitch_usage_tunneling":
                    return await self.get_pitch_usage_tunneling(arguments)
                elif name == "get_pitch_location_command":
                    return await self.get_pitch_location_command(arguments)
                elif name == "get_specialized_pitch_analysis":
                    return await self.get_specialized_pitch_analysis(arguments)
                elif name == "get_run_prevention_metrics":
                    return await self.get_run_prevention_metrics(arguments)
                elif name == "get_contact_quality_metrics":
                    return await self.get_contact_quality_metrics(arguments)
                elif name == "get_win_probability_metrics":
                    return await self.get_win_probability_metrics(arguments)
                elif name == "get_plate_discipline_metrics":
                    return await self.get_plate_discipline_metrics(arguments)
                elif name == "get_spin_aerodynamics_metrics":
                    return await self.get_spin_aerodynamics_metrics(arguments)
                elif name == "get_biomechanics_release_metrics":
                    return await self.get_biomechanics_release_metrics(arguments)
                elif name == "get_advanced_tunneling_metrics":
                    return await self.get_advanced_tunneling_metrics(arguments)
                elif name == "get_deception_perceptual_metrics":
                    return await self.get_deception_perceptual_metrics(arguments)
                elif name == "get_pitch_shape_classification":
                    return await self.get_pitch_shape_classification(arguments)
                elif name == "get_contact_quality_by_pitch":
                    return await self.get_contact_quality_by_pitch(arguments)
                elif name == "get_biomechanics_tech_metrics":
                    return await self.get_biomechanics_tech_metrics(arguments)
                elif name == "scrape_pitcher_news":
                    return await self.scrape_pitcher_news(arguments)
                elif name == "get_batter_basic_stats":
                    return await self.get_batter_basic_stats(arguments)
                elif name == "get_batter_contact_quality":
                    return await self.get_batter_contact_quality(arguments)
                elif name == "get_batter_plate_discipline":
                    return await self.get_batter_plate_discipline(arguments)
                elif name == "get_batter_expected_outcomes":
                    return await self.get_batter_expected_outcomes(arguments)
                elif name == "get_batter_batted_ball_profile":
                    return await self.get_batter_batted_ball_profile(arguments)
                elif name == "get_batter_speed_metrics":
                    return await self.get_batter_speed_metrics(arguments)
                elif name == "get_batter_clutch_performance":
                    return await self.get_batter_clutch_performance(arguments)
                elif name == "get_pitcher_defensive_metrics":
                    return await self.get_pitcher_defensive_metrics(arguments)
                elif name == "get_batter_defensive_metrics":
                    return await self.get_batter_defensive_metrics(arguments)
                elif name == "get_defensive_comparison":
                    return await self.get_defensive_comparison(arguments)
                else:
                    return [TextContent(type="text", text=f"Unknown tool: {name}")]
            except Exception as e:
                logger.error(f"Error in tool {name}: {str(e)}")
                return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    async def get_pitcher_basic_stats(self, arguments: Dict[str, Any]) -> List[TextContent]:
        pitcher_name = arguments.get("pitcher_name")
        season = arguments.get("season", "2024")
        
        stats = await self._fetch_pitcher_stats(pitcher_name, season)
        
        if not stats:
            return [TextContent(type="text", text=f"No stats found for {pitcher_name} in {season}")]
        
        summary = f"""
**{pitcher_name} - {season} Season Basic Stats**

**Traditional Stats:**
- W-L: {stats.get('wins', 'N/A')}-{stats.get('losses', 'N/A')}
- ERA: {stats.get('era', 'N/A')}
- IP: {stats.get('innings_pitched', 'N/A')}
- SO: {stats.get('strikeouts', 'N/A')}
- BB: {stats.get('walks', 'N/A')}
- WHIP: {stats.get('whip', 'N/A')}

**Advanced Metrics:**
- K/9: {stats.get('k_per_9', 'N/A')}
- BB/9: {stats.get('bb_per_9', 'N/A')}
- HR/9: {stats.get('hr_per_9', 'N/A')}
- FIP: {stats.get('fip', 'N/A')}
- xFIP: {stats.get('xfip', 'N/A')}
- BABIP: {stats.get('babip', 'N/A')}

**Strikeout & Walk Rates:**
- K%: {stats.get('k_percent', 'N/A')}%
- BB%: {stats.get('bb_percent', 'N/A')}%
- K-BB%: {stats.get('k_bb_percent', 'N/A')}%
"""
        
        return [TextContent(type="text", text=summary)]
    
    async def get_pitch_breakdown(self, arguments: Dict[str, Any]) -> List[TextContent]:
        pitcher_name = arguments.get("pitcher_name")
        season = arguments.get("season", "2024")
        pitch_type = arguments.get("pitch_type")
        
        pitch_data = await self._fetch_pitch_data(pitcher_name, season)
        
        if not pitch_data:
            return [TextContent(type="text", text=f"No pitch data found for {pitcher_name} in {season}")]
        
        if pitch_type:
            pitch_data = [p for p in pitch_data if p.get('pitch_type') == pitch_type]
        
        pitch_summary = f"""
**{pitcher_name} - {season} Pitch Breakdown**

**Pitch Types and Usage:**
"""
        
        pitch_types = {}
        for pitch in pitch_data:
            p_type = pitch.get('pitch_type', 'Unknown')
            if p_type not in pitch_types:
                pitch_types[p_type] = {
                    'count': 0,
                    'avg_velocity': [],
                    'avg_movement': [],
                    'avg_spin_rate': [],
                    'avg_spin_efficiency': [],
                    'avg_ivb': [],
                    'avg_hb': [],
                    'avg_movement_vs_avg': []
                }
            
            pitch_types[p_type]['count'] += 1
            if pitch.get('velocity'):
                pitch_types[p_type]['avg_velocity'].append(pitch['velocity'])
            if pitch.get('movement'):
                pitch_types[p_type]['avg_movement'].append(pitch['movement'])
            if pitch.get('spin_rate'):
                pitch_types[p_type]['avg_spin_rate'].append(pitch['spin_rate'])
            if pitch.get('spin_efficiency'):
                pitch_types[p_type]['avg_spin_efficiency'].append(pitch['spin_efficiency'])
            if pitch.get('ivb'):
                pitch_types[p_type]['avg_ivb'].append(pitch['ivb'])
            if pitch.get('hb'):
                pitch_types[p_type]['avg_hb'].append(pitch['hb'])
            if pitch.get('movement_vs_avg'):
                pitch_types[p_type]['avg_movement_vs_avg'].append(pitch['movement_vs_avg'])
        
        for p_type, data in pitch_types.items():
            avg_vel = np.mean(data['avg_velocity']) if data['avg_velocity'] else 'N/A'
            avg_mov = np.mean(data['avg_movement']) if data['avg_movement'] else 'N/A'
            avg_spin = np.mean(data['avg_spin_rate']) if data['avg_spin_rate'] else 'N/A'
            avg_spin_eff = np.mean(data['avg_spin_efficiency']) if data['avg_spin_efficiency'] else 'N/A'
            avg_ivb = np.mean(data['avg_ivb']) if data['avg_ivb'] else 'N/A'
            avg_hb = np.mean(data['avg_hb']) if data['avg_hb'] else 'N/A'
            avg_mov_vs_avg = np.mean(data['avg_movement_vs_avg']) if data['avg_movement_vs_avg'] else 'N/A'
            usage_pct = (data['count'] / len(pitch_data)) * 100
            
            pitch_summary += f"""
**{p_type}:**
- Usage: {usage_pct:.1f}% ({data['count']} pitches)
- Avg Velocity: {avg_vel:.1f} mph
- Avg Movement: {avg_mov:.1f} inches
- Avg Spin Rate: {avg_spin:.0f} rpm
- Avg Spin Efficiency: {avg_spin_eff:.1f}%
- Avg IVB: {avg_ivb:.1f} inches
- Avg HB: {avg_hb:.1f} inches
- Movement vs Avg: {avg_mov_vs_avg:.1f} inches
"""
        
        return [TextContent(type="text", text=pitch_summary)]
    
    async def get_pitch_efficiency_metrics(self, arguments: Dict[str, Any]) -> List[TextContent]:
        pitcher_name = arguments.get("pitcher_name")
        season = arguments.get("season", "2024")
        metric_type = arguments.get("metric_type", "all")
        
        efficiency_data = await self._fetch_efficiency_metrics(pitcher_name, season)
        
        if not efficiency_data:
            return [TextContent(type="text", text=f"No efficiency data found for {pitcher_name} in {season}")]
        
        summary = f"""
**{pitcher_name} - {season} Efficiency Metrics**

**Contact Quality:**
- Whiff Rate: {efficiency_data.get('whiff_rate', 'N/A')}%
- Chase Rate: {efficiency_data.get('chase_rate', 'N/A')}%
- Barrel Percentage: {efficiency_data.get('barrel_pct', 'N/A')}%
- Hard Hit Rate: {efficiency_data.get('hard_hit_rate', 'N/A')}%

**Pitch Effectiveness:**
- Zone Rate: {efficiency_data.get('zone_rate', 'N/A')}%
- First Pitch Strike Rate: {efficiency_data.get('first_pitch_strike_rate', 'N/A')}%
- Swinging Strike Rate: {efficiency_data.get('swinging_strike_rate', 'N/A')}%
- Called Strike Rate: {efficiency_data.get('called_strike_rate', 'N/A')}%

**Advanced Metrics:**
- CSW% (Called Strike + Whiff): {efficiency_data.get('csw_pct', 'N/A')}%
- O-Swing% (Chase Rate): {efficiency_data.get('o_swing_pct', 'N/A')}%
- Z-Swing% (Zone Swing Rate): {efficiency_data.get('z_swing_pct', 'N/A')}%
- O-Contact% (Out of Zone Contact): {efficiency_data.get('o_contact_pct', 'N/A')}%
- Z-Contact% (Zone Contact): {efficiency_data.get('z_contact_pct', 'N/A')}%

**Statcast Outcomes:**
- Whiff% per pitch: {efficiency_data.get('whiff_per_pitch', 'N/A')}%
- CSW% per pitch: {efficiency_data.get('csw_per_pitch', 'N/A')}%
- Putaway%: {efficiency_data.get('putaway_pct', 'N/A')}%
- xBA vs pitch: {efficiency_data.get('xba_vs_pitch', 'N/A')}
- xSLG vs pitch: {efficiency_data.get('xslg_vs_pitch', 'N/A')}
- xwOBA vs pitch: {efficiency_data.get('xwoba_vs_pitch', 'N/A')}
- Run Value (RV): {efficiency_data.get('run_value', 'N/A')}
- RV/100 pitches: {efficiency_data.get('rv_per_100', 'N/A')}
"""
        
        return [TextContent(type="text", text=summary)]
    
    async def generate_pitch_plot(self, arguments: Dict[str, Any]) -> List[TextContent]:
        pitcher_name = arguments.get("pitcher_name")
        season = arguments.get("season", "2024")
        chart_type = arguments.get("chart_type")
        pitch_type = arguments.get("pitch_type")
        
        pitch_data = await self._fetch_pitch_data(pitcher_name, season)
        
        if not pitch_data:
            return [TextContent(type="text", text=f"No pitch data found for {pitcher_name} in {season}")]
        
        if pitch_type:
            pitch_data = [p for p in pitch_data if p.get('pitch_type') == pitch_type]
        
        if chart_type == "movement":
            chart = self._create_movement_chart(pitch_data, pitcher_name, season)
        elif chart_type == "velocity":
            chart = self._create_velocity_chart(pitch_data, pitcher_name, season)
        elif chart_type == "location":
            chart = self._create_location_chart(pitch_data, pitcher_name, season)
        elif chart_type == "heatmap":
            chart = self._create_heatmap_chart(pitch_data, pitcher_name, season)
        else:
            return [TextContent(type="text", text=f"Unknown chart type: {chart_type}")]
        
        chart_html = chart.to_html(include_plotlyjs=True, full_html=True)
        
        return [
            TextContent(type="text", text=f"Generated {chart_type} chart for {pitcher_name}"),
            TextContent(type="text", text=chart_html)
        ]
    
    async def get_pitcher_comparison(self, arguments: Dict[str, Any]) -> List[TextContent]:
        pitcher_names = arguments.get("pitcher_names", [])
        season = arguments.get("season", "2024")
        metrics = arguments.get("metrics", ["whiff_rate", "chase_rate", "barrel_pct"])
        
        if len(pitcher_names) < 2:
            return [TextContent(type="text", text="Please provide at least 2 pitchers to compare")]
        
        comparison_data = []
        for pitcher in pitcher_names:
            data = await self._fetch_efficiency_metrics(pitcher, season)
            if data:
                comparison_data.append({"name": pitcher, "data": data})
        
        if len(comparison_data) < 2:
            return [TextContent(type="text", text="Insufficient data for comparison")]
        
        comparison_text = f"**Pitcher Comparison - {season} Season**\n\n"
        
        for metric in metrics:
            comparison_text += f"**{metric.replace('_', ' ').title()}:**\n"
            for pitcher_data in comparison_data:
                value = pitcher_data["data"].get(metric, "N/A")
                comparison_text += f"- {pitcher_data['name']}: {value}\n"
            comparison_text += "\n"
        
        return [TextContent(type="text", text=comparison_text)]
    
    async def get_pitch_sequence_analysis(self, arguments: Dict[str, Any]) -> List[TextContent]:
        pitcher_name = arguments.get("pitcher_name")
        season = arguments.get("season", "2024")
        count_situation = arguments.get("count_situation")
        
        sequence_data = await self._fetch_sequence_data(pitcher_name, season)
        
        if not sequence_data:
            return [TextContent(type="text", text=f"No sequence data found for {pitcher_name} in {season}")]
        
        summary = f"""
**{pitcher_name} - {season} Pitch Sequence Analysis**

**Overall Sequencing Patterns:**
- Most Common First Pitch: {sequence_data.get('most_common_first_pitch', 'N/A')}
- First Pitch Strike Rate: {sequence_data.get('first_pitch_strike_rate', 'N/A')}%
- Two-Strike Approach: {sequence_data.get('two_strike_approach', 'N/A')}

**Count-Specific Tendencies:**
"""
        
        count_tendencies = sequence_data.get('count_tendencies', {})
        for count, tendency in count_tendencies.items():
            summary += f"- {count}: {tendency}\n"
        
        return [TextContent(type="text", text=summary)]
    
    async def scrape_pitcher_news(self, arguments: Dict[str, Any]) -> List[TextContent]:
        pitcher_name = arguments.get("pitcher_name")
        news_sources = arguments.get("news_sources", ["mlb.com", "fangraphs.com", "baseball-reference.com"])
        
        news_summary = f"**Latest News for {pitcher_name}**\n\n"
        
        for source in news_sources:
            try:
                search_query = f"{pitcher_name} pitcher news analysis"
                news_data = await self._scrape_news(source, search_query)
                if news_data:
                    news_summary += f"**{source}:**\n{news_data[:500]}...\n\n"
            except Exception as e:
                news_summary += f"**{source}:** Error retrieving news - {str(e)}\n\n"
        
        return [TextContent(type="text", text=news_summary)]
    
    async def get_pitch_quality_metrics(self, arguments: Dict[str, Any]) -> List[TextContent]:
        pitcher_name = arguments.get("pitcher_name")
        season = arguments.get("season", "2024")
        pitch_type = arguments.get("pitch_type")
        
        quality_data = await self._fetch_pitch_quality_data(pitcher_name, season)
        
        if not quality_data:
            return [TextContent(type="text", text=f"No quality data found for {pitcher_name} in {season}")]
        
        if pitch_type:
            quality_data = [q for q in quality_data if q.get('pitch_type') == pitch_type]
        
        summary = f"""
**{pitcher_name} - {season} Pitch Quality Metrics**

**Pitch Quality & Movement:**
"""
        
        pitch_types = {}
        for pitch in quality_data:
            p_type = pitch.get('pitch_type', 'Unknown')
            if p_type not in pitch_types:
                pitch_types[p_type] = {
                    'count': 0,
                    'avg_velocity': [],
                    'avg_spin_rate': [],
                    'avg_spin_axis': [],
                    'avg_spin_efficiency': [],
                    'avg_ivb': [],
                    'avg_hb': [],
                    'avg_movement_vs_avg': []
                }
            
            pitch_types[p_type]['count'] += 1
            if pitch.get('velocity'):
                pitch_types[p_type]['avg_velocity'].append(pitch['velocity'])
            if pitch.get('spin_rate'):
                pitch_types[p_type]['avg_spin_rate'].append(pitch['spin_rate'])
            if pitch.get('spin_axis'):
                pitch_types[p_type]['avg_spin_axis'].append(pitch['spin_axis'])
            if pitch.get('spin_efficiency'):
                pitch_types[p_type]['avg_spin_efficiency'].append(pitch['spin_efficiency'])
            if pitch.get('ivb'):
                pitch_types[p_type]['avg_ivb'].append(pitch['ivb'])
            if pitch.get('hb'):
                pitch_types[p_type]['avg_hb'].append(pitch['hb'])
            if pitch.get('movement_vs_avg'):
                pitch_types[p_type]['avg_movement_vs_avg'].append(pitch['movement_vs_avg'])
        
        for p_type, data in pitch_types.items():
            avg_vel = np.mean(data['avg_velocity']) if data['avg_velocity'] else 'N/A'
            avg_spin = np.mean(data['avg_spin_rate']) if data['avg_spin_rate'] else 'N/A'
            avg_axis = np.mean(data['avg_spin_axis']) if data['avg_spin_axis'] else 'N/A'
            avg_eff = np.mean(data['avg_spin_efficiency']) if data['avg_spin_efficiency'] else 'N/A'
            avg_ivb = np.mean(data['avg_ivb']) if data['avg_ivb'] else 'N/A'
            avg_hb = np.mean(data['avg_hb']) if data['avg_hb'] else 'N/A'
            avg_mov_vs_avg = np.mean(data['avg_movement_vs_avg']) if data['avg_movement_vs_avg'] else 'N/A'
            
            summary += f"""
**{p_type}:**
- Avg Velocity: {avg_vel:.1f} mph
- Avg Spin Rate: {avg_spin:.0f} rpm
- Avg Spin Axis: {avg_axis:.1f}° (clock face)
- Avg Spin Efficiency: {avg_eff:.1f}%
- Avg IVB: {avg_ivb:.1f} inches
- Avg HB: {avg_hb:.1f} inches
- Movement vs Avg: {avg_mov_vs_avg:.1f} inches
"""
        
        return [TextContent(type="text", text=summary)]
    
    async def get_pitch_usage_tunneling(self, arguments: Dict[str, Any]) -> List[TextContent]:
        pitcher_name = arguments.get("pitcher_name")
        season = arguments.get("season", "2024")
        pitch_type = arguments.get("pitch_type")
        
        usage_data = await self._fetch_usage_tunneling_data(pitcher_name, season)
        
        if not usage_data:
            return [TextContent(type="text", text=f"No usage data found for {pitcher_name} in {season}")]
        
        if pitch_type:
            usage_data = [u for u in usage_data if u.get('pitch_type') == pitch_type]
        
        summary = f"""
**{pitcher_name} - {season} Pitch Usage & Tunneling**

**Pitch Usage & Tunneling:**
"""
        
        pitch_types = {}
        for pitch in usage_data:
            p_type = pitch.get('pitch_type', 'Unknown')
            if p_type not in pitch_types:
                pitch_types[p_type] = {
                    'count': 0,
                    'usage_pct': 0,
                    'release_point_x': [],
                    'release_point_z': [],
                    'tunneling_distance': [],
                    'tunneling_time': []
                }
            
            pitch_types[p_type]['count'] += 1
            pitch_types[p_type]['usage_pct'] = pitch.get('usage_pct', 0)
            if pitch.get('release_point_x'):
                pitch_types[p_type]['release_point_x'].append(pitch['release_point_x'])
            if pitch.get('release_point_z'):
                pitch_types[p_type]['release_point_z'].append(pitch['release_point_z'])
            if pitch.get('tunneling_distance'):
                pitch_types[p_type]['tunneling_distance'].append(pitch['tunneling_distance'])
            if pitch.get('tunneling_time'):
                pitch_types[p_type]['tunneling_time'].append(pitch['tunneling_time'])
        
        for p_type, data in pitch_types.items():
            usage_pct = data['usage_pct']
            avg_release_x = np.mean(data['release_point_x']) if data['release_point_x'] else 'N/A'
            avg_release_z = np.mean(data['release_point_z']) if data['release_point_z'] else 'N/A'
            avg_tunnel_dist = np.mean(data['tunneling_distance']) if data['tunneling_distance'] else 'N/A'
            avg_tunnel_time = np.mean(data['tunneling_time']) if data['tunneling_time'] else 'N/A'
            
            summary += f"""
**{p_type}:**
- Usage: {usage_pct:.1f}%
- Avg Release Point: ({avg_release_x:.2f}, {avg_release_z:.2f}) ft
- Avg Tunneling Distance: {avg_tunnel_dist:.2f} ft
- Avg Tunneling Time: {avg_tunnel_time:.3f} sec
"""
        
        return [TextContent(type="text", text=summary)]
    
    async def get_pitch_location_command(self, arguments: Dict[str, Any]) -> List[TextContent]:
        pitcher_name = arguments.get("pitcher_name")
        season = arguments.get("season", "2024")
        pitch_type = arguments.get("pitch_type")
        
        location_data = await self._fetch_location_command_data(pitcher_name, season)
        
        if not location_data:
            return [TextContent(type="text", text=f"No location data found for {pitcher_name} in {season}")]
        
        if pitch_type:
            location_data = [l for l in location_data if l.get('pitch_type') == pitch_type]
        
        summary = f"""
**{pitcher_name} - {season} Pitch Location & Command**

**Pitch Location / Command:**
"""
        
        pitch_types = {}
        for pitch in location_data:
            p_type = pitch.get('pitch_type', 'Unknown')
            if p_type not in pitch_types:
                pitch_types[p_type] = {
                    'count': 0,
                    'edge_pct': 0,
                    'zone_pct': 0,
                    'meatball_pct': 0,
                    'called_strike_pct': 0
                }
            
            pitch_types[p_type]['count'] += 1
            pitch_types[p_type]['edge_pct'] = pitch.get('edge_pct', 0)
            pitch_types[p_type]['zone_pct'] = pitch.get('zone_pct', 0)
            pitch_types[p_type]['meatball_pct'] = pitch.get('meatball_pct', 0)
            pitch_types[p_type]['called_strike_pct'] = pitch.get('called_strike_pct', 0)
        
        for p_type, data in pitch_types.items():
            edge_pct = data['edge_pct']
            zone_pct = data['zone_pct']
            meatball_pct = data['meatball_pct']
            called_strike_pct = data['called_strike_pct']
            
            summary += f"""
**{p_type}:**
- Edge%: {edge_pct:.1f}%
- Zone%: {zone_pct:.1f}%
- Meatball%: {meatball_pct:.1f}%
- Called Strike%: {called_strike_pct:.1f}%
"""
        
        return [TextContent(type="text", text=summary)]
    
    async def get_specialized_pitch_analysis(self, arguments: Dict[str, Any]) -> List[TextContent]:
        pitcher_name = arguments.get("pitcher_name")
        season = arguments.get("season", "2024")
        pitch_type = arguments.get("pitch_type")
        
        if not pitch_type:
            return [TextContent(type="text", text="Please specify a pitch type for specialized analysis")]
        
        specialized_data = await self._fetch_specialized_pitch_data(pitcher_name, season, pitch_type)
        
        if not specialized_data:
            return [TextContent(type="text", text=f"No specialized data found for {pitcher_name}'s {pitch_type} in {season}")]
        
        summary = f"""
**{pitcher_name} - {season} {pitch_type} Specialized Analysis**

**Specialized {pitch_type} Characteristics:**
"""
        
        if pitch_type.lower() == "fastball":
            summary += f"""
**Fastball Analysis:**
- IVB (Induced Vertical Break): {specialized_data.get('ivb', 'N/A')} inches
- "Ride" Factor: {specialized_data.get('ride_factor', 'N/A')}
- Hop Ratio: {specialized_data.get('hop_ratio', 'N/A')}
- Spin Efficiency: {specialized_data.get('spin_efficiency', 'N/A')}%
- Movement vs Avg: {specialized_data.get('movement_vs_avg', 'N/A')} inches
"""
        elif pitch_type.lower() in ["slider", "curveball"]:
            summary += f"""
**Breaking Ball Analysis:**
- Sweep (Horizontal Break): {specialized_data.get('sweep', 'N/A')} inches
- Spin Efficiency: {specialized_data.get('spin_efficiency', 'N/A')}%
- Gyro Spin Factor: {specialized_data.get('gyro_spin_factor', 'N/A')}
- Late Break: {specialized_data.get('late_break', 'N/A')} inches
- Movement vs Avg: {specialized_data.get('movement_vs_avg', 'N/A')} inches
"""
        elif pitch_type.lower() == "changeup":
            summary += f"""
**Changeup Analysis:**
- Velocity Differential: {specialized_data.get('velocity_differential', 'N/A')} mph
- Arm-Side Fade: {specialized_data.get('arm_side_fade', 'N/A')} inches
- Drop vs Fastball: {specialized_data.get('drop_vs_fastball', 'N/A')} inches
- Spin Efficiency: {specialized_data.get('spin_efficiency', 'N/A')}%
- Movement vs Avg: {specialized_data.get('movement_vs_avg', 'N/A')} inches
"""
        elif pitch_type.lower() == "sinker":
            summary += f"""
**Sinker Analysis:**
- Arm-Side Run: {specialized_data.get('arm_side_run', 'N/A')} inches
- IVB vs Fastball: {specialized_data.get('ivb_vs_fastball', 'N/A')} inches
- Ground Ball Rate: {specialized_data.get('ground_ball_rate', 'N/A')}%
- Movement vs Avg: {specialized_data.get('movement_vs_avg', 'N/A')} inches
"""
        else:
            summary += f"""
**General {pitch_type} Analysis:**
- Spin Rate: {specialized_data.get('spin_rate', 'N/A')} rpm
- Spin Efficiency: {specialized_data.get('spin_efficiency', 'N/A')}%
- IVB: {specialized_data.get('ivb', 'N/A')} inches
- HB: {specialized_data.get('hb', 'N/A')} inches
- Movement vs Avg: {specialized_data.get('movement_vs_avg', 'N/A')} inches
"""
        
        return [TextContent(type="text", text=summary)]
    
    async def get_run_prevention_metrics(self, arguments: Dict[str, Any]) -> List[TextContent]:
        pitcher_name = arguments.get("pitcher_name")
        season = arguments.get("season", "2024")
        
        run_prevention_data = await self._fetch_run_prevention_data(pitcher_name, season)
        
        if not run_prevention_data:
            return [TextContent(type="text", text=f"No run prevention data found for {pitcher_name} in {season}")]
        
        summary = f"""
**{pitcher_name} - {season} Run Prevention Metrics**

**ERA Alternatives:**
- ERA: {run_prevention_data.get('era', 'N/A')}
- ERA+: {run_prevention_data.get('era_plus', 'N/A')} (100 = league average, above is better)
- FIP: {run_prevention_data.get('fip', 'N/A')} (Fielding Independent Pitching)
- xFIP: {run_prevention_data.get('xfip', 'N/A')} (Expected FIP, normalizes HR/FB rate)
- SIERA: {run_prevention_data.get('siera', 'N/A')} (Skill-Interactive ERA, best predictor)

**Component Metrics:**
- K%: {run_prevention_data.get('k_percent', 'N/A')}%
- BB%: {run_prevention_data.get('bb_percent', 'N/A')}%
- K-BB%: {run_prevention_data.get('k_bb_percent', 'N/A')}%
- HR/9: {run_prevention_data.get('hr_per_9', 'N/A')}
- BABIP: {run_prevention_data.get('babip', 'N/A')}
"""
        
        return [TextContent(type="text", text=summary)]
    
    async def get_contact_quality_metrics(self, arguments: Dict[str, Any]) -> List[TextContent]:
        pitcher_name = arguments.get("pitcher_name")
        season = arguments.get("season", "2024")
        
        contact_data = await self._fetch_contact_quality_data(pitcher_name, season)
        
        if not contact_data:
            return [TextContent(type="text", text=f"No contact quality data found for {pitcher_name} in {season}")]
        
        summary = f"""
**{pitcher_name} - {season} Contact Quality & Batted Ball Metrics**

**Batted Ball Distribution:**
- GB% (Ground Ball): {contact_data.get('gb_percent', 'N/A')}%
- FB% (Fly Ball): {contact_data.get('fb_percent', 'N/A')}%
- LD% (Line Drive): {contact_data.get('ld_percent', 'N/A')}%
- HR/FB%: {contact_data.get('hr_fb_percent', 'N/A')}%

**Contact Quality (Statcast):**
- Hard Hit%: {contact_data.get('hard_hit_percent', 'N/A')}% (≥95 mph)
- Barrel%: {contact_data.get('barrel_percent', 'N/A')}% (ideal exit velocity + launch angle)
- Avg Exit Velocity: {contact_data.get('avg_exit_velocity', 'N/A')} mph
- Launch Angle: {contact_data.get('launch_angle', 'N/A')}°

**Expected Outcomes:**
- xERA: {contact_data.get('xera', 'N/A')} (Expected ERA based on contact quality)
- xBA: {contact_data.get('xba', 'N/A')} (Expected batting average)
- xSLG: {contact_data.get('xslg', 'N/A')} (Expected slugging)
- xwOBA: {contact_data.get('xwoba', 'N/A')} (Expected weighted on-base)
"""
        
        return [TextContent(type="text", text=summary)]
    
    async def get_win_probability_metrics(self, arguments: Dict[str, Any]) -> List[TextContent]:
        pitcher_name = arguments.get("pitcher_name")
        season = arguments.get("season", "2024")
        
        win_prob_data = await self._fetch_win_probability_data(pitcher_name, season)
        
        if not win_prob_data:
            return [TextContent(type="text", text=f"No win probability data found for {pitcher_name} in {season}")]
        
        summary = f"""
**{pitcher_name} - {season} Win Probability & Value Metrics**

**Overall Value:**
- WAR: {win_prob_data.get('war', 'N/A')} (Wins Above Replacement)
- WPA: {win_prob_data.get('wpa', 'N/A')} (Win Probability Added)
- RE24: {win_prob_data.get('re24', 'N/A')} (Run Expectancy 24 Base/Out States)

**Leverage & Situational:**
- gmLI: {win_prob_data.get('gmli', 'N/A')} (Average Leverage Index)
- Shutdowns: {win_prob_data.get('shutdowns', 'N/A')} (Significant WPA increases)
- Meltdowns: {win_prob_data.get('meltdowns', 'N/A')} (Significant WPA decreases)
- High Leverage IP: {win_prob_data.get('high_leverage_ip', 'N/A')}

**Clutch Performance:**
- WPA/LI: {win_prob_data.get('wpa_li', 'N/A')} (WPA per leverage situation)
- Clutch: {win_prob_data.get('clutch', 'N/A')} (Performance in high-leverage situations)
"""
        
        return [TextContent(type="text", text=summary)]
    
    async def get_plate_discipline_metrics(self, arguments: Dict[str, Any]) -> List[TextContent]:
        pitcher_name = arguments.get("pitcher_name")
        season = arguments.get("season", "2024")
        
        discipline_data = await self._fetch_plate_discipline_data(pitcher_name, season)
        
        if not discipline_data:
            return [TextContent(type="text", text=f"No plate discipline data found for {pitcher_name} in {season}")]
        
        summary = f"""
**{pitcher_name} - {season} Plate Discipline Metrics**

**Swing & Contact Rates:**
- O-Swing%: {discipline_data.get('o_swing_percent', 'N/A')}% (Out-of-zone swings)
- Z-Swing%: {discipline_data.get('z_swing_percent', 'N/A')}% (In-zone swings)
- SwStr%: {discipline_data.get('swstr_percent', 'N/A')}% (Swinging strike rate)
- CSW%: {discipline_data.get('csw_percent', 'N/A')}% (Called strikes + whiffs)
- Contact%: {discipline_data.get('contact_percent', 'N/A')}% (Contact when swinging)

**Strike Zone Control:**
- First Pitch Strike%: {discipline_data.get('first_pitch_strike_percent', 'N/A')}%
- Zone%: {discipline_data.get('zone_percent', 'N/A')}% (Pitches in strike zone)
- O-Contact%: {discipline_data.get('o_contact_percent', 'N/A')}% (Out-of-zone contact)
- Z-Contact%: {discipline_data.get('z_contact_percent', 'N/A')}% (In-zone contact)

**Plate Discipline Summary:**
- Chase Rate: {discipline_data.get('chase_rate', 'N/A')}%
- Whiff Rate: {discipline_data.get('whiff_rate', 'N/A')}%
- Called Strike Rate: {discipline_data.get('called_strike_rate', 'N/A')}%
"""
        
        return [TextContent(type="text", text=summary)]
    
    async def get_spin_aerodynamics_metrics(self, arguments: Dict[str, Any]) -> List[TextContent]:
        pitcher_name = arguments.get("pitcher_name")
        season = arguments.get("season", "2024")
        pitch_type = arguments.get("pitch_type")
        
        spin_data = await self._fetch_spin_aerodynamics_data(pitcher_name, season)
        
        if not spin_data:
            return [TextContent(type="text", text=f"No spin aerodynamics data found for {pitcher_name} in {season}")]
        
        if pitch_type:
            spin_data = [s for s in spin_data if s.get('pitch_type') == pitch_type]
        
        summary = f"""
**{pitcher_name} - {season} Spin & Aerodynamics Analysis**

**Seam-Shifted Wake (SSW) Analysis:**
- SSW Factor: {spin_data.get('ssw_factor', 'N/A')} (higher = more seam effects)
- True Spin Axis: {spin_data.get('true_spin_axis', 'N/A')}° (clock face)
- Observed Movement Axis: {spin_data.get('observed_movement_axis', 'N/A')}°
- SSW Discrepancy: {spin_data.get('ssw_discrepancy', 'N/A')}° (difference indicates seam effects)

**Magnus vs. Non-Magnus Movement:**
- Expected Magnus Movement: {spin_data.get('expected_magnus', 'N/A')} inches
- Actual Movement: {spin_data.get('actual_movement', 'N/A')} inches
- Non-Magnus Component: {spin_data.get('non_magnus_component', 'N/A')} inches
- Seam Effect Contribution: {spin_data.get('seam_effect_contribution', 'N/A')}%

**Advanced Spin Metrics:**
- Spin Efficiency: {spin_data.get('spin_efficiency', 'N/A')}%
- Gyro Spin Component: {spin_data.get('gyro_spin_component', 'N/A')}%
- Transverse Spin: {spin_data.get('transverse_spin', 'N/A')}%
- Spin-Based Movement: {spin_data.get('spin_based_movement', 'N/A')} inches
- Seam-Based Movement: {spin_data.get('seam_based_movement', 'N/A')} inches
"""
        
        return [TextContent(type="text", text=summary)]
    
    async def get_biomechanics_release_metrics(self, arguments: Dict[str, Any]) -> List[TextContent]:
        pitcher_name = arguments.get("pitcher_name")
        season = arguments.get("season", "2024")
        
        biomech_data = await self._fetch_biomechanics_release_data(pitcher_name, season)
        
        if not biomech_data:
            return [TextContent(type="text", text=f"No biomechanics data found for {pitcher_name} in {season}")]
        
        summary = f"""
**{pitcher_name} - {season} Biomechanics & Release Characteristics**

**Extension & Release Points:**
- Extension: {biomech_data.get('extension', 'N/A')} ft (distance in front of rubber)
- Release Height: {biomech_data.get('release_height', 'N/A')} ft
- Release Side: {biomech_data.get('release_side', 'N/A')} ft
- Vertical Release Point: {biomech_data.get('vertical_release_point', 'N/A')} ft
- Horizontal Release Point: {biomech_data.get('horizontal_release_point', 'N/A')} ft

**Delivery Mechanics:**
- Arm Slot: {biomech_data.get('arm_slot', 'N/A')}° (3/4, overhand, sidearm)
- Stride Length: {biomech_data.get('stride_length', 'N/A')} ft
- Hip-Shoulder Separation: {biomech_data.get('hip_shoulder_separation', 'N/A')}°
- Front Leg Stability: {biomech_data.get('front_leg_stability', 'N/A')} (1-10 scale)
- Release Consistency: {biomech_data.get('release_consistency', 'N/A')}% (standard deviation)

**Perceived Velocity Impact:**
- Raw Velocity: {biomech_data.get('raw_velocity', 'N/A')} mph
- Extension Boost: {biomech_data.get('extension_boost', 'N/A')} mph
- Perceived Velocity: {biomech_data.get('perceived_velocity', 'N/A')} mph
- Release Point Factor: {biomech_data.get('release_point_factor', 'N/A')} mph
"""
        
        return [TextContent(type="text", text=summary)]
    
    async def get_advanced_tunneling_metrics(self, arguments: Dict[str, Any]) -> List[TextContent]:
        pitcher_name = arguments.get("pitcher_name")
        season = arguments.get("season", "2024")
        pitch_comparison = arguments.get("pitch_comparison", "Fastball-Slider")
        
        tunneling_data = await self._fetch_advanced_tunneling_data(pitcher_name, season, pitch_comparison)
        
        if not tunneling_data:
            return [TextContent(type="text", text=f"No advanced tunneling data found for {pitcher_name} in {season}")]
        
        summary = f"""
**{pitcher_name} - {season} Advanced Tunneling Analysis: {pitch_comparison}**

**Release Point Consistency:**
- Release Distance (RelDist): {tunneling_data.get('release_distance', 'N/A')} ft
- Release Point Variance: {tunneling_data.get('release_point_variance', 'N/A')} ft
- Consistency Score: {tunneling_data.get('consistency_score', 'N/A')}% (1-100)

**Tunneling Metrics:**
- Tunnel Point: {tunneling_data.get('tunnel_point', 'N/A')} ft from plate
- Tunnel Distance: {tunneling_data.get('tunnel_distance', 'N/A')} inches
- Tunnel Differential: {tunneling_data.get('tunnel_differential', 'N/A')} inches
- Plate Differential: {tunneling_data.get('plate_differential', 'N/A')} inches

**Advanced Tunneling Analysis:**
- Break Tunneling Ratio: {tunneling_data.get('break_tunneling_ratio', 'N/A')} (higher = better)
- Deception Score: {tunneling_data.get('deception_score', 'N/A')}% (1-100)
- Tunneling Efficiency: {tunneling_data.get('tunneling_efficiency', 'N/A')}%
- Late Break Factor: {tunneling_data.get('late_break_factor', 'N/A')} inches

**Pitch-Specific Tunneling:**
- Fastball Tunneling: {tunneling_data.get('fastball_tunneling', 'N/A')} inches
- Breaking Ball Tunneling: {tunneling_data.get('breaking_ball_tunneling', 'N/A')} inches
- Changeup Tunneling: {tunneling_data.get('changeup_tunneling', 'N/A')} inches
"""
        
        return [TextContent(type="text", text=summary)]
    
    async def get_deception_perceptual_metrics(self, arguments: Dict[str, Any]) -> List[TextContent]:
        pitcher_name = arguments.get("pitcher_name")
        season = arguments.get("season", "2024")
        
        deception_data = await self._fetch_deception_perceptual_data(pitcher_name, season)
        
        if not deception_data:
            return [TextContent(type="text", text=f"No deception data found for {pitcher_name} in {season}")]
        
        summary = f"""
**{pitcher_name} - {season} Deception & Perceptual Metrics**

**Effective Velocity Analysis:**
- Raw Velocity: {deception_data.get('raw_velocity', 'N/A')} mph
- Effective Velocity: {deception_data.get('effective_velocity', 'N/A')} mph
- Location Adjustment: {deception_data.get('location_adjustment', 'N/A')} mph
- Extension Adjustment: {deception_data.get('extension_adjustment', 'N/A')} mph

**Perceived Velocity Factors:**
- Perceived Velocity: {deception_data.get('perceived_velocity', 'N/A')} mph
- Extension Boost: {deception_data.get('extension_boost', 'N/A')} mph
- Release Point Factor: {deception_data.get('release_point_factor', 'N/A')} mph
- Total Velocity Boost: {deception_data.get('total_velocity_boost', 'N/A')} mph

**Time to Plate Analysis:**
- Time to Plate: {deception_data.get('time_to_plate', 'N/A')} ms
- Reaction Window: {deception_data.get('reaction_window', 'N/A')} ms
- Decision Point: {deception_data.get('decision_point', 'N/A')} ft from plate
- Late Movement Window: {deception_data.get('late_movement_window', 'N/A')} ms

**Deception Summary:**
- Overall Deception Score: {deception_data.get('overall_deception_score', 'N/A')}% (1-100)
- Velocity Deception: {deception_data.get('velocity_deception', 'N/A')}% (1-100)
- Movement Deception: {deception_data.get('movement_deception', 'N/A')}% (1-100)
- Timing Deception: {deception_data.get('timing_deception', 'N/A')}% (1-100)
"""
        
        return [TextContent(type="text", text=summary)]
    
    async def get_pitch_shape_classification(self, arguments: Dict[str, Any]) -> List[TextContent]:
        pitcher_name = arguments.get("pitcher_name")
        season = arguments.get("season", "2024")
        pitch_type = arguments.get("pitch_type")
        
        shape_data = await self._fetch_pitch_shape_classification_data(pitcher_name, season)
        
        if not shape_data:
            return [TextContent(type="text", text=f"No pitch shape data found for {pitcher_name} in {season}")]
        
        if pitch_type:
            shape_data = [s for s in shape_data if s.get('pitch_type') == pitch_type]
        
        summary = f"""
**{pitcher_name} - {season} Pitch Shape Classification**

**Movement Clusters:**
- Primary Movement Pattern: {shape_data.get('primary_movement_pattern', 'N/A')}
- Secondary Movement: {shape_data.get('secondary_movement', 'N/A')}
- Movement Cluster: {shape_data.get('movement_cluster', 'N/A')}
- Shape Classification: {shape_data.get('shape_classification', 'N/A')}

**Axis Tilt Analysis:**
- Axis Tilt: {shape_data.get('axis_tilt', 'N/A')}° (clock face)
- Tilt Clock: {shape_data.get('tilt_clock', 'N/A')} (e.g., 2:30)
- Tilt Consistency: {shape_data.get('tilt_consistency', 'N/A')}%
- Tilt Variance: {shape_data.get('tilt_variance', 'N/A')}°

**Stuff+ Modeling (Eno Sarris):**
- Stuff+ Score: {shape_data.get('stuff_plus_score', 'N/A')} (100 = average, above = better)
- Velocity Component: {shape_data.get('velocity_component', 'N/A')}
- Movement Component: {shape_data.get('movement_component', 'N/A')}
- Location Component: {shape_data.get('location_component', 'N/A')}
- Overall Stuff Grade: {shape_data.get('overall_stuff_grade', 'N/A')} (A+ to F)

**Advanced Shape Metrics:**
- Break Pattern: {shape_data.get('break_pattern', 'N/A')}
- Late Movement: {shape_data.get('late_movement', 'N/A')} inches
- Movement Efficiency: {shape_data.get('movement_efficiency', 'N/A')}%
- Shape Uniqueness: {shape_data.get('shape_uniqueness', 'N/A')}% (1-100)
"""
        
        return [TextContent(type="text", text=summary)]
    
    async def get_contact_quality_by_pitch(self, arguments: Dict[str, Any]) -> List[TextContent]:
        pitcher_name = arguments.get("pitcher_name")
        season = arguments.get("season", "2024")
        pitch_type = arguments.get("pitch_type")
        
        contact_data = await self._fetch_contact_quality_by_pitch_data(pitcher_name, season)
        
        if not contact_data:
            return [TextContent(type="text", text=f"No contact quality by pitch data found for {pitcher_name} in {season}")]
        
        if pitch_type:
            contact_data = [c for c in contact_data if c.get('pitch_type') == pitch_type]
        
        summary = f"""
**{pitcher_name} - {season} Contact Quality by Pitch Type**

**Launch Angle Patterns:**
- Fastball Launch Angle: {contact_data.get('fastball_launch_angle', 'N/A')}°
- Slider Launch Angle: {contact_data.get('slider_launch_angle', 'N/A')}°
- Changeup Launch Angle: {contact_data.get('changeup_launch_angle', 'N/A')}°
- Curveball Launch Angle: {contact_data.get('curveball_launch_angle', 'N/A')}°

**Bat Speed Matchups:**
- Fastball Bat Speed Match: {contact_data.get('fastball_bat_speed_match', 'N/A')}% (1-100)
- Slider Bat Speed Match: {contact_data.get('slider_bat_speed_match', 'N/A')}% (1-100)
- Changeup Bat Speed Match: {contact_data.get('changeup_bat_speed_match', 'N/A')}% (1-100)
- Overall Bat Speed Exploitation: {contact_data.get('overall_bat_speed_exploitation', 'N/A')}%

**Expected Run Value by Location:**
- High Fastball xRV: {contact_data.get('high_fastball_xrv', 'N/A')} runs
- Low Slider xRV: {contact_data.get('low_slider_xrv', 'N/A')} runs
- Outside Changeup xRV: {contact_data.get('outside_changeup_xrv', 'N/A')} runs
- Inside Breaking Ball xRV: {contact_data.get('inside_breaking_ball_xrv', 'N/A')} runs

**Contact Quality Summary:**
- Weak Contact Rate: {contact_data.get('weak_contact_rate', 'N/A')}%
- Medium Contact Rate: {contact_data.get('medium_contact_rate', 'N/A')}%
- Hard Contact Rate: {contact_data.get('hard_contact_rate', 'N/A')}%
- Barrel Rate by Pitch: {contact_data.get('barrel_rate_by_pitch', 'N/A')}%
"""
        
        return [TextContent(type="text", text=summary)]
    
    async def get_biomechanics_tech_metrics(self, arguments: Dict[str, Any]) -> List[TextContent]:
        pitcher_name = arguments.get("pitcher_name")
        season = arguments.get("season", "season")
        
        tech_data = await self._fetch_biomechanics_tech_data(pitcher_name, season)
        
        if not tech_data:
            return [TextContent(type="text", text=f"No biomechanics tech data found for {pitcher_name} in {season}")]
        
        summary = f"""
**{pitcher_name} - {season} Cutting-Edge Biomechanics & Technology**

**Hawkeye / Markerless Motion Capture:**
- Hip-Shoulder Separation: {tech_data.get('hip_shoulder_separation', 'N/A')}°
- Separation Impact on Spin: {tech_data.get('separation_impact_on_spin', 'N/A')}%
- Front Leg Stability: {tech_data.get('front_leg_stability', 'N/A')} (1-10 scale)
- Stability Impact on Command: {tech_data.get('stability_impact_on_command', 'N/A')}%

**Kinematic Sequencing Data:**
- Rotation Order: {tech_data.get('rotation_order', 'N/A')}
- Sequencing Efficiency: {tech_data.get('sequencing_efficiency', 'N/A')}%
- Timing Consistency: {tech_data.get('timing_consistency', 'N/A')}%
- Mechanical Repeatability: {tech_data.get('mechanical_repeatability', 'N/A')}%

**Grip Analysis (High-Speed Cameras):**
- Seam Orientation: {tech_data.get('seam_orientation', 'N/A')}°
- Grip Consistency: {tech_data.get('grip_consistency', 'N/A')}%
- Seam Pressure Points: {tech_data.get('seam_pressure_points', 'N/A')}
- Grip Impact on Movement: {tech_data.get('grip_impact_on_movement', 'N/A')}%

**Advanced Biomechanics:**
- Arm Path Efficiency: {tech_data.get('arm_path_efficiency', 'N/A')}%
- Kinetic Chain Transfer: {tech_data.get('kinetic_chain_transfer', 'N/A')}%
- Energy Transfer Efficiency: {tech_data.get('energy_transfer_efficiency', 'N/A')}%
- Overall Mechanical Grade: {tech_data.get('overall_mechanical_grade', 'N/A')} (A+ to F)
"""
        
        return [TextContent(type="text", text=summary)]
    
    async def _fetch_pitcher_stats(self, pitcher_name: str, season: str) -> Optional[Dict]:
        try:
            if self.baseball_api_key:
                url = f"https://api.mlb.com/v1/stats/players"
                params = {
                    "personIds": await self._get_pitcher_id(pitcher_name),
                    "group": "pitching",
                    "season": season,
                    "stats": "season"
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_pitcher_stats(data)
            
            return self._get_mock_pitcher_stats(pitcher_name, season)
        except Exception as e:
            logger.error(f"Error fetching pitcher stats: {e}")
            return self._get_mock_pitcher_stats(pitcher_name, season)
    
    async def _fetch_pitch_data(self, pitcher_name: str, season: str) -> Optional[List[Dict]]:
        try:
            if self.baseball_api_key:
                url = f"https://api.mlb.com/v1/stats/players"
                params = {
                    "personIds": await self._get_pitcher_id(pitcher_name),
                    "group": "pitching",
                    "season": season,
                    "stats": "pitch"
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_pitch_data(data)
            
            return self._get_mock_pitch_data(pitcher_name, season)
        except Exception as e:
            logger.error(f"Error fetching pitch data: {e}")
            return self._get_mock_pitch_data(pitcher_name, season)
    
    async def _fetch_efficiency_metrics(self, pitcher_name: str, season: str) -> Optional[Dict]:
        try:
            if self.baseball_api_key:
                url = f"https://api.mlb.com/v1/stats/players"
                params = {
                    "personIds": await self._get_pitcher_id(pitcher_name),
                    "group": "pitching",
                    "season": season,
                    "stats": "advanced"
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_efficiency_metrics(data)
            
            return self._get_mock_efficiency_metrics(pitcher_name, season)
        except Exception as e:
            logger.error(f"Error fetching efficiency metrics: {e}")
            return self._get_mock_efficiency_metrics(pitcher_name, season)
    
    async def _fetch_sequence_data(self, pitcher_name: str, season: str) -> Optional[Dict]:
        try:
            if self.baseball_api_key:
                url = f"https://api.mlb.com/v1/stats/players"
                params = {
                    "personIds": await self._get_pitcher_id(pitcher_name),
                    "group": "pitching",
                    "season": season,
                    "stats": "sequence"
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_sequence_data(data)
            
            return self._get_mock_sequence_data(pitcher_name, season)
        except Exception as e:
            logger.error(f"Error fetching sequence data: {e}")
            return self._get_mock_sequence_data(pitcher_name, season)
    
    async def _fetch_pitch_quality_data(self, pitcher_name: str, season: str) -> Optional[List[Dict]]:
        try:
            if self.baseball_api_key:
                url = f"https://api.mlb.com/v1/stats/players"
                params = {
                    "personIds": await self._get_pitcher_id(pitcher_name),
                    "group": "pitching",
                    "season": season,
                    "stats": "pitch_quality"
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_pitch_quality_data(data)
            
            return self._get_mock_pitch_quality_data(pitcher_name, season)
        except Exception as e:
            logger.error(f"Error fetching pitch quality data: {e}")
            return self._get_mock_pitch_quality_data(pitcher_name, season)
    
    async def _fetch_usage_tunneling_data(self, pitcher_name: str, season: str) -> Optional[List[Dict]]:
        try:
            if self.baseball_api_key:
                url = f"https://api.mlb.com/v1/stats/players"
                params = {
                    "personIds": await self._get_pitcher_id(pitcher_name),
                    "group": "pitching",
                    "season": season,
                    "stats": "usage_tunneling"
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_usage_tunneling_data(data)
            
            return self._get_mock_usage_tunneling_data(pitcher_name, season)
        except Exception as e:
            logger.error(f"Error fetching usage tunneling data: {e}")
            return self._get_mock_usage_tunneling_data(pitcher_name, season)
    
    async def _fetch_location_command_data(self, pitcher_name: str, season: str) -> Optional[List[Dict]]:
        try:
            if self.baseball_api_key:
                url = f"https://api.mlb.com/v1/stats/players"
                params = {
                    "personIds": await self._get_pitcher_id(pitcher_name),
                    "group": "pitching",
                    "season": season,
                    "stats": "location_command"
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_location_command_data(data)
            
            return self._get_mock_location_command_data(pitcher_name, season)
        except Exception as e:
            logger.error(f"Error fetching location command data: {e}")
            return self._get_mock_location_command_data(pitcher_name, season)
    
    async def _fetch_specialized_pitch_data(self, pitcher_name: str, season: str, pitch_type: str) -> Optional[Dict]:
        try:
            if self.baseball_api_key:
                url = f"https://api.mlb.com/v1/stats/players"
                params = {
                    "personIds": await self._get_pitcher_id(pitcher_name),
                    "group": "pitching",
                    "season": season,
                    "stats": "specialized_pitch",
                    "pitchType": pitch_type
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_specialized_pitch_data(data)
            
            return self._get_mock_specialized_pitch_data(pitcher_name, season, pitch_type)
        except Exception as e:
            logger.error(f"Error fetching specialized pitch data: {e}")
            return self._get_mock_specialized_pitch_data(pitcher_name, season, pitch_type)
    
    async def _fetch_run_prevention_data(self, pitcher_name: str, season: str) -> Optional[Dict]:
        try:
            if self.baseball_api_key:
                url = f"https://api.mlb.com/v1/stats/players"
                params = {
                    "personIds": await self._get_pitcher_id(pitcher_name),
                    "group": "pitching",
                    "season": season,
                    "stats": "run_prevention"
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_run_prevention_data(data)
            
            return self._get_mock_run_prevention_data(pitcher_name, season)
        except Exception as e:
            logger.error(f"Error fetching run prevention data: {e}")
            return self._get_mock_run_prevention_data(pitcher_name, season)
    
    async def _fetch_contact_quality_data(self, pitcher_name: str, season: str) -> Optional[Dict]:
        try:
            if self.baseball_api_key:
                url = f"https://api.mlb.com/v1/stats/players"
                params = {
                    "personIds": await self._get_pitcher_id(pitcher_name),
                    "group": "pitching",
                    "season": season,
                    "stats": "contact_quality"
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_contact_quality_data(data)
            
            return self._get_mock_contact_quality_data(pitcher_name, season)
        except Exception as e:
            logger.error(f"Error fetching contact quality data: {e}")
            return self._get_mock_contact_quality_data(pitcher_name, season)
    
    async def _fetch_win_probability_data(self, pitcher_name: str, season: str) -> Optional[Dict]:
        try:
            if self.baseball_api_key:
                url = f"https://api.mlb.com/v1/stats/players"
                params = {
                    "personIds": await self._get_pitcher_id(pitcher_name),
                    "group": "pitching",
                    "season": season,
                    "stats": "win_probability"
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_win_probability_data(data)
            
            return self._get_mock_win_probability_data(pitcher_name, season)
        except Exception as e:
            logger.error(f"Error fetching win probability data: {e}")
            return self._get_mock_win_probability_data(pitcher_name, season)
    
    async def _fetch_plate_discipline_data(self, pitcher_name: str, season: str) -> Optional[Dict]:
        try:
            if self.baseball_api_key:
                url = f"https://api.mlb.com/v1/stats/players"
                params = {
                    "personIds": await self._get_pitcher_id(pitcher_name),
                    "group": "pitching",
                    "season": season,
                    "stats": "plate_discipline"
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_plate_discipline_data(data)
            
            return self._get_mock_plate_discipline_data(pitcher_name, season)
        except Exception as e:
            logger.error(f"Error fetching plate discipline data: {e}")
            return self._get_mock_plate_discipline_data(pitcher_name, season)
    
    async def _fetch_spin_aerodynamics_data(self, pitcher_name: str, season: str) -> Optional[Dict]:
        try:
            if self.baseball_api_key:
                url = f"https://api.mlb.com/v1/stats/players"
                params = {
                    "personIds": await self._get_pitcher_id(pitcher_name),
                    "group": "pitching",
                    "season": season,
                    "stats": "spin_aerodynamics"
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_spin_aerodynamics_data(data)
            
            return self._get_mock_spin_aerodynamics_data(pitcher_name, season)
        except Exception as e:
            logger.error(f"Error fetching spin aerodynamics data: {e}")
            return self._get_mock_spin_aerodynamics_data(pitcher_name, season)
    
    async def _fetch_biomechanics_release_data(self, pitcher_name: str, season: str) -> Optional[Dict]:
        try:
            if self.baseball_api_key:
                url = f"https://api.mlb.com/v1/stats/players"
                params = {
                    "personIds": await self._get_pitcher_id(pitcher_name),
                    "group": "pitching",
                    "season": season,
                    "stats": "biomechanics_release"
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_biomechanics_release_data(data)
            
            return self._get_mock_biomechanics_release_data(pitcher_name, season)
        except Exception as e:
            logger.error(f"Error fetching biomechanics release data: {e}")
            return self._get_mock_biomechanics_release_data(pitcher_name, season)
    
    async def _fetch_advanced_tunneling_data(self, pitcher_name: str, season: str, pitch_comparison: str) -> Optional[Dict]:
        try:
            if self.baseball_api_key:
                url = f"https://api.mlb.com/v1/stats/players"
                params = {
                    "personIds": await self._get_pitcher_id(pitcher_name),
                    "group": "pitching",
                    "season": season,
                    "stats": "advanced_tunneling",
                    "pitchComparison": pitch_comparison
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_advanced_tunneling_data(data)
            
            return self._get_mock_advanced_tunneling_data(pitcher_name, season, pitch_comparison)
        except Exception as e:
            logger.error(f"Error fetching advanced tunneling data: {e}")
            return self._get_mock_advanced_tunneling_data(pitcher_name, season, pitch_comparison)
    
    async def _fetch_deception_perceptual_data(self, pitcher_name: str, season: str) -> Optional[Dict]:
        try:
            if self.baseball_api_key:
                url = f"https://api.mlb.com/v1/stats/players"
                params = {
                    "personIds": await self._get_pitcher_id(pitcher_name),
                    "group": "pitching",
                    "season": season,
                    "stats": "deception_perceptual"
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_deception_perceptual_data(data)
            
            return self._get_mock_deception_perceptual_data(pitcher_name, season)
        except Exception as e:
            logger.error(f"Error fetching deception perceptual data: {e}")
            return self._get_mock_deception_perceptual_data(pitcher_name, season)
    
    async def _fetch_pitch_shape_classification_data(self, pitcher_name: str, season: str) -> Optional[Dict]:
        try:
            if self.baseball_api_key:
                url = f"https://api.mlb.com/v1/stats/players"
                params = {
                    "personIds": await self._get_pitcher_id(pitcher_name),
                    "group": "pitching",
                    "season": season,
                    "stats": "pitch_shape_classification"
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_pitch_shape_classification_data(data)
            
            return self._get_mock_pitch_shape_classification_data(pitcher_name, season)
        except Exception as e:
            logger.error(f"Error fetching pitch shape classification data: {e}")
            return self._get_mock_pitch_shape_classification_data(pitcher_name, season)
    
    async def _fetch_contact_quality_by_pitch_data(self, pitcher_name: str, season: str) -> Optional[Dict]:
        try:
            if self.baseball_api_key:
                url = f"https://api.mlb.com/v1/stats/players"
                params = {
                    "personIds": await self._get_pitcher_id(pitcher_name),
                    "group": "pitching",
                    "season": season,
                    "stats": "contact_quality_by_pitch"
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_contact_quality_by_pitch_data(data)
            
            return self._get_mock_contact_quality_by_pitch_data(pitcher_name, season)
        except Exception as e:
            logger.error(f"Error fetching contact quality by pitch data: {e}")
            return self._get_mock_contact_quality_by_pitch_data(pitcher_name, season)
    
    async def _fetch_biomechanics_tech_data(self, pitcher_name: str, season: str) -> Optional[Dict]:
        try:
            if self.baseball_api_key:
                url = f"https://api.mlb.com/v1/stats/players"
                params = {
                    "personIds": await self._get_pitcher_id(pitcher_name),
                    "group": "pitching",
                    "season": season,
                    "stats": "biomechanics_tech"
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_biomechanics_tech_data(data)
            
            return self._get_mock_biomechanics_tech_data(pitcher_name, season)
        except Exception as e:
            logger.error(f"Error fetching biomechanics tech data: {e}")
            return self._get_mock_biomechanics_tech_data(pitcher_name, season)
    
    async def _get_pitcher_id(self, pitcher_name: str) -> str:
        try:
            url = "https://api.mlb.com/v1/people"
            params = {"search": pitcher_name}
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get("people"):
                    return str(data["people"][0]["id"])
        except Exception as e:
            logger.error(f"Error getting pitcher ID: {e}")
        return ""
    
    async def _scrape_news(self, source: str, query: str) -> Optional[str]:
        try:
            headers = {"Authorization": f"Bearer {self.firecrawl_token}"}
            url = "https://api.firecrawl.dev/scrape"
            params = {
                "url": f"https://{source}/search?q={query}",
                "formats": ["markdown"],
                "onlyMainContent": True
            }
            response = requests.post(url, json=params, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return data.get("data", {}).get("markdown", "")
        except Exception as e:
            logger.error(f"Error scraping news: {e}")
        return None
    
    def _create_movement_chart(self, pitch_data: List[Dict], pitcher_name: str, season: str):
        fig = go.Figure()
        
        for pitch_type in set(p.get('pitch_type', 'Unknown') for p in pitch_data):
            type_data = [p for p in pitch_data if p.get('pitch_type') == pitch_type]
            if type_data:
                horizontal_movement = [p.get('horizontal_movement', 0) for p in type_data]
                vertical_movement = [p.get('vertical_movement', 0) for p in type_data]
                
                fig.add_trace(go.Scatter(
                    x=horizontal_movement,
                    y=vertical_movement,
                    mode='markers',
                    name=pitch_type,
                    marker=dict(size=8, opacity=0.7)
                ))
        
        fig.update_layout(
            title=f"{pitcher_name} - {season} Pitch Movement Chart",
            xaxis_title="Horizontal Movement (inches)",
            yaxis_title="Vertical Movement (inches)",
            hovermode='closest'
        )
        
        return fig
    
    def _create_velocity_chart(self, pitch_data: List[Dict], pitcher_name: str, season: str):
        fig = go.Figure()
        
        for pitch_type in set(p.get('pitch_type', 'Unknown') for p in pitch_data):
            type_data = [p for p in pitch_data if p.get('pitch_type') == pitch_type]
            if type_data:
                velocities = [p.get('velocity', 0) for p in type_data if p.get('velocity')]
                if velocities:
                    fig.add_trace(go.Box(
                        y=velocities,
                        name=pitch_type,
                        boxpoints='outliers'
                    ))
        
        fig.update_layout(
            title=f"{pitcher_name} - {season} Pitch Velocity Distribution",
            yaxis_title="Velocity (mph)",
            showlegend=True
        )
        
        return fig
    
    def _create_location_chart(self, pitch_data: List[Dict], pitcher_name: str, season: str):
        fig = go.Figure()
        
        for pitch_type in set(p.get('pitch_type', 'Unknown') for p in pitch_data):
            type_data = [p for p in pitch_data if p.get('pitch_type') == pitch_type]
            if type_data:
                x_locations = [p.get('x_location', 0) for p in type_data]
                z_locations = [p.get('z_location', 0) for p in type_data]
                
                fig.add_trace(go.Scatter(
                    x=x_locations,
                    y=z_locations,
                    mode='markers',
                    name=pitch_type,
                    marker=dict(size=6, opacity=0.6)
                ))
        
        fig.update_layout(
            title=f"{pitcher_name} - {season} Pitch Location Chart",
            xaxis_title="Horizontal Location (feet)",
            yaxis_title="Vertical Location (feet)",
            hovermode='closest'
        )
        
        return fig
    
    def _create_heatmap_chart(self, pitch_data: List[Dict], pitcher_name: str, season: str):
        fig = go.Figure()
        
        x_locations = [p.get('x_location', 0) for p in pitch_data if p.get('x_location')]
        z_locations = [p.get('z_location', 0) for p in pitch_data if p.get('z_location')]
        
        if x_locations and z_locations:
            fig.add_trace(go.Histogram2d(
                x=x_locations,
                y=z_locations,
                nbinsx=20,
                nbinsy=20,
                colorscale='Viridis'
            ))
        
        fig.update_layout(
            title=f"{pitcher_name} - {season} Pitch Location Heatmap",
            xaxis_title="Horizontal Location (feet)",
            yaxis_title="Vertical Location (feet)"
        )
        
        return fig
    
    def _parse_pitcher_stats(self, data: Dict) -> Optional[Dict]:
        try:
            if data.get("stats") and data["stats"]:
                stats = data["stats"][0]
                return {
                    "wins": stats.get("wins", 0),
                    "losses": stats.get("losses", 0),
                    "era": stats.get("era", 0.0),
                    "innings_pitched": stats.get("inningsPitched", 0.0),
                    "strikeouts": stats.get("strikeOuts", 0),
                    "walks": stats.get("baseOnBalls", 0),
                    "whip": stats.get("whip", 0.0),
                    "k_per_9": stats.get("strikeOutsPer9Inn", 0.0),
                    "bb_per_9": stats.get("baseOnBallsPer9Inn", 0.0),
                    "hr_per_9": stats.get("homeRunsPer9Inn", 0.0),
                    "fip": stats.get("fip", 0.0),
                    "xfip": stats.get("xfip", 0.0),
                    "babip": stats.get("babip", 0.0)
                }
        except Exception as e:
            logger.error(f"Error parsing pitcher stats: {e}")
        return None
    
    def _parse_pitch_data(self, data: Dict) -> Optional[List[Dict]]:
        try:
            if data.get("stats") and data["stats"]:
                pitches = data["stats"][0].get("pitches", [])
                return [
                    {
                        "pitch_type": p.get("pitchType", "Unknown"),
                        "velocity": p.get("velocity", 0),
                        "movement": p.get("movement", 0),
                        "horizontal_movement": p.get("horizontalMovement", 0),
                        "vertical_movement": p.get("verticalMovement", 0),
                        "x_location": p.get("xLocation", 0),
                        "z_location": p.get("zLocation", 0)
                    }
                    for p in pitches
                ]
        except Exception as e:
            logger.error(f"Error parsing pitch data: {e}")
        return None
    
    def _parse_efficiency_metrics(self, data: Dict) -> Optional[Dict]:
        try:
            if data.get("stats") and data["stats"]:
                stats = data["stats"][0]
                return {
                    "whiff_rate": stats.get("whiffRate", 0.0),
                    "chase_rate": stats.get("chaseRate", 0.0),
                    "barrel_pct": stats.get("barrelPct", 0.0),
                    "hard_hit_rate": stats.get("hardHitRate", 0.0),
                    "zone_rate": stats.get("zoneRate", 0.0),
                    "first_pitch_strike_rate": stats.get("firstPitchStrikeRate", 0.0),
                    "swinging_strike_rate": stats.get("swingingStrikeRate", 0.0),
                    "called_strike_rate": stats.get("calledStrikeRate", 0.0),
                    "csw_pct": stats.get("cswPct", 0.0),
                    "o_swing_pct": stats.get("oSwingPct", 0.0),
                    "z_swing_pct": stats.get("zSwingPct", 0.0),
                    "o_contact_pct": stats.get("oContactPct", 0.0),
                    "z_contact_pct": stats.get("zContactPct", 0.0)
                }
        except Exception as e:
            logger.error(f"Error parsing efficiency metrics: {e}")
        return None
    
    def _parse_sequence_data(self, data: Dict) -> Optional[Dict]:
        try:
            if data.get("stats") and data["stats"]:
                stats = data["stats"][0]
                return {
                    "most_common_first_pitch": stats.get("mostCommonFirstPitch", "Unknown"),
                    "first_pitch_strike_rate": stats.get("firstPitchStrikeRate", 0.0),
                    "two_strike_approach": stats.get("twoStrikeApproach", "Unknown"),
                    "count_tendencies": stats.get("countTendencies", {})
                }
        except Exception as e:
            logger.error(f"Error parsing sequence data: {e}")
        return None
    
    async def _fetch_batter_stats(self, batter_name: str, season: str) -> Optional[Dict]:
        try:
            if self.baseball_api_key:
                url = f"https://api.mlb.com/v1/stats/players"
                params = {
                    "personIds": await self._get_batter_id(batter_name),
                    "group": "hitting",
                    "season": season,
                    "stats": "season"
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_batter_stats(data)
            
            return self._get_mock_batter_stats(batter_name, season)
        except Exception as e:
            logger.error(f"Error fetching batter stats: {e}")
            return self._get_mock_batter_stats(batter_name, season)
    
    async def _fetch_batter_contact_quality(self, batter_name: str, season: str) -> Optional[Dict]:
        try:
            if self.baseball_api_key:
                url = f"https://api.mlb.com/v1/stats/players"
                params = {
                    "personIds": await self._get_batter_id(batter_name),
                    "group": "hitting",
                    "season": season,
                    "stats": "statcast"
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_batter_contact_quality(data)
            
            return self._get_mock_batter_contact_quality(batter_name, season)
        except Exception as e:
            logger.error(f"Error fetching batter contact quality: {e}")
            return self._get_mock_batter_contact_quality(batter_name, season)
    
    async def _fetch_batter_plate_discipline(self, batter_name: str, season: str) -> Optional[Dict]:
        try:
            if self.baseball_api_key:
                url = f"https://api.mlb.com/v1/stats/players"
                params = {
                    "personIds": await self._get_batter_id(batter_name),
                    "group": "hitting",
                    "season": season,
                    "stats": "plate_discipline"
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_batter_plate_discipline(data)
            
            return self._get_mock_batter_plate_discipline(batter_name, season)
        except Exception as e:
            logger.error(f"Error fetching batter plate discipline: {e}")
            return self._get_mock_batter_plate_discipline(batter_name, season)
    
    async def _fetch_batter_expected_outcomes(self, batter_name: str, season: str) -> Optional[Dict]:
        try:
            if self.baseball_api_key:
                url = f"https://api.mlb.com/v1/stats/players"
                params = {
                    "personIds": await self._get_batter_id(batter_name),
                    "group": "hitting",
                    "season": season,
                    "stats": "statcast"
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_batter_expected_outcomes(data)
            
            return self._get_mock_batter_expected_outcomes(batter_name, season)
        except Exception as e:
            logger.error(f"Error fetching batter expected outcomes: {e}")
            return self._get_mock_batter_expected_outcomes(batter_name, season)
    
    async def _fetch_batter_batted_ball_profile(self, batter_name: str, season: str) -> Optional[Dict]:
        try:
            if self.baseball_api_key:
                url = f"https://api.mlb.com/v1/stats/players"
                params = {
                    "personIds": await self._get_batter_id(batter_name),
                    "group": "hitting",
                    "season": season,
                    "stats": "batted_ball"
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_batter_batted_ball_profile(data)
            
            return self._get_mock_batter_batted_ball_profile(batter_name, season)
        except Exception as e:
            logger.error(f"Error fetching batter batted ball profile: {e}")
            return self._get_mock_batter_batted_ball_profile(batter_name, season)
    
    async def _fetch_batter_speed_metrics(self, batter_name: str, season: str) -> Optional[Dict]:
        try:
            if self.baseball_api_key:
                url = f"https://api.mlb.com/v1/stats/players"
                params = {
                    "personIds": await self._get_batter_id(batter_name),
                    "group": "hitting",
                    "season": season,
                    "stats": "speed"
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_batter_speed_metrics(data)
            
            return self._get_mock_batter_speed_metrics(batter_name, season)
        except Exception as e:
            logger.error(f"Error fetching batter speed metrics: {e}")
            return self._get_mock_batter_speed_metrics(batter_name, season)
    
    async def _fetch_batter_clutch_performance(self, batter_name: str, season: str) -> Optional[Dict]:
        try:
            if self.baseball_api_key:
                url = f"https://api.mlb.com/v1/stats/players"
                params = {
                    "personIds": await self._get_batter_id(batter_name),
                    "group": "hitting",
                    "season": season,
                    "stats": "clutch"
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_batter_clutch_performance(data)
            
            return self._get_mock_batter_clutch_performance(batter_name, season)
        except Exception as e:
            logger.error(f"Error fetching batter clutch performance: {e}")
            return self._get_mock_batter_clutch_performance(batter_name, season)
    
    async def _fetch_pitcher_defensive_metrics(self, pitcher_name: str, season: str) -> Optional[Dict]:
        try:
            if self.baseball_api_key:
                url = f"https://api.mlb.com/v1/stats/players"
                params = {
                    "personIds": await self._get_pitcher_id(pitcher_name),
                    "group": "pitching",
                    "season": season,
                    "stats": "fielding"
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_pitcher_defensive_metrics(data)
            
            return self._get_mock_pitcher_defensive_metrics(pitcher_name, season)
        except Exception as e:
            logger.error(f"Error fetching pitcher defensive metrics: {e}")
            return self._get_mock_pitcher_defensive_metrics(pitcher_name, season)
    
    async def _fetch_batter_defensive_metrics(self, batter_name: str, season: str, position: str = "all") -> Optional[Dict]:
        try:
            if self.baseball_api_key:
                url = f"https://api.mlb.com/v1/stats/players"
                params = {
                    "personIds": await self._get_batter_id(batter_name),
                    "group": "hitting",
                    "season": season,
                    "stats": "fielding"
                }
                if position != "all":
                    params["position"] = position
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_batter_defensive_metrics(data)
            
            return self._get_mock_batter_defensive_metrics(batter_name, season, position)
        except Exception as e:
            logger.error(f"Error fetching batter defensive metrics: {e}")
            return self._get_mock_batter_defensive_metrics(batter_name, season, position)
    
    async def _get_batter_id(self, batter_name: str) -> str:
        try:
            url = "https://api.mlb.com/v1/people"
            params = {"search": batter_name}
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get("people"):
                    return str(data["people"][0]["id"])
        except Exception as e:
            logger.error(f"Error getting batter ID: {e}")
        return ""
    
    def _get_mock_pitcher_stats(self, pitcher_name: str, season: str) -> Dict:
        return {
            "wins": 15,
            "losses": 8,
            "era": 3.45,
            "innings_pitched": 180.2,
            "strikeouts": 195,
            "walks": 45,
            "whip": 1.18,
            "k_per_9": 9.7,
            "bb_per_9": 2.2,
            "hr_per_9": 0.8,
            "fip": 3.52,
            "xfip": 3.48,
            "babip": 0.285,
            "k_percent": 28.5,
            "bb_percent": 6.8,
            "k_bb_percent": 21.7
        }
    
    def _get_mock_pitch_data(self, pitcher_name: str, season: str) -> List[Dict]:
        return [
            {"pitch_type": "Fastball", "velocity": 95.2, "movement": 12.5, "horizontal_movement": 2.1, "vertical_movement": 12.5, "x_location": -0.8, "z_location": 2.9, "spin_rate": 2450, "spin_efficiency": 0.92, "ivb": 15.2, "hb": 2.1, "movement_vs_avg": 2.3},
            {"pitch_type": "Fastball", "velocity": 94.8, "movement": 11.8, "horizontal_movement": 1.9, "vertical_movement": 11.8, "x_location": 0.2, "z_location": 3.1, "spin_rate": 2420, "spin_efficiency": 0.89, "ivb": 14.8, "hb": 1.9, "movement_vs_avg": 1.9},
            {"pitch_type": "Slider", "velocity": 87.3, "movement": 8.2, "horizontal_movement": -3.2, "vertical_movement": 8.2, "x_location": -1.1, "z_location": 2.7, "spin_rate": 2850, "spin_efficiency": 0.78, "ivb": -8.5, "hb": -3.2, "movement_vs_avg": -1.8},
            {"pitch_type": "Slider", "velocity": 86.9, "movement": 7.9, "horizontal_movement": -2.8, "vertical_movement": 7.9, "x_location": 0.5, "z_location": 2.5, "spin_rate": 2820, "spin_efficiency": 0.75, "ivb": -8.1, "hb": -2.8, "movement_vs_avg": -1.5},
            {"pitch_type": "Changeup", "velocity": 84.1, "movement": 6.5, "horizontal_movement": 1.2, "vertical_movement": 6.5, "x_location": -0.3, "z_location": 2.8, "spin_rate": 1850, "spin_efficiency": 0.85, "ivb": -12.3, "hb": 1.2, "movement_vs_avg": -0.8}
        ]
    
    def _get_mock_efficiency_metrics(self, pitcher_name: str, season: str) -> Dict:
        return {
            "whiff_rate": 28.5,
            "chase_rate": 32.1,
            "barrel_pct": 6.8,
            "hard_hit_rate": 35.2,
            "zone_rate": 48.7,
            "first_pitch_strike_rate": 62.3,
            "swinging_strike_rate": 12.8,
            "called_strike_rate": 18.9,
            "csw_pct": 31.7,
            "o_swing_pct": 32.1,
            "z_swing_pct": 65.4,
            "o_contact_pct": 58.2,
            "z_contact_pct": 82.1,
            "whiff_per_pitch": 24.3,
            "csw_per_pitch": 28.9,
            "putaway_pct": 18.7,
            "xba_vs_pitch": 0.218,
            "xslg_vs_pitch": 0.342,
            "xwoba_vs_pitch": 0.298,
            "run_value": 12.4,
            "rv_per_100": 1.8
        }
    
    def _get_mock_sequence_data(self, pitcher_name: str, season: str) -> Dict:
        return {
            "most_common_first_pitch": "Fastball",
            "first_pitch_strike_rate": 62.3,
            "two_strike_approach": "Slider-heavy",
            "count_tendencies": {
                "0-0": "Fastball (65%)",
                "0-1": "Slider (45%)",
                "0-2": "Slider (70%)",
                "1-0": "Fastball (80%)",
                "1-1": "Fastball (55%)",
                "1-2": "Slider (60%)",
                "2-0": "Fastball (90%)",
                "2-1": "Fastball (60%)",
                "2-2": "Slider (75%)",
                "3-0": "Fastball (95%)",
                "3-1": "Fastball (70%)",
                "3-2": "Slider (80%)"
            }
        }
    
    def _parse_pitch_quality_data(self, data: Dict) -> Optional[List[Dict]]:
        try:
            if data.get("stats") and data["stats"]:
                pitches = data["stats"][0].get("pitches", [])
                return [
                    {
                        "pitch_type": p.get("pitchType", "Unknown"),
                        "velocity": p.get("velocity", 0),
                        "spin_rate": p.get("spinRate", 0),
                        "spin_axis": p.get("spinAxis", 0),
                        "spin_efficiency": p.get("spinEfficiency", 0),
                        "ivb": p.get("ivb", 0),
                        "hb": p.get("hb", 0),
                        "movement_vs_avg": p.get("movementVsAvg", 0)
                    }
                    for p in pitches
                ]
        except Exception as e:
            logger.error(f"Error parsing pitch quality data: {e}")
        return None
    
    def _parse_usage_tunneling_data(self, data: Dict) -> Optional[List[Dict]]:
        try:
            if data.get("stats") and data["stats"]:
                pitches = data["stats"][0].get("pitches", [])
                return [
                    {
                        "pitch_type": p.get("pitchType", "Unknown"),
                        "usage_pct": p.get("usagePct", 0),
                        "release_point_x": p.get("releasePointX", 0),
                        "release_point_z": p.get("releasePointZ", 0),
                        "tunneling_distance": p.get("tunnelingDistance", 0),
                        "tunneling_time": p.get("tunnelingTime", 0)
                    }
                    for p in pitches
                ]
        except Exception as e:
            logger.error(f"Error parsing usage tunneling data: {e}")
        return None
    
    def _parse_location_command_data(self, data: Dict) -> Optional[List[Dict]]:
        try:
            if data.get("stats") and data["stats"]:
                pitches = data["stats"][0].get("pitches", [])
                return [
                    {
                        "pitch_type": p.get("pitchType", "Unknown"),
                        "edge_pct": p.get("edgePct", 0),
                        "zone_pct": p.get("zonePct", 0),
                        "meatball_pct": p.get("meatballPct", 0),
                        "called_strike_pct": p.get("calledStrikePct", 0)
                    }
                    for p in pitches
                ]
        except Exception as e:
            logger.error(f"Error parsing location command data: {e}")
        return None
    
    def _parse_specialized_pitch_data(self, data: Dict) -> Optional[Dict]:
        try:
            if data.get("stats") and data["stats"]:
                stats = data["stats"][0]
                return {
                    "ivb": stats.get("ivb", 0),
                    "ride_factor": stats.get("rideFactor", "Unknown"),
                    "hop_ratio": stats.get("hopRatio", 0),
                    "sweep": stats.get("sweep", 0),
                    "gyro_spin_factor": stats.get("gyroSpinFactor", "Unknown"),
                    "late_break": stats.get("lateBreak", 0),
                    "velocity_differential": stats.get("velocityDifferential", 0),
                    "arm_side_fade": stats.get("armSideFade", 0),
                    "drop_vs_fastball": stats.get("dropVsFastball", 0),
                    "arm_side_run": stats.get("armSideRun", 0),
                    "ivb_vs_fastball": stats.get("ivbVsFastball", 0),
                    "ground_ball_rate": stats.get("groundBallRate", 0),
                    "spin_efficiency": stats.get("spinEfficiency", 0),
                    "movement_vs_avg": stats.get("movementVsAvg", 0)
                }
        except Exception as e:
            logger.error(f"Error parsing specialized pitch data: {e}")
        return None
    
    def _parse_run_prevention_data(self, data: Dict) -> Optional[Dict]:
        try:
            if data.get("stats") and data["stats"]:
                stats = data["stats"][0]
                return {
                    "era": stats.get("era", 0.0),
                    "era_plus": stats.get("eraPlus", 100),
                    "fip": stats.get("fip", 0.0),
                    "xfip": stats.get("xfip", 0.0),
                    "siera": stats.get("siera", 0.0),
                    "k_percent": stats.get("kPercent", 0.0),
                    "bb_percent": stats.get("bbPercent", 0.0),
                    "k_bb_percent": stats.get("kBbPercent", 0.0),
                    "hr_per_9": stats.get("hrPer9", 0.0),
                    "babip": stats.get("babip", 0.0)
                }
        except Exception as e:
            logger.error(f"Error parsing run prevention data: {e}")
        return None
    
    def _parse_contact_quality_data(self, data: Dict) -> Optional[Dict]:
        try:
            if data.get("stats") and data["stats"]:
                stats = data["stats"][0]
                return {
                    "gb_percent": stats.get("gbPercent", 0.0),
                    "fb_percent": stats.get("fbPercent", 0.0),
                    "ld_percent": stats.get("ldPercent", 0.0),
                    "hr_fb_percent": stats.get("hrFbPercent", 0.0),
                    "hard_hit_percent": stats.get("hardHitPercent", 0.0),
                    "barrel_percent": stats.get("barrelPercent", 0.0),
                    "avg_exit_velocity": stats.get("avgExitVelocity", 0.0),
                    "launch_angle": stats.get("launchAngle", 0.0),
                    "xera": stats.get("xera", 0.0),
                    "xba": stats.get("xba", 0.0),
                    "xslg": stats.get("xslg", 0.0),
                    "xwoba": stats.get("xwoba", 0.0)
                }
        except Exception as e:
            logger.error(f"Error parsing contact quality data: {e}")
        return None
    
    def _parse_win_probability_data(self, data: Dict) -> Optional[Dict]:
        try:
            if data.get("stats") and data["stats"]:
                stats = data["stats"][0]
                return {
                    "war": stats.get("war", 0.0),
                    "wpa": stats.get("wpa", 0.0),
                    "re24": stats.get("re24", 0.0),
                    "gmli": stats.get("gmli", 0.0),
                    "shutdowns": stats.get("shutdowns", 0),
                    "meltdowns": stats.get("meltdowns", 0),
                    "high_leverage_ip": stats.get("highLeverageIp", 0.0),
                    "wpa_li": stats.get("wpaLi", 0.0),
                    "clutch": stats.get("clutch", 0.0)
                }
        except Exception as e:
            logger.error(f"Error parsing win probability data: {e}")
        return None
    
    def _parse_plate_discipline_data(self, data: Dict) -> Optional[Dict]:
        try:
            if data.get("stats") and data["stats"]:
                stats = data["stats"][0]
                return {
                    "o_swing_percent": stats.get("oSwingPercent", 0.0),
                    "z_swing_percent": stats.get("zSwingPercent", 0.0),
                    "swstr_percent": stats.get("swstrPercent", 0.0),
                    "csw_percent": stats.get("cswPercent", 0.0),
                    "contact_percent": stats.get("contactPercent", 0.0),
                    "first_pitch_strike_percent": stats.get("firstPitchStrikePercent", 0.0),
                    "zone_percent": stats.get("zonePercent", 0.0),
                    "o_contact_percent": stats.get("oContactPercent", 0.0),
                    "z_contact_percent": stats.get("zContactPercent", 0.0),
                    "chase_rate": stats.get("chaseRate", 0.0),
                    "whiff_rate": stats.get("whiffRate", 0.0),
                    "called_strike_rate": stats.get("calledStrikeRate", 0.0)
                }
        except Exception as e:
            logger.error(f"Error parsing plate discipline data: {e}")
        return None
    
    def _parse_spin_aerodynamics_data(self, data: Dict) -> Optional[Dict]:
        try:
            if data.get("stats") and data["stats"]:
                stats = data["stats"][0]
                return {
                    "ssw_factor": stats.get("sswFactor", 0.0),
                    "true_spin_axis": stats.get("trueSpinAxis", 0.0),
                    "observed_movement_axis": stats.get("observedMovementAxis", 0.0),
                    "ssw_discrepancy": stats.get("sswDiscrepancy", 0.0),
                    "expected_magnus": stats.get("expectedMagnus", 0.0),
                    "actual_movement": stats.get("actualMovement", 0.0),
                    "non_magnus_component": stats.get("nonMagnusComponent", 0.0),
                    "seam_effect_contribution": stats.get("seamEffectContribution", 0.0),
                    "spin_efficiency": stats.get("spinEfficiency", 0.0),
                    "gyro_spin_component": stats.get("gyroSpinComponent", 0.0),
                    "transverse_spin": stats.get("transverseSpin", 0.0),
                    "spin_based_movement": stats.get("spinBasedMovement", 0.0),
                    "seam_based_movement": stats.get("seamBasedMovement", 0.0)
                }
        except Exception as e:
            logger.error(f"Error parsing spin aerodynamics data: {e}")
        return None
    
    def _parse_biomechanics_release_data(self, data: Dict) -> Optional[Dict]:
        try:
            if data.get("stats") and data["stats"]:
                stats = data["stats"][0]
                return {
                    "extension": stats.get("extension", 0.0),
                    "release_height": stats.get("releaseHeight", 0.0),
                    "release_side": stats.get("releaseSide", 0.0),
                    "vertical_release_point": stats.get("verticalReleasePoint", 0.0),
                    "horizontal_release_point": stats.get("horizontalReleasePoint", 0.0),
                    "arm_slot": stats.get("armSlot", 0.0),
                    "stride_length": stats.get("strideLength", 0.0),
                    "hip_shoulder_separation": stats.get("hipShoulderSeparation", 0.0),
                    "front_leg_stability": stats.get("frontLegStability", 0.0),
                    "release_consistency": stats.get("releaseConsistency", 0.0),
                    "raw_velocity": stats.get("rawVelocity", 0.0),
                    "extension_boost": stats.get("extensionBoost", 0.0),
                    "perceived_velocity": stats.get("perceivedVelocity", 0.0),
                    "release_point_factor": stats.get("releasePointFactor", 0.0)
                }
        except Exception as e:
            logger.error(f"Error parsing biomechanics release data: {e}")
        return None
    
    def _parse_advanced_tunneling_data(self, data: Dict) -> Optional[Dict]:
        try:
            if data.get("stats") and data["stats"]:
                stats = data["stats"][0]
                return {
                    "release_distance": stats.get("releaseDistance", 0.0),
                    "release_point_variance": stats.get("releasePointVariance", 0.0),
                    "consistency_score": stats.get("consistencyScore", 0.0),
                    "tunnel_point": stats.get("tunnelPoint", 0.0),
                    "tunnel_distance": stats.get("tunnelDistance", 0.0),
                    "tunnel_differential": stats.get("tunnelDifferential", 0.0),
                    "plate_differential": stats.get("plateDifferential", 0.0),
                    "break_tunneling_ratio": stats.get("breakTunnelingRatio", 0.0),
                    "deception_score": stats.get("deceptionScore", 0.0),
                    "tunneling_efficiency": stats.get("tunnelingEfficiency", 0.0),
                    "late_break_factor": stats.get("lateBreakFactor", 0.0),
                    "fastball_tunneling": stats.get("fastballTunneling", 0.0),
                    "breaking_ball_tunneling": stats.get("breakingBallTunneling", 0.0),
                    "changeup_tunneling": stats.get("changeupTunneling", 0.0)
                }
        except Exception as e:
            logger.error(f"Error parsing advanced tunneling data: {e}")
        return None
    
    def _parse_deception_perceptual_data(self, data: Dict) -> Optional[Dict]:
        try:
            if data.get("stats") and data["stats"]:
                stats = data["stats"][0]
                return {
                    "raw_velocity": stats.get("rawVelocity", 0.0),
                    "effective_velocity": stats.get("effectiveVelocity", 0.0),
                    "location_adjustment": stats.get("locationAdjustment", 0.0),
                    "extension_adjustment": stats.get("extensionAdjustment", 0.0),
                    "perceived_velocity": stats.get("perceivedVelocity", 0.0),
                    "extension_boost": stats.get("extensionBoost", 0.0),
                    "release_point_factor": stats.get("releasePointFactor", 0.0),
                    "total_velocity_boost": stats.get("totalVelocityBoost", 0.0),
                    "time_to_plate": stats.get("timeToPlate", 0.0),
                    "reaction_window": stats.get("reactionWindow", 0.0),
                    "decision_point": stats.get("decisionPoint", 0.0),
                    "late_movement_window": stats.get("lateMovementWindow", 0.0),
                    "overall_deception_score": stats.get("overallDeceptionScore", 0.0),
                    "velocity_deception": stats.get("velocityDeception", 0.0),
                    "movement_deception": stats.get("movementDeception", 0.0),
                    "timing_deception": stats.get("timingDeception", 0.0)
                }
        except Exception as e:
            logger.error(f"Error parsing deception perceptual data: {e}")
        return None
    
    def _parse_pitch_shape_classification_data(self, data: Dict) -> Optional[Dict]:
        try:
            if data.get("stats") and data["stats"]:
                stats = data["stats"][0]
                return {
                    "primary_movement_pattern": stats.get("primaryMovementPattern", "Unknown"),
                    "secondary_movement": stats.get("secondaryMovement", "Unknown"),
                    "movement_cluster": stats.get("movementCluster", "Unknown"),
                    "shape_classification": stats.get("shapeClassification", "Unknown"),
                    "axis_tilt": stats.get("axisTilt", 0.0),
                    "tilt_clock": stats.get("tiltClock", "Unknown"),
                    "tilt_consistency": stats.get("tiltConsistency", 0.0),
                    "tilt_variance": stats.get("tiltVariance", 0.0),
                    "stuff_plus_score": stats.get("stuffPlusScore", 100.0),
                    "velocity_component": stats.get("velocityComponent", 0.0),
                    "movement_component": stats.get("movementComponent", 0.0),
                    "location_component": stats.get("locationComponent", 0.0),
                    "overall_stuff_grade": stats.get("overallStuffGrade", "B"),
                    "break_pattern": stats.get("breakPattern", "Unknown"),
                    "late_movement": stats.get("lateMovement", 0.0),
                    "movement_efficiency": stats.get("movementEfficiency", 0.0),
                    "shape_uniqueness": stats.get("shapeUniqueness", 0.0)
                }
        except Exception as e:
            logger.error(f"Error parsing pitch shape classification data: {e}")
        return None
    
    def _parse_contact_quality_by_pitch_data(self, data: Dict) -> Optional[Dict]:
        try:
            if data.get("stats") and data["stats"]:
                stats = data["stats"][0]
                return {
                    "fastball_launch_angle": stats.get("fastballLaunchAngle", 0.0),
                    "slider_launch_angle": stats.get("sliderLaunchAngle", 0.0),
                    "changeup_launch_angle": stats.get("changeupLaunchAngle", 0.0),
                    "curveball_launch_angle": stats.get("curveballLaunchAngle", 0.0),
                    "fastball_bat_speed_match": stats.get("fastballBatSpeedMatch", 0.0),
                    "slider_bat_speed_match": stats.get("sliderBatSpeedMatch", 0.0),
                    "changeup_bat_speed_match": stats.get("changeupBatSpeedMatch", 0.0),
                    "overall_bat_speed_exploitation": stats.get("overallBatSpeedExploitation", 0.0),
                    "high_fastball_xrv": stats.get("highFastballXrv", 0.0),
                    "low_slider_xrv": stats.get("lowSliderXrv", 0.0),
                    "outside_changeup_xrv": stats.get("outsideChangeupXrv", 0.0),
                    "inside_breaking_ball_xrv": stats.get("insideBreakingBallXrv", 0.0),
                    "weak_contact_rate": stats.get("weakContactRate", 0.0),
                    "medium_contact_rate": stats.get("mediumContactRate", 0.0),
                    "hard_contact_rate": stats.get("hardContactRate", 0.0),
                    "barrel_rate_by_pitch": stats.get("barrelRateByPitch", 0.0)
                }
        except Exception as e:
            logger.error(f"Error parsing contact quality by pitch data: {e}")
        return None
    
    def _parse_biomechanics_tech_data(self, data: Dict) -> Optional[Dict]:
        try:
            if data.get("stats") and data["stats"]:
                stats = data["stats"][0]
                return {
                    "hip_shoulder_separation": stats.get("hipShoulderSeparation", 0.0),
                    "separation_impact_on_spin": stats.get("separationImpactOnSpin", 0.0),
                    "front_leg_stability": stats.get("frontLegStability", 0.0),
                    "stability_impact_on_command": stats.get("stabilityImpactOnCommand", 0.0),
                    "rotation_order": stats.get("rotationOrder", "Unknown"),
                    "sequencing_efficiency": stats.get("sequencingEfficiency", 0.0),
                    "timing_consistency": stats.get("timingConsistency", 0.0),
                    "mechanical_repeatability": stats.get("mechanicalRepeatability", 0.0),
                    "seam_orientation": stats.get("seamOrientation", 0.0),
                    "grip_consistency": stats.get("gripConsistency", 0.0),
                    "seam_pressure_points": stats.get("seamPressurePoints", "Unknown"),
                    "grip_impact_on_movement": stats.get("gripImpactOnMovement", 0.0),
                    "arm_path_efficiency": stats.get("armPathEfficiency", 0.0),
                    "kinetic_chain_transfer": stats.get("kineticChainTransfer", 0.0),
                    "energy_transfer_efficiency": stats.get("energyTransferEfficiency", 0.0),
                    "overall_mechanical_grade": stats.get("overallMechanicalGrade", "B")
                }
        except Exception as e:
            logger.error(f"Error parsing biomechanics tech data: {e}")
        return None
    
    def _parse_batter_stats(self, data: Dict) -> Optional[Dict]:
        try:
            if data.get("stats") and data["stats"]:
                stats = data["stats"][0]
                return {
                    "avg": stats.get("avg", 0.0),
                    "obp": stats.get("obp", 0.0),
                    "slg": stats.get("slg", 0.0),
                    "ops": stats.get("ops", 0.0),
                    "home_runs": stats.get("homeRuns", 0),
                    "rbi": stats.get("rbi", 0),
                    "stolen_bases": stats.get("stolenBases", 0),
                    "walks": stats.get("baseOnBalls", 0),
                    "strikeouts": stats.get("strikeOuts", 0),
                    "woba": stats.get("woba", 0.0),
                    "wrc_plus": stats.get("wrcPlus", 0.0),
                    "iso": stats.get("iso", 0.0),
                    "babip": stats.get("babip", 0.0),
                    "k_percent": stats.get("kPercent", 0.0),
                    "bb_percent": stats.get("bbPercent", 0.0),
                    "k_bb_percent": stats.get("kbbPercent", 0.0)
                }
        except Exception as e:
            logger.error(f"Error parsing batter stats: {e}")
        return None
    
    def _parse_batter_contact_quality(self, data: Dict) -> Optional[Dict]:
        try:
            if data.get("stats") and data["stats"]:
                stats = data["stats"][0]
                return {
                    "avg_exit_velocity": stats.get("avgExitVelocity", 0.0),
                    "max_exit_velocity": stats.get("maxExitVelocity", 0.0),
                    "hard_hit_percent": stats.get("hardHitPercent", 0.0),
                    "avg_launch_angle": stats.get("avgLaunchAngle", 0.0),
                    "sweet_spot_percent": stats.get("sweetSpotPercent", 0.0),
                    "gb_percent": stats.get("gbPercent", 0.0),
                    "fb_percent": stats.get("fbPercent", 0.0),
                    "ld_percent": stats.get("ldPercent", 0.0),
                    "barrel_percent": stats.get("barrelPercent", 0.0),
                    "barrel_per_pa": stats.get("barrelPerPa", 0.0),
                    "avg_distance": stats.get("avgDistance", 0.0),
                    "xba": stats.get("xba", 0.0),
                    "xslg": stats.get("xslg", 0.0),
                    "xwoba": stats.get("xwoba", 0.0),
                    "xiso": stats.get("xiso", 0.0)
                }
        except Exception as e:
            logger.error(f"Error parsing batter contact quality: {e}")
        return None
    
    def _parse_batter_plate_discipline(self, data: Dict) -> Optional[Dict]:
        try:
            if data.get("stats") and data["stats"]:
                stats = data["stats"][0]
                return {
                    "o_swing_percent": stats.get("oSwingPercent", 0.0),
                    "z_swing_percent": stats.get("zSwingPercent", 0.0),
                    "swing_percent": stats.get("swingPercent", 0.0),
                    "contact_percent": stats.get("contactPercent", 0.0),
                    "o_contact_percent": stats.get("oContactPercent", 0.0),
                    "z_contact_percent": stats.get("zContactPercent", 0.0),
                    "swstr_percent": stats.get("swstrPercent", 0.0),
                    "csw_percent": stats.get("cswPercent", 0.0),
                    "k_percent": stats.get("kPercent", 0.0),
                    "zone_percent": stats.get("zonePercent", 0.0),
                    "first_pitch_strike_percent": stats.get("firstPitchStrikePercent", 0.0),
                    "chase_rate": stats.get("chaseRate", 0.0),
                    "whiff_rate": stats.get("whiffRate", 0.0)
                }
        except Exception as e:
            logger.error(f"Error parsing batter plate discipline: {e}")
        return None
    
    def _parse_batter_expected_outcomes(self, data: Dict) -> Optional[Dict]:
        try:
            if data.get("stats") and data["stats"]:
                stats = data["stats"][0]
                return {
                    "xba": stats.get("xba", 0.0),
                    "xslg": stats.get("xslg", 0.0),
                    "xwOBA": stats.get("xwoba", 0.0),
                    "xiso": stats.get("xiso", 0.0),
                    "run_value": stats.get("runValue", 0.0),
                    "run_value_per_100": stats.get("runValuePer100", 0.0),
                    "run_value_per_100_bbe": stats.get("runValuePer100Bbe", 0.0),
                    "hard_hit_percent": stats.get("hardHitPercent", 0.0),
                    "barrel_percent": stats.get("barrelPercent", 0.0),
                    "sweet_spot_percent": stats.get("sweetSpotPercent", 0.0),
                    "ba_vs_xba": stats.get("baVsXba", 0.0),
                    "slg_vs_xslg": stats.get("slgVsXslg", 0.0),
                    "woba_vs_xwoba": stats.get("wobaVsXwoba", 0.0)
                }
        except Exception as e:
            logger.error(f"Error parsing batter expected outcomes: {e}")
        return None
    
    def _parse_batter_batted_ball_profile(self, data: Dict) -> Optional[Dict]:
        try:
            if data.get("stats") and data["stats"]:
                stats = data["stats"][0]
                return {
                    "gb_percent": stats.get("gbPercent", 0.0),
                    "fb_percent": stats.get("fbPercent", 0.0),
                    "ld_percent": stats.get("ldPercent", 0.0),
                    "iffb_percent": stats.get("iffbPercent", 0.0),
                    "pull_percent": stats.get("pullPercent", 0.0),
                    "center_percent": stats.get("centerPercent", 0.0),
                    "oppo_percent": stats.get("oppoPercent", 0.0),
                    "hard_hit_percent": stats.get("hardHitPercent", 0.0),
                    "medium_hit_percent": stats.get("mediumHitPercent", 0.0),
                    "soft_hit_percent": stats.get("softHitPercent", 0.0),
                    "avg_launch_angle": stats.get("avgLaunchAngle", 0.0),
                    "sweet_spot_percent": stats.get("sweetSpotPercent", 0.0),
                    "under_percent": stats.get("underPercent", 0.0),
                    "topped_percent": stats.get("toppedPercent", 0.0)
                }
        except Exception as e:
            logger.error(f"Error parsing batter batted ball profile: {e}")
        return None
    
    def _parse_batter_speed_metrics(self, data: Dict) -> Optional[Dict]:
        try:
            if data.get("stats") and data["stats"]:
                stats = data["stats"][0]
                return {
                    "sprint_speed": stats.get("sprintSpeed", 0.0),
                    "sprint_speed_percentile": stats.get("sprintSpeedPercentile", 0.0),
                    "sb_success_rate": stats.get("sbSuccessRate", 0.0),
                    "baserunning_value": stats.get("baserunningValue", 0.0),
                    "baserunning_runs": stats.get("baserunningRuns", 0.0),
                    "first_to_third_rate": stats.get("firstToThirdRate", 0.0),
                    "home_to_first_time": stats.get("homeToFirstTime", 0.0),
                    "range_factor": stats.get("rangeFactor", 0.0),
                    "range_factor_per_9": stats.get("rangeFactorPer9", 0.0)
                }
        except Exception as e:
            logger.error(f"Error parsing batter speed metrics: {e}")
        return None
    
    def _parse_batter_clutch_performance(self, data: Dict) -> Optional[Dict]:
        try:
            if data.get("stats") and data["stats"]:
                stats = data["stats"][0]
                return {
                    "wpa": stats.get("wpa", 0.0),
                    "wpa_li": stats.get("wpaLi", 0.0),
                    "clutch": stats.get("clutch", 0.0),
                    "re24": stats.get("re24", 0.0),
                    "re24_per_pa": stats.get("re24PerPa", 0.0),
                    "high_leverage_wpa": stats.get("highLeverageWpa", 0.0),
                    "medium_leverage_wpa": stats.get("mediumLeverageWpa", 0.0),
                    "low_leverage_wpa": stats.get("lowLeverageWpa", 0.0),
                    "risp_avg": stats.get("rispAvg", 0.0),
                    "risp_ops": stats.get("rispOps", 0.0),
                    "late_close_wpa": stats.get("lateCloseWpa", 0.0)
                }
        except Exception as e:
            logger.error(f"Error parsing batter clutch performance: {e}")
        return None
    
    def _parse_pitcher_defensive_metrics(self, data: Dict) -> Optional[Dict]:
        try:
            if data.get("stats") and data["stats"]:
                stats = data["stats"][0]
                return {
                    "fielding_percentage": stats.get("fieldingPercentage", 0.0),
                    "errors": stats.get("errors", 0),
                    "assists": stats.get("assists", 0),
                    "putouts": stats.get("putouts", 0),
                    "range_factor": stats.get("rangeFactor", 0.0),
                    "range_factor_per_9": stats.get("rangeFactorPer9", 0.0),
                    "zone_rating": stats.get("zoneRating", 0.0),
                    "drs": stats.get("drs", 0.0),
                    "uzr": stats.get("uzr", 0.0),
                    "defensive_war": stats.get("defensiveWar", 0.0),
                    "pickoff_attempts": stats.get("pickoffAttempts", 0),
                    "pickoff_success_rate": stats.get("pickoffSuccessRate", 0.0),
                    "fip": stats.get("fip", 0.0)
                }
        except Exception as e:
            logger.error(f"Error parsing pitcher defensive metrics: {e}")
        return None
    
    def _parse_batter_defensive_metrics(self, data: Dict) -> Optional[Dict]:
        try:
            if data.get("stats") and data["stats"]:
                stats = data["stats"][0]
                return {
                    "fielding_percentage": stats.get("fieldingPercentage", 0.0),
                    "errors": stats.get("errors", 0),
                    "assists": stats.get("assists", 0),
                    "putouts": stats.get("putouts", 0),
                    "range_factor": stats.get("rangeFactor", 0.0),
                    "range_factor_per_9": stats.get("rangeFactorPer9", 0.0),
                    "zone_rating": stats.get("zoneRating", 0.0),
                    "drs": stats.get("drs", 0.0),
                    "uzr": stats.get("uzr", 0.0),
                    "defensive_war": stats.get("defensiveWar", 0.0),
                    "innings_played": stats.get("inningsPlayed", 0.0),
                    "games_started": stats.get("gamesStarted", 0),
                    "double_plays_turned": stats.get("doublePlaysTurned", 0),
                    "outfield_assists": stats.get("outfieldAssists", 0)
                }
        except Exception as e:
            logger.error(f"Error parsing batter defensive metrics: {e}")
        return None
    
    def _get_mock_pitch_quality_data(self, pitcher_name: str, season: str) -> List[Dict]:
        return [
            {"pitch_type": "Fastball", "velocity": 95.2, "spin_rate": 2450, "spin_axis": 12.5, "spin_efficiency": 0.92, "ivb": 15.2, "hb": 2.1, "movement_vs_avg": 2.3},
            {"pitch_type": "Fastball", "velocity": 94.8, "spin_rate": 2420, "spin_axis": 12.1, "spin_efficiency": 0.89, "ivb": 14.8, "hb": 1.9, "movement_vs_avg": 1.9},
            {"pitch_type": "Slider", "velocity": 87.3, "spin_rate": 2850, "spin_axis": 8.2, "spin_efficiency": 0.78, "ivb": -8.5, "hb": -3.2, "movement_vs_avg": -1.8},
            {"pitch_type": "Slider", "velocity": 86.9, "spin_rate": 2820, "spin_axis": 7.9, "spin_efficiency": 0.75, "ivb": -8.1, "hb": -2.8, "movement_vs_avg": -1.5},
            {"pitch_type": "Changeup", "velocity": 84.1, "spin_rate": 1850, "spin_axis": 6.5, "spin_efficiency": 0.85, "ivb": -12.3, "hb": 1.2, "movement_vs_avg": -0.8}
        ]
    
    def _get_mock_usage_tunneling_data(self, pitcher_name: str, season: str) -> List[Dict]:
        return [
            {"pitch_type": "Fastball", "usage_pct": 45.2, "release_point_x": -1.2, "release_point_z": 6.8, "tunneling_distance": 15.2, "tunneling_time": 0.245},
            {"pitch_type": "Fastball", "usage_pct": 45.2, "release_point_x": -1.1, "release_point_z": 6.9, "tunneling_distance": 15.1, "tunneling_time": 0.248},
            {"pitch_type": "Slider", "usage_pct": 32.1, "release_point_x": -1.2, "release_point_z": 6.8, "tunneling_distance": 12.8, "tunneling_time": 0.198},
            {"pitch_type": "Slider", "usage_pct": 32.1, "release_point_x": -1.1, "release_point_z": 6.9, "tunneling_distance": 12.9, "tunneling_time": 0.201},
            {"pitch_type": "Changeup", "usage_pct": 22.7, "release_point_x": -1.2, "release_point_z": 6.8, "tunneling_distance": 14.5, "tunneling_time": 0.235}
        ]
    
    def _get_mock_location_command_data(self, pitcher_name: str, season: str) -> List[Dict]:
        return [
            {"pitch_type": "Fastball", "edge_pct": 28.5, "zone_pct": 52.3, "meatball_pct": 8.2, "called_strike_pct": 18.9},
            {"pitch_type": "Fastball", "edge_pct": 28.5, "zone_pct": 52.3, "meatball_pct": 8.2, "called_strike_pct": 18.9},
            {"pitch_type": "Slider", "edge_pct": 35.2, "zone_pct": 45.8, "meatball_pct": 6.1, "called_strike_pct": 22.3},
            {"pitch_type": "Slider", "edge_pct": 35.2, "zone_pct": 45.8, "meatball_pct": 6.1, "called_strike_pct": 22.3},
            {"pitch_type": "Changeup", "edge_pct": 31.8, "zone_pct": 48.7, "meatball_pct": 7.5, "called_strike_pct": 19.8}
        ]
    
    def _get_mock_specialized_pitch_data(self, pitcher_name: str, season: str, pitch_type: str) -> Dict:
        if pitch_type.lower() == "fastball":
            return {
                "ivb": 15.2,
                "ride_factor": "High",
                "hop_ratio": 0.16,
                "spin_efficiency": 92.0,
                "movement_vs_avg": 2.3
            }
        elif pitch_type.lower() in ["slider", "curveball"]:
            return {
                "sweep": -3.2,
                "spin_efficiency": 78.0,
                "gyro_spin_factor": "Medium",
                "late_break": -2.1,
                "movement_vs_avg": -1.8
            }
        elif pitch_type.lower() == "changeup":
            return {
                "velocity_differential": 11.1,
                "arm_side_fade": 1.2,
                "drop_vs_fastball": -27.5,
                "spin_efficiency": 85.0,
                "movement_vs_avg": -0.8
            }
        elif pitch_type.lower() == "sinker":
            return {
                "arm_side_run": 2.8,
                "ivb_vs_fastball": -8.5,
                "ground_ball_rate": 68.5,
                "movement_vs_avg": 1.2
            }
        else:
            return {
                "spin_rate": 2500,
                "spin_efficiency": 85.0,
                "ivb": 8.5,
                "hb": 1.5,
                "movement_vs_avg": 0.5
            }
    
    def _get_mock_run_prevention_data(self, pitcher_name: str, season: str) -> Dict:
        return {
            "era": 3.45,
            "era_plus": 125,
            "fip": 3.52,
            "xfip": 3.48,
            "siera": 3.41,
            "k_percent": 28.5,
            "bb_percent": 6.8,
            "k_bb_percent": 21.7,
            "hr_per_9": 0.8,
            "babip": 0.285
        }
    
    def _get_mock_contact_quality_data(self, pitcher_name: str, season: str) -> Dict:
        return {
            "gb_percent": 45.2,
            "fb_percent": 32.1,
            "ld_percent": 22.7,
            "hr_fb_percent": 8.5,
            "hard_hit_percent": 35.2,
            "barrel_percent": 6.8,
            "avg_exit_velocity": 87.3,
            "launch_angle": 12.5,
            "xera": 3.38,
            "xba": 0.218,
            "xslg": 0.342,
            "xwoba": 0.298
        }
    
    def _get_mock_win_probability_data(self, pitcher_name: str, season: str) -> Dict:
        return {
            "war": 4.2,
            "wpa": 2.8,
            "re24": 18.5,
            "gmli": 1.2,
            "shutdowns": 8,
            "meltdowns": 2,
            "high_leverage_ip": 12.3,
            "wpa_li": 0.15,
            "clutch": 0.8
        }
    
    def _get_mock_plate_discipline_data(self, pitcher_name: str, season: str) -> Dict:
        return {
            "o_swing_percent": 32.1,
            "z_swing_percent": 65.4,
            "swstr_percent": 12.8,
            "csw_percent": 31.7,
            "contact_percent": 76.2,
            "first_pitch_strike_percent": 62.3,
            "zone_percent": 48.7,
            "o_contact_percent": 58.2,
            "z_contact_percent": 82.1,
            "chase_rate": 32.1,
            "whiff_rate": 28.5,
            "called_strike_rate": 18.9
        }
    
    def _get_mock_spin_aerodynamics_data(self, pitcher_name: str, season: str) -> Dict:
        return {
            "ssw_factor": 0.85,
            "true_spin_axis": 12.3,
            "observed_movement_axis": 15.7,
            "ssw_discrepancy": 3.4,
            "expected_magnus": 12.8,
            "actual_movement": 16.2,
            "non_magnus_component": 3.4,
            "seam_effect_contribution": 21.0,
            "spin_efficiency": 92.5,
            "gyro_spin_component": 7.5,
            "transverse_spin": 15.2,
            "spin_based_movement": 12.8,
            "seam_based_movement": 3.4
        }
    
    def _get_mock_biomechanics_release_data(self, pitcher_name: str, season: str) -> Dict:
        return {
            "extension": 6.8,
            "release_height": 6.2,
            "release_side": -1.2,
            "vertical_release_point": 6.2,
            "horizontal_release_point": -1.2,
            "arm_slot": 45.0,
            "stride_length": 7.2,
            "hip_shoulder_separation": 18.5,
            "front_leg_stability": 8.5,
            "release_consistency": 94.2,
            "raw_velocity": 94.8,
            "extension_boost": 1.2,
            "perceived_velocity": 96.0,
            "release_point_factor": 0.8
        }
    
    def _get_mock_advanced_tunneling_data(self, pitcher_name: str, season: str, pitch_comparison: str) -> Dict:
        return {
            "release_distance": 0.15,
            "release_point_variance": 0.08,
            "consistency_score": 92.5,
            "tunnel_point": 23.5,
            "tunnel_distance": 1.8,
            "tunnel_differential": 1.8,
            "plate_differential": 8.5,
            "break_tunneling_ratio": 4.72,
            "deception_score": 88.5,
            "tunneling_efficiency": 91.2,
            "late_break_factor": 2.1,
            "fastball_tunneling": 1.9,
            "breaking_ball_tunneling": 1.7,
            "changeup_tunneling": 2.2
        }
    
    def _get_mock_deception_perceptual_data(self, pitcher_name: str, season: str) -> Dict:
        return {
            "raw_velocity": 94.8,
            "effective_velocity": 96.2,
            "location_adjustment": 0.8,
            "extension_adjustment": 1.2,
            "perceived_velocity": 96.0,
            "extension_boost": 1.2,
            "release_point_factor": 0.8,
            "total_velocity_boost": 2.0,
            "time_to_plate": 425,
            "reaction_window": 180,
            "decision_point": 23.5,
            "late_movement_window": 245,
            "overall_deception_score": 87.5,
            "velocity_deception": 89.2,
            "movement_deception": 85.8,
            "timing_deception": 87.5
        }
    
    def _get_mock_pitch_shape_classification_data(self, pitcher_name: str, season: str) -> Dict:
        return {
            "primary_movement_pattern": "Rising Fastball",
            "secondary_movement": "Arm-Side Run",
            "movement_cluster": "High-IVB Fastball",
            "shape_classification": "Rising Heater",
            "axis_tilt": 12.3,
            "tilt_clock": "2:30",
            "tilt_consistency": 94.5,
            "tilt_variance": 2.1,
            "stuff_plus_score": 125.8,
            "velocity_component": 135.2,
            "movement_component": 118.7,
            "location_component": 123.1,
            "overall_stuff_grade": "A",
            "break_pattern": "Late Rise",
            "late_movement": 1.8,
            "movement_efficiency": 92.5,
            "shape_uniqueness": 87.3
        }
    
    def _get_mock_contact_quality_by_pitch_data(self, pitcher_name: str, season: str) -> Dict:
        return {
            "fastball_launch_angle": 18.5,
            "slider_launch_angle": 8.2,
            "changeup_launch_angle": 12.7,
            "curveball_launch_angle": 6.8,
            "fastball_bat_speed_match": 78.5,
            "slider_bat_speed_match": 82.3,
            "changeup_bat_speed_match": 75.8,
            "overall_bat_speed_exploitation": 79.2,
            "high_fastball_xrv": -0.12,
            "low_slider_xrv": -0.08,
            "outside_changeup_xrv": -0.15,
            "inside_breaking_ball_xrv": -0.22,
            "weak_contact_rate": 42.5,
            "medium_contact_rate": 38.7,
            "hard_contact_rate": 18.8,
            "barrel_rate_by_pitch": 6.8
        }
    
    def _get_mock_biomechanics_tech_data(self, pitcher_name: str, season: str) -> Dict:
        return {
            "hip_shoulder_separation": 18.5,
            "separation_impact_on_spin": 12.8,
            "front_leg_stability": 8.5,
            "stability_impact_on_command": 15.2,
            "rotation_order": "Hips-Shoulders-Arm",
            "sequencing_efficiency": 91.8,
            "timing_consistency": 94.2,
            "mechanical_repeatability": 92.7,
            "seam_orientation": 12.3,
            "grip_consistency": 96.5,
            "seam_pressure_points": "Index-Middle",
            "grip_impact_on_movement": 18.8,
            "arm_path_efficiency": 89.2,
            "kinetic_chain_transfer": 92.8,
            "energy_transfer_efficiency": 90.5,
            "overall_mechanical_grade": "A-"
        }
    
    def _get_mock_batter_stats(self, batter_name: str, season: str) -> Dict:
        return {
            "avg": 0.285,
            "obp": 0.365,
            "slg": 0.485,
            "ops": 0.850,
            "home_runs": 25,
            "rbi": 85,
            "stolen_bases": 15,
            "walks": 65,
            "strikeouts": 120,
            "woba": 0.365,
            "wrc_plus": 125,
            "iso": 0.200,
            "babip": 0.315,
            "k_percent": 22.5,
            "bb_percent": 12.1,
            "k_bb_percent": -10.4
        }
    
    def _get_mock_batter_contact_quality(self, batter_name: str, season: str) -> Dict:
        return {
            "avg_exit_velocity": 89.2,
            "max_exit_velocity": 112.5,
            "hard_hit_percent": 42.3,
            "avg_launch_angle": 15.8,
            "sweet_spot_percent": 32.1,
            "gb_percent": 38.5,
            "fb_percent": 35.2,
            "ld_percent": 26.3,
            "barrel_percent": 8.7,
            "barrel_per_pa": 0.065,
            "avg_distance": 285.3,
            "xba": 0.292,
            "xslg": 0.478,
            "xwoba": 0.358,
            "xiso": 0.186
        }
    
    def _get_mock_batter_plate_discipline(self, batter_name: str, season: str) -> Dict:
        return {
            "o_swing_percent": 28.5,
            "z_swing_percent": 68.2,
            "swing_percent": 48.7,
            "contact_percent": 78.9,
            "o_contact_percent": 62.3,
            "z_contact_percent": 85.6,
            "swstr_percent": 10.2,
            "csw_percent": 29.8,
            "k_percent": 22.5,
            "zone_percent": 45.2,
            "first_pitch_strike_percent": 58.7,
            "chase_rate": 28.5,
            "whiff_rate": 21.3
        }
    
    def _get_mock_batter_expected_outcomes(self, batter_name: str, season: str) -> Dict:
        return {
            "xba": 0.292,
            "xslg": 0.478,
            "xwOBA": 0.358,
            "xiso": 0.186,
            "run_value": 15.8,
            "run_value_per_100": 2.3,
            "run_value_per_100_bbe": 3.1,
            "hard_hit_percent": 42.3,
            "barrel_percent": 8.7,
            "sweet_spot_percent": 32.1,
            "ba_vs_xba": -0.007,
            "slg_vs_xslg": 0.007,
            "woba_vs_xwoba": 0.007
        }
    
    def _get_mock_batter_batted_ball_profile(self, batter_name: str, season: str) -> Dict:
        return {
            "gb_percent": 38.5,
            "fb_percent": 35.2,
            "ld_percent": 26.3,
            "iffb_percent": 8.2,
            "pull_percent": 42.1,
            "center_percent": 35.8,
            "oppo_percent": 22.1,
            "hard_hit_percent": 42.3,
            "medium_hit_percent": 45.2,
            "soft_hit_percent": 12.5,
            "avg_launch_angle": 15.8,
            "sweet_spot_percent": 32.1,
            "under_percent": 28.5,
            "topped_percent": 15.2
        }
    
    def _get_mock_batter_speed_metrics(self, batter_name: str, season: str) -> Dict:
        return {
            "sprint_speed": 27.8,
            "sprint_speed_percentile": 75,
            "sb_success_rate": 83.3,
            "baserunning_value": 2.1,
            "baserunning_runs": 3.2,
            "first_to_third_rate": 65.2,
            "home_to_first_time": 4.2,
            "range_factor": 2.15,
            "range_factor_per_9": 2.12
        }
    
    def _get_mock_batter_clutch_performance(self, batter_name: str, season: str) -> Dict:
        return {
            "wpa": 2.8,
            "wpa_li": 0.15,
            "clutch": 0.8,
            "re24": 18.5,
            "re24_per_pa": 0.027,
            "high_leverage_wpa": 1.2,
            "medium_leverage_wpa": 0.9,
            "low_leverage_wpa": 0.7,
            "risp_avg": 0.298,
            "risp_ops": 0.865,
            "late_close_wpa": 0.8
        }
    
    def _get_mock_pitcher_defensive_metrics(self, pitcher_name: str, season: str) -> Dict:
        return {
            "fielding_percentage": 98.5,
            "errors": 2,
            "assists": 15,
            "putouts": 8,
            "range_factor": 1.28,
            "range_factor_per_9": 1.25,
            "zone_rating": 0.85,
            "drs": 2,
            "uzr": 1.8,
            "defensive_war": 0.3,
            "pickoff_attempts": 12,
            "pickoff_success_rate": 25.0,
            "fip": 3.52
        }
    
    def _get_mock_batter_defensive_metrics(self, batter_name: str, season: str, position: str = "all") -> Dict:
        return {
            "fielding_percentage": 98.2,
            "errors": 8,
            "assists": 125,
            "putouts": 95,
            "range_factor": 2.15,
            "range_factor_per_9": 2.12,
            "zone_rating": 0.78,
            "drs": 5,
            "uzr": 4.2,
            "defensive_war": 0.8,
            "innings_played": 1350.2,
            "games_started": 145,
            "double_plays_turned": 45,
            "outfield_assists": 12 if position in ['lf', 'cf', 'rf'] else 0
        }
    
    async def get_batter_basic_stats(self, arguments: Dict[str, Any]) -> List[TextContent]:
        batter_name = arguments.get("batter_name")
        season = arguments.get("season", "2024")
        
        stats = await self._fetch_batter_stats(batter_name, season)
        
        if not stats:
            return [TextContent(type="text", text=f"No stats found for {batter_name} in {season}")]
        
        summary = f"""
**{batter_name} - {season} Season Basic Stats**

**Traditional Stats:**
- AVG: {stats.get('avg', 'N/A')}
- OBP: {stats.get('obp', 'N/A')}
- SLG: {stats.get('slg', 'N/A')}
- OPS: {stats.get('ops', 'N/A')}
- HR: {stats.get('home_runs', 'N/A')}
- RBI: {stats.get('rbi', 'N/A')}
- SB: {stats.get('stolen_bases', 'N/A')}
- BB: {stats.get('walks', 'N/A')}
- SO: {stats.get('strikeouts', 'N/A')}

**Advanced Stats:**
- wOBA: {stats.get('woba', 'N/A')}
- wRC+: {stats.get('wrc_plus', 'N/A')}
- ISO: {stats.get('iso', 'N/A')}
- BABIP: {stats.get('babip', 'N/A')}
- K%: {stats.get('k_percent', 'N/A')}
- BB%: {stats.get('bb_percent', 'N/A')}
- K-BB%: {stats.get('k_bb_percent', 'N/A')}
"""
        return [TextContent(type="text", text=summary)]
    
    async def get_batter_contact_quality(self, arguments: Dict[str, Any]) -> List[TextContent]:
        batter_name = arguments.get("batter_name")
        season = arguments.get("season", "2024")
        metric_type = arguments.get("metric_type", "all")
        
        stats = await self._fetch_batter_contact_quality(batter_name, season)
        
        if not stats:
            return [TextContent(type="text", text=f"No contact quality data found for {batter_name} in {season}")]
        
        summary = f"""
**{batter_name} - {season} Contact Quality Metrics (Statcast Core)**

**Exit Velocity:**
- Average Exit Velocity: {stats.get('avg_exit_velocity', 'N/A')} mph
- Max Exit Velocity: {stats.get('max_exit_velocity', 'N/A')} mph
- Hard Hit% (≥95 mph): {stats.get('hard_hit_percent', 'N/A')}%

**Launch Angle:**
- Average Launch Angle: {stats.get('avg_launch_angle', 'N/A')}°
- Sweet Spot% (8-32°): {stats.get('sweet_spot_percent', 'N/A')}%
- Ground Ball%: {stats.get('gb_percent', 'N/A')}%
- Fly Ball%: {stats.get('fb_percent', 'N/A')}%
- Line Drive%: {stats.get('ld_percent', 'N/A')}%

**Barrel Metrics:**
- Barrel%: {stats.get('barrel_percent', 'N/A')}%
- Barrel/PA: {stats.get('barrel_per_pa', 'N/A')}
- Average Distance: {stats.get('avg_distance', 'N/A')} ft

**Expected Outcomes:**
- xBA: {stats.get('xba', 'N/A')}
- xSLG: {stats.get('xslg', 'N/A')}
- xwOBA: {stats.get('xwoba', 'N/A')}
- xISO: {stats.get('xiso', 'N/A')}
"""
        return [TextContent(type="text", text=summary)]
    
    async def get_batter_plate_discipline(self, arguments: Dict[str, Any]) -> List[TextContent]:
        batter_name = arguments.get("batter_name")
        season = arguments.get("season", "2024")
        
        stats = await self._fetch_batter_plate_discipline(batter_name, season)
        
        if not stats:
            return [TextContent(type="text", text=f"No plate discipline data found for {batter_name} in {season}")]
        
        summary = f"""
**{batter_name} - {season} Plate Discipline Metrics**

**Swing Rates:**
- O-Swing% (Out of Zone): {stats.get('o_swing_percent', 'N/A')}%
- Z-Swing% (In Zone): {stats.get('z_swing_percent', 'N/A')}%
- Overall Swing%: {stats.get('swing_percent', 'N/A')}%

**Contact Rates:**
- Contact%: {stats.get('contact_percent', 'N/A')}%
- O-Contact% (Out of Zone): {stats.get('o_contact_percent', 'N/A')}%
- Z-Contact% (In Zone): {stats.get('z_contact_percent', 'N/A')}%

**Strikeout Metrics:**
- SwStr% (Swinging Strikes): {stats.get('swstr_percent', 'N/A')}%
- CSW% (Called + Swinging Strikes): {stats.get('csw_percent', 'N/A')}%
- K%: {stats.get('k_percent', 'N/A')}%

**Zone Control:**
- Zone%: {stats.get('zone_percent', 'N/A')}%
- First Pitch Strike%: {stats.get('first_pitch_strike_percent', 'N/A')}%
- Chase Rate: {stats.get('chase_rate', 'N/A')}%
- Whiff Rate: {stats.get('whiff_rate', 'N/A')}%
"""
        return [TextContent(type="text", text=summary)]
    
    async def get_batter_expected_outcomes(self, arguments: Dict[str, Any]) -> List[TextContent]:
        batter_name = arguments.get("batter_name")
        season = arguments.get("season", "2024")
        
        stats = await self._fetch_batter_expected_outcomes(batter_name, season)
        
        if not stats:
            return [TextContent(type="text", text=f"No expected outcome data found for {batter_name} in {season}")]
        
        summary = f"""
**{batter_name} - {season} Expected Outcome Metrics**

**Expected Batting Stats:**
- xBA (Expected Batting Average): {stats.get('xba', 'N/A')}
- xSLG (Expected Slugging): {stats.get('xslg', 'N/A')}
- xwOBA (Expected wOBA): {stats.get('xwOBA', 'N/A')}
- xISO (Expected ISO): {stats.get('xiso', 'N/A')}

**Run Value:**
- Run Value: {stats.get('run_value', 'N/A')}
- Run Value per 100 PA: {stats.get('run_value_per_100', 'N/A')}
- Run Value per 100 BBE: {stats.get('run_value_per_100_bbe', 'N/A')}

**Quality of Contact:**
- Hard Hit%: {stats.get('hard_hit_percent', 'N/A')}%
- Barrel%: {stats.get('barrel_percent', 'N/A')}%
- Sweet Spot%: {stats.get('sweet_spot_percent', 'N/A')}%

**Performance vs Expected:**
- BA vs xBA: {stats.get('ba_vs_xba', 'N/A')}
- SLG vs xSLG: {stats.get('slg_vs_xslg', 'N/A')}
- wOBA vs xwOBA: {stats.get('woba_vs_xwoba', 'N/A')}
"""
        return [TextContent(type="text", text=summary)]
    
    async def get_batter_batted_ball_profile(self, arguments: Dict[str, Any]) -> List[TextContent]:
        batter_name = arguments.get("batter_name")
        season = arguments.get("season", "2024")
        
        stats = await self._fetch_batter_batted_ball_profile(batter_name, season)
        
        if not stats:
            return [TextContent(type="text", text=f"No batted ball profile data found for {batter_name} in {season}")]
        
        summary = f"""
**{batter_name} - {season} Batted Ball Profile**

**Batted Ball Types:**
- Ground Ball%: {stats.get('gb_percent', 'N/A')}%
- Fly Ball%: {stats.get('fb_percent', 'N/A')}%
- Line Drive%: {stats.get('ld_percent', 'N/A')}%
- Infield Fly Ball%: {stats.get('iffb_percent', 'N/A')}%

**Spray Chart Distribution:**
- Pull%: {stats.get('pull_percent', 'N/A')}%
- Center%: {stats.get('center_percent', 'N/A')}%
- Opposite%: {stats.get('oppo_percent', 'N/A')}%

**Contact Quality:**
- Hard Hit%: {stats.get('hard_hit_percent', 'N/A')}%
- Medium Hit%: {stats.get('medium_hit_percent', 'N/A')}%
- Soft Hit%: {stats.get('soft_hit_percent', 'N/A')}%

**Launch Characteristics:**
- Average Launch Angle: {stats.get('avg_launch_angle', 'N/A')}°
- Sweet Spot%: {stats.get('sweet_spot_percent', 'N/A')}%
- Under%: {stats.get('under_percent', 'N/A')}%
- Topped%: {stats.get('topped_percent', 'N/A')}%
"""
        return [TextContent(type="text", text=summary)]
    
    async def get_batter_speed_metrics(self, arguments: Dict[str, Any]) -> List[TextContent]:
        batter_name = arguments.get("batter_name")
        season = arguments.get("season", "2024")
        
        stats = await self._fetch_batter_speed_metrics(batter_name, season)
        
        if not stats:
            return [TextContent(type="text", text=f"No speed metrics found for {batter_name} in {season}")]
        
        summary = f"""
**{batter_name} - {season} Speed & Baserunning Metrics**

**Sprint Speed:**
- Sprint Speed: {stats.get('sprint_speed', 'N/A')} ft/s
- Sprint Speed Percentile: {stats.get('sprint_speed_percentile', 'N/A')}%

**Baserunning:**
- Stolen Base Success Rate: {stats.get('sb_success_rate', 'N/A')}%
- Baserunning Value: {stats.get('baserunning_value', 'N/A')}
- Baserunning Runs: {stats.get('baserunning_runs', 'N/A')}

**First to Third:**
- First to Third Rate: {stats.get('first_to_third_rate', 'N/A')}%
- Home to First Time: {stats.get('home_to_first_time', 'N/A')}s

**Defensive Range:**
- Range Factor: {stats.get('range_factor', 'N/A')}
- Range Factor per 9: {stats.get('range_factor_per_9', 'N/A')}
"""
        return [TextContent(type="text", text=summary)]
    
    async def get_batter_clutch_performance(self, arguments: Dict[str, Any]) -> List[TextContent]:
        batter_name = arguments.get("batter_name")
        season = arguments.get("season", "2024")
        
        stats = await self._fetch_batter_clutch_performance(batter_name, season)
        
        if not stats:
            return [TextContent(type="text", text=f"No clutch performance data found for {batter_name} in {season}")]
        
        summary = f"""
**{batter_name} - {season} Clutch Performance Metrics**

**Win Probability:**
- WPA (Win Probability Added): {stats.get('wpa', 'N/A')}
- WPA/LI: {stats.get('wpa_li', 'N/A')}
- Clutch: {stats.get('clutch', 'N/A')}

**Run Expectancy:**
- RE24 (Run Expectancy 24): {stats.get('re24', 'N/A')}
- RE24/PA: {stats.get('re24_per_pa', 'N/A')}

**Leverage Performance:**
- High Leverage WPA: {stats.get('high_leverage_wpa', 'N/A')}
- Medium Leverage WPA: {stats.get('medium_leverage_wpa', 'N/A')}
- Low Leverage WPA: {stats.get('low_leverage_wpa', 'N/A')}

**Situational Performance:**
- RISP AVG: {stats.get('risp_avg', 'N/A')}
- RISP OPS: {stats.get('risp_ops', 'N/A')}
- Late & Close WPA: {stats.get('late_close_wpa', 'N/A')}
"""
        return [TextContent(type="text", text=summary)]
    
    async def get_pitcher_defensive_metrics(self, arguments: Dict[str, Any]) -> List[TextContent]:
        pitcher_name = arguments.get("pitcher_name")
        season = arguments.get("season", "2024")
        
        stats = await self._fetch_pitcher_defensive_metrics(pitcher_name, season)
        
        if not stats:
            return [TextContent(type="text", text=f"No defensive metrics found for {pitcher_name} in {season}")]
        
        summary = f"""
**{pitcher_name} - {season} Defensive Metrics**

**Fielding:**
- Fielding Percentage: {stats.get('fielding_percentage', 'N/A')}%
- Errors: {stats.get('errors', 'N/A')}
- Assists: {stats.get('assists', 'N/A')}
- Putouts: {stats.get('putouts', 'N/A')}

**Range & Positioning:**
- Range Factor: {stats.get('range_factor', 'N/A')}
- Range Factor per 9: {stats.get('range_factor_per_9', 'N/A')}
- Zone Rating: {stats.get('zone_rating', 'N/A')}

**Advanced Defensive Metrics:**
- Defensive Runs Saved (DRS): {stats.get('drs', 'N/A')}
- Ultimate Zone Rating (UZR): {stats.get('uzr', 'N/A')}
- Defensive WAR: {stats.get('defensive_war', 'N/A')}

**Pitcher-Specific Defense:**
- Pickoff Attempts: {stats.get('pickoff_attempts', 'N/A')}
- Pickoff Success Rate: {stats.get('pickoff_success_rate', 'N/A')}%
- Fielding Independent Pitching (FIP): {stats.get('fip', 'N/A')}
"""
        return [TextContent(type="text", text=summary)]
    
    async def get_batter_defensive_metrics(self, arguments: Dict[str, Any]) -> List[TextContent]:
        batter_name = arguments.get("batter_name")
        season = arguments.get("season", "2024")
        position = arguments.get("position", "all")
        
        stats = await self._fetch_batter_defensive_metrics(batter_name, season, position)
        
        if not stats:
            return [TextContent(type="text", text=f"No defensive metrics found for {batter_name} in {season}")]
        
        summary = f"""
**{batter_name} - {season} Defensive Metrics ({position.upper() if position != 'all' else 'All Positions'})**

**Fielding:**
- Fielding Percentage: {stats.get('fielding_percentage', 'N/A')}%
- Errors: {stats.get('errors', 'N/A')}
- Assists: {stats.get('assists', 'N/A')}
- Putouts: {stats.get('putouts', 'N/A')}

**Range & Positioning:**
- Range Factor: {stats.get('range_factor', 'N/A')}
- Range Factor per 9: {stats.get('range_factor_per_9', 'N/A')}
- Zone Rating: {stats.get('zone_rating', 'N/A')}

**Advanced Defensive Metrics:**
- Defensive Runs Saved (DRS): {stats.get('drs', 'N/A')}
- Ultimate Zone Rating (UZR): {stats.get('uzr', 'N/A')}
- Defensive WAR: {stats.get('defensive_war', 'N/A')}

**Position-Specific Metrics:**
- Innings Played: {stats.get('innings_played', 'N/A')}
- Games Started: {stats.get('games_started', 'N/A')}
- Double Plays Turned: {stats.get('double_plays_turned', 'N/A')}
- Outfield Assists: {stats.get('outfield_assists', 'N/A') if position in ['lf', 'cf', 'rf'] else 'N/A'}
"""
        return [TextContent(type="text", text=summary)]
    
    async def get_defensive_comparison(self, arguments: Dict[str, Any]) -> List[TextContent]:
        player_names = arguments.get("player_names", [])
        season = arguments.get("season", "2024")
        position = arguments.get("position", "all")
        
        if len(player_names) < 2:
            return [TextContent(type="text", text="Please provide at least 2 player names to compare")]
        
        comparison_data = []
        for player_name in player_names:
            if "pitcher" in arguments.get("player_type", "").lower():
                stats = await self._fetch_pitcher_defensive_metrics(player_name, season)
            else:
                stats = await self._fetch_batter_defensive_metrics(player_name, season, position)
            
            if stats:
                comparison_data.append((player_name, stats))
        
        if not comparison_data:
            return [TextContent(type="text", text="No defensive data found for the specified players")]
        
        summary = f"**Defensive Comparison - {season} Season**\n\n"
        
        for player_name, stats in comparison_data:
            summary += f"**{player_name}**\n"
            summary += f"- Fielding %: {stats.get('fielding_percentage', 'N/A')}%\n"
            summary += f"- DRS: {stats.get('drs', 'N/A')}\n"
            summary += f"- UZR: {stats.get('uzr', 'N/A')}\n"
            summary += f"- Range Factor: {stats.get('range_factor', 'N/A')}\n\n"
        
        return [TextContent(type="text", text=summary)]
    
    async def run(self):
        try:
            print("Starting MCP server...", file=sys.stderr)
            async with stdio_server() as (read_stream, write_stream):
                print("Stdio server started successfully", file=sys.stderr)
                await self.server.run(
                    read_stream,
                    write_stream,
                    InitializationOptions(
                        server_name="baseball-stats-mcp",
                        server_version="1.0.0",
                        capabilities=ServerCapabilities(
                            tools=ToolsCapability(listChanged=False)
                        ),
                    ),
                )
        except Exception as e:
            print(f"Error in MCP server: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)
            raise

async def async_main():
    server = BaseballStatsMCPServer()
    await server.run()

def main():
    """Entry point for console script"""
    asyncio.run(async_main())

if __name__ == "__main__":
    main()
