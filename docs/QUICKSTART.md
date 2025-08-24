# Baseball Stats MCP Server - Quick Start Guide

Get up and running with the most comprehensive baseball analytics platform in minutes!

## 🚀 **Prerequisites**

- **Python 3.8+** installed on your system
- **Git** for cloning the repository
- **MCP Client** (e.g., Claude Desktop) for integration

## 📥 **Installation**

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd baseball-stats-mcp
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables (Optional)
```bash
# For enhanced functionality
export FIRECRAWL_TOKEN="your_firecrawl_token"
export BASEBALL_API_KEY="your_mlb_api_key"
```

## 🧪 **Quick Test**

Verify everything is working by running the test suite:

```bash
cd tests
python3 run_all_tests.py --basic
```

You should see: **36 tests passed, 0 failed (100% success rate)**

## 🖥️ **Running the Server**

### Start the MCP Server
```bash
cd src
python3 run_server.py
```

The server will start and display connection information.

### Test Individual Tools
```bash
# Test basic functionality
python3 demo_visualizations.py
```

## 🔧 **MCP Client Integration**

### Claude Desktop Configuration
1. Open Claude Desktop
2. Go to Settings → MCP Servers
3. Add new server with configuration from `mcp_config.json`
4. Restart Claude Desktop

### Other MCP Clients
The server follows the standard MCP protocol and should work with any compliant client.

## 📊 **First Steps**

### 1. Basic Pitcher Analysis
```python
# Get comprehensive stats for Logan Webb
pitcher_stats = await get_pitcher_basic_stats({
    "pitcher_name": "Logan Webb", 
    "season": "2024"
})
```

### 2. Pitch Breakdown
```python
# Analyze pitch characteristics
pitch_breakdown = await get_pitch_breakdown({
    "pitcher_name": "Logan Webb", 
    "season": "2024"
})
```

### 3. Generate Visualizations
```python
# Create movement chart
movement_chart = await generate_pitch_plot({
    "pitcher_name": "Logan Webb", 
    "chart_type": "movement", 
    "season": "2024"
})
```

## 🎯 **Example Workflows**

### **Complete Pitcher Analysis**
```python
# 1. Get basic stats
basic_stats = await get_pitcher_basic_stats({
    "pitcher_name": "Logan Webb", 
    "season": "2024"
})

# 2. Analyze pitch quality
pitch_quality = await get_pitch_quality_metrics({
    "pitcher_name": "Logan Webb", 
    "season": "2024"
})

# 3. Check efficiency
efficiency = await get_pitch_efficiency_metrics({
    "pitcher_name": "Logan Webb", 
    "season": "2024"
})

# 4. Generate visualization
chart = await generate_pitch_plot({
    "pitcher_name": "Logan Webb", 
    "chart_type": "movement", 
    "season": "2024"
})
```

### **Batter Analysis**
```python
# Analyze Aaron Judge's performance
batter_stats = await get_batter_basic_stats({
    "batter_name": "Aaron Judge", 
    "season": "2024"
})

contact_quality = await get_batter_contact_quality({
    "batter_name": "Aaron Judge", 
    "season": "2024"
})
```

## 🔍 **Available Tools Overview**

### **Pitching Analysis (18 tools)**
- `get_pitcher_basic_stats` - Traditional metrics
- `get_pitch_breakdown` - Pitch characteristics
- `get_pitch_efficiency_metrics` - Advanced efficiency
- `get_pitch_quality_metrics` - Movement and spin
- `get_pitch_usage_tunneling` - Usage patterns
- `get_pitch_location_command` - Command metrics
- `get_specialized_pitch_analysis` - Pitch-specific analysis
- `get_run_prevention_metrics` - ERA alternatives
- `get_contact_quality_metrics` - Contact control
- `get_win_probability_metrics` - Value metrics
- `get_plate_discipline_metrics` - Zone control
- `get_spin_aerodynamics_metrics` - Advanced spin
- `get_biomechanics_release_metrics` - Delivery analysis
- `get_advanced_tunneling_metrics` - Deception metrics
- `get_deception_perceptual_metrics` - Perception analysis
- `get_pitch_shape_classification` - Shape analysis
- `get_contact_quality_by_pitch` - Pitch-specific contact
- `get_biomechanics_tech_metrics` - Tech metrics

### **Batting Analysis (7 tools)**
- `get_batter_basic_stats` - Traditional stats
- `get_batter_contact_quality` - Contact metrics
- `get_batter_plate_discipline` - Approach metrics
- `get_batter_expected_outcomes` - Expected results
- `get_batter_batted_ball_profile` - Batted ball data
- `get_batter_speed_metrics` - Speed and baserunning
- `get_batter_clutch_performance` - Clutch metrics

### **Other Tools (6 tools)**
- `get_pitcher_defensive_metrics` - Pitcher defense
- `get_batter_defensive_metrics` - Batter defense
- `get_defensive_comparison` - Defensive comparison
- `generate_pitch_plot` - Visualizations
- `get_pitcher_comparison` - Pitcher comparison
- `get_pitch_sequence_analysis` - Sequencing analysis
- `scrape_pitcher_news` - Latest news

## 🚨 **Troubleshooting**

### Common Issues

#### **Import Errors**
```bash
# Ensure you're in the right directory
cd baseball-stats-mcp
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

#### **Test Failures**
```bash
# Run basic tests first
python3 tests/run_all_tests.py --basic

# Check for specific failures
python3 tests/run_all_tests.py --comprehensive
```

#### **Server Connection Issues**
- Verify the server is running
- Check MCP client configuration
- Ensure correct port/connection settings

### **Getting Help**

1. **Check the logs** for error messages
2. **Run the test suite** to identify issues
3. **Review documentation** in the `docs/` directory
4. **Check issues** on the GitHub repository

## 📚 **Next Steps**

### **Learn More**
- **[TOOLS_REFERENCE.md](TOOLS_REFERENCE.md)** - Complete tool documentation
- **[ADVANCED_METRICS_GUIDE.md](ADVANCED_METRICS_GUIDE.md)** - Understanding baseball metrics
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Project architecture

### **Advanced Usage**
- **Custom Analysis**: Combine multiple tools for comprehensive evaluation
- **Data Export**: Use generated charts and data for reports
- **Integration**: Connect with other baseball analytics tools
- **Development**: Extend the server with new tools and metrics

### **Examples**
- **Scouting Reports**: Generate comprehensive player evaluations
- **Game Planning**: Analyze opponent tendencies and weaknesses
- **Development**: Identify areas for player improvement
- **Research**: Conduct baseball analytics research

## 🏆 **Success Indicators**

You're ready to go when:
- ✅ All tests pass (100% basic functionality)
- ✅ Server starts without errors
- ✅ MCP client connects successfully
- ✅ You can query basic stats
- ✅ Visualizations generate correctly

## 🎉 **Congratulations!**

You now have access to the most comprehensive baseball analytics platform available! 

**Start exploring:**
- Analyze your favorite players
- Generate professional-grade reports
- Create interactive visualizations
- Discover advanced baseball insights

**Welcome to the future of baseball analytics!** ⚾📊🚀
