#!/usr/bin/env python3

import asyncio
import json
from server import BaseballStatsMCPServer

async def demo_visualizations():
    server = BaseballStatsMCPServer()
    
    print("Baseball Stats MCP Server - Visualization Demo\n")
    
    demo_pitchers = ["Jacob deGrom", "Gerrit Cole", "Max Scherzer"]
    chart_types = ["movement", "velocity", "location", "heatmap"]
    
    for pitcher in demo_pitchers:
        print(f"=== Generating Charts for {pitcher} ===\n")
        
        for chart_type in chart_types:
            print(f"Creating {chart_type} chart...")
            try:
                result = await server.generate_pitch_plot({
                    "pitcher_name": pitcher,
                    "chart_type": chart_type,
                    "season": "2024"
                })
                
                print(f"✓ {chart_type.title()} chart generated successfully")
                print(f"  Chart info: {result[0].text}")
                
                if len(result) > 1 and hasattr(result[1], 'text'):
                    html_content = result[1].text
                    print(f"  HTML content length: {len(html_content)} characters")
                    print(f"  Preview: {html_content[:100]}...")
                
                print()
                
            except Exception as e:
                print(f"✗ Error generating {chart_type} chart: {e}\n")
        
        print("="*60 + "\n")
    
    print("Visualization demo completed!")
    print("\nNote: The generated charts are in HTML format and can be:")
    print("- Saved to .html files for viewing in browsers")
    print("- Embedded in web applications")
    print("- Converted to static images using headless browsers")
    print("- Integrated into Jupyter notebooks")

if __name__ == "__main__":
    asyncio.run(demo_visualizations())
