#!/usr/bin/env python3

import asyncio
import sys
import os

def main():
    print("Baseball Stats MCP Server")
    print("=" * 40)
    
    try:
        from server import BaseballStatsMCPServer
        
        print("✓ Server imported successfully")
        print("✓ Dependencies loaded")
        print("✓ Ready to start MCP server")
        print("\nStarting server...")
        print("Note: This server is designed to run as an MCP server.")
        print("For testing, use: python3 test_server.py")
        print("For demos, use: python3 demo_visualizations.py")
        
        server = BaseballStatsMCPServer()
        asyncio.run(server.run())
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("Make sure all dependencies are installed:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
