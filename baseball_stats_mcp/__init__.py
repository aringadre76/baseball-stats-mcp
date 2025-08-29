"""
Baseball Stats MCP Server
========================

The most comprehensive baseball analytics platform ever created, providing access to 
every advanced baseball metric available through a powerful MCP (Model Context Protocol) server.

Features:
- 32 comprehensive tools covering every aspect of baseball analysis
- Complete metric coverage from basic stats to cutting-edge Statcast analytics
- Real-time data integration with MLB API and Statcast
- Interactive visualizations using Plotly charts
- Professional-grade analytics used by MLB teams and analysts

Usage:
    from baseball_stats_mcp.server import BaseballStatsMCPServer
    
    server = BaseballStatsMCPServer()
    # Use with MCP client or run standalone
"""

__version__ = "1.0.1"
__author__ = "Arin Gadre"
__email__ = "aringadre76@gmail.com"

from .server import BaseballStatsMCPServer

__all__ = ["BaseballStatsMCPServer"]
