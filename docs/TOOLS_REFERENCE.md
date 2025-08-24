# Baseball Stats MCP Server - Complete Tools Reference

This document provides a comprehensive reference for all available tools in the Baseball Stats MCP Server, organized by category and functionality.

## Table of Contents

1. [Pitcher Analysis Tools](#pitcher-analysis-tools)
2. [Batter Analysis Tools](#batter-analysis-tools)
3. [Defensive Metrics Tools](#defensive-metrics-tools)
4. [Visualization Tools](#visualization-tools)
5. [Comparison Tools](#comparison-tools)
6. [News and Information Tools](#news-and-information-tools)

---

## Pitcher Analysis Tools

### 1. get_pitcher_basic_stats
**Purpose**: Retrieves traditional and advanced pitching statistics for a specific pitcher.

**Input Parameters**:
- `pitcher_name` (required): Full name of the pitcher
- `season` (optional): Season year (e.g., '2024')

**Returns**: Basic stats including W-L, ERA, IP, SO, BB, WHIP, K/9, BB/9, HR/9, FIP, xFIP, BABIP, K%, BB%, K-BB%

**Use Case**: Quick overview of a pitcher's season performance and effectiveness.

---

### 2. get_pitch_breakdown
**Purpose**: Provides detailed breakdown of pitch types, velocities, and movement including advanced metrics.

**Input Parameters**:
- `pitcher_name` (required): Full name of the pitcher
- `season` (optional): Season year (e.g., '2024')
- `pitch_type` (optional): Specific pitch type to analyze

**Returns**: Comprehensive pitch data including velocity, spin rate, spin axis, spin efficiency, IVB, HB, movement vs. average, and location data.

**Use Case**: Deep analysis of pitch characteristics and movement patterns.

---

### 3. get_pitch_efficiency_metrics
**Purpose**: Retrieves advanced efficiency metrics that measure how effective pitches are at getting outs.

**Input Parameters**:
- `pitcher_name` (required): Full name of the pitcher
- `season` (optional): Season year (e.g., '2024')
- `metric_type` (optional): Type of efficiency metric to focus on

**Returns**: Whiff rate, chase rate, barrel percentage, CSW%, putaway%, xBA, xSLG, xwOBA, run value, and RV/100 pitches.

**Use Case**: Evaluating pitch effectiveness and identifying strengths/weaknesses.

---

### 4. get_pitch_quality_metrics
**Purpose**: Analyzes comprehensive pitch quality including spin characteristics and movement.

**Input Parameters**:
- `pitcher_name` (required): Full name of the pitcher
- `season` (optional): Season year (e.g., '2024')
- `pitch_type` (optional): Specific pitch type to analyze

**Returns**: Spin rate, spin axis, spin efficiency, IVB, HB, movement vs. average, and quality indicators.

**Use Case**: Understanding the physical characteristics that make pitches effective.

---

### 5. get_pitch_usage_tunneling
**Purpose**: Examines pitch usage patterns and tunneling deception strategies.

**Input Parameters**:
- `pitcher_name` (required): Full name of the pitcher
- `season` (optional): Season year (e.g., '2024')
- `pitch_type` (optional): Specific pitch type to analyze

**Returns**: Usage percentages, release point consistency, tunneling distance, tunneling time, and deception metrics.

**Use Case**: Analyzing strategic pitch sequencing and deception tactics.

---

### 6. get_pitch_location_command
**Purpose**: Evaluates pitch location and command metrics for zone control.

**Input Parameters**:
- `pitcher_name` (required): Full name of the pitcher
- `season` (optional): Season year (e.g., '2024')
- `pitch_type` (optional): Specific pitch type to analyze

**Returns**: Edge%, zone%, meatball%, called strike%, and location effectiveness metrics.

**Use Case**: Assessing pitch command and location precision.

---

### 7. get_specialized_pitch_analysis
**Purpose**: Provides pitch-specific analysis for different pitch types.

**Input Parameters**:
- `pitcher_name` (required): Full name of the pitcher
- `season` (optional): Season year (e.g., '2024')
- `pitch_type` (required): Specific pitch type (Fastball, Slider, Changeup, Sinker, etc.)

**Returns**: Pitch-specific characteristics like fastball ride, breaking ball sweep, changeup velocity differential, and sinker characteristics.

**Use Case**: Understanding the unique qualities of specific pitch types.

---

### 8. get_run_prevention_metrics
**Purpose**: Analyzes comprehensive run prevention metrics and ERA alternatives.

**Input Parameters**:
- `pitcher_name` (required): Full name of the pitcher
- `season` (optional): Season year (e.g., '2024')

**Returns**: ERA+, FIP, xFIP, SIERA, and other advanced run prevention metrics.

**Use Case**: Evaluating true pitching effectiveness beyond traditional ERA.

---

### 9. get_contact_quality_metrics
**Purpose**: Examines how well a pitcher controls contact quality and batted ball outcomes.

**Input Parameters**:
- `pitcher_name` (required): Full name of the pitcher
- `season` (optional): Season year (e.g., '2024')

**Returns**: HR/FB%, GB%/FB%/LD%, Hard Hit%, Barrel%, expected outcomes, and contact quality indicators.

**Use Case**: Understanding how well a pitcher limits damage when contact is made.

---

### 10. get_win_probability_metrics
**Purpose**: Analyzes win probability and value metrics for situational effectiveness.

**Input Parameters**:
- `pitcher_name` (required): Full name of the pitcher
- `season` (optional): Season year (e.g., '2024')

**Returns**: WAR, WPA, RE24, leverage statistics, shutdowns, meltdowns, and clutch performance.

**Use Case**: Evaluating a pitcher's impact on game outcomes and win probability.

---

### 11. get_plate_discipline_metrics
**Purpose**: Examines how well a pitcher controls the strike zone and induces poor swings.

**Input Parameters**:
- `pitcher_name` (required): Full name of the pitcher
- `season` (optional): Season year (e.g., '2024')

**Returns**: O-Swing%, Z-Swing%, SwStr%, CSW%, Contact%, First Pitch Strike%, and zone control metrics.

**Use Case**: Understanding a pitcher's ability to control at-bats and induce weak contact.

---

### 12. get_spin_aerodynamics_metrics
**Purpose**: Analyzes advanced spin and aerodynamics including Seam-Shifted Wake effects.

**Input Parameters**:
- `pitcher_name` (required): Full name of the pitcher
- `season` (optional): Season year (e.g., '2024')
- `pitch_type` (optional): Specific pitch type to analyze

**Returns**: SSW factors, true spin axis vs. observed movement, Magnus vs. non-Magnus movement, and aerodynamic effects.

**Use Case**: Understanding the physics behind pitch movement and deception.

---

### 13. get_biomechanics_release_metrics
**Purpose**: Examines biomechanics and release characteristics for delivery analysis.

**Input Parameters**:
- `pitcher_name` (required): Full name of the pitcher
- `season` (optional): Season year (e.g., '2024')

**Returns**: Extension, release points, delivery mechanics, arm slot, and biomechanical efficiency.

**Use Case**: Analyzing delivery mechanics and identifying potential improvements.

---

### 14. get_advanced_tunneling_metrics
**Purpose**: Provides advanced pitch tunneling analysis for deception evaluation.

**Input Parameters**:
- `pitcher_name` (required): Full name of the pitcher
- `season` (optional): Season year (e.g., '2024')
- `pitch_comparison` (optional): Pitch types to compare for tunneling

**Returns**: Release distance, tunnel point, tunnel differential, break tunneling ratio, and deception scores.

**Use Case**: Evaluating how well a pitcher can disguise different pitch types.

---

### 15. get_deception_perceptual_metrics
**Purpose**: Analyzes deception and perceptual metrics for effectiveness evaluation.

**Input Parameters**:
- `pitcher_name` (required): Full name of the pitcher
- `season` (optional): Season year (e.g., '2024')

**Returns**: Effective velocity, perceived velocity, time to plate analysis, and deception factors.

**Use Case**: Understanding how a pitcher's delivery affects batter perception and timing.

---

### 16. get_pitch_shape_classification
**Purpose**: Classifies pitch shapes and movement patterns using advanced modeling.

**Input Parameters**:
- `pitcher_name` (required): Full name of the pitcher
- `season` (optional): Season year (e.g., '2024')
- `pitch_type` (optional): Specific pitch type to analyze

**Returns**: Movement clusters, axis tilt, Stuff+ modeling, and shape classification.

**Use Case**: Categorizing pitch movement patterns and identifying unique characteristics.

---

### 17. get_contact_quality_by_pitch
**Purpose**: Analyzes contact quality patterns for specific pitch types.

**Input Parameters**:
- `pitcher_name` (required): Full name of the pitcher
- `season` (optional): Season year (e.g., '2024')
- `pitch_type` (optional): Specific pitch type to analyze

**Returns**: Launch angle patterns, bat speed matchups, and contact quality by pitch type.

**Use Case**: Understanding how different pitch types perform against contact.

---

### 18. get_biomechanics_tech_metrics
**Purpose**: Provides cutting-edge biomechanics and technology metrics.

**Input Parameters**:
- `pitcher_name` (required): Full name of the pitcher
- `season` (optional): Season year (e.g., '2024')

**Returns**: Hawkeye data, kinematic sequencing, grip analysis, and advanced biomechanical metrics.

**Use Case**: Accessing the latest technology-driven pitching insights.

---

## Batter Analysis Tools

### 19. get_batter_basic_stats
**Purpose**: Retrieves basic batting statistics including traditional and advanced metrics.

**Input Parameters**:
- `batter_name` (required): Full name of the batter
- `season` (optional): Season year (e.g., '2024')

**Returns**: AVG, OBP, SLG, OPS, HR, RBI, SB, BB, SO, wOBA, wRC+, ISO, BABIP, K%, BB%, K-BB%

**Use Case**: Quick overview of a batter's season performance and offensive value.

---

### 20. get_batter_contact_quality
**Purpose**: Analyzes comprehensive contact quality metrics including Statcast Core data.

**Input Parameters**:
- `batter_name` (required): Full name of the batter
- `season` (optional): Season year (e.g., '2024')
- `metric_type` (optional): Type of contact quality metric to focus on

**Returns**: Exit velocity, launch angle, sweet spot%, GB%/FB%/LD%, barrel metrics, and expected outcomes.

**Use Case**: Understanding how well a batter makes contact and the quality of that contact.

---

### 21. get_batter_plate_discipline
**Purpose**: Examines plate discipline and swing decision metrics.

**Input Parameters**:
- `batter_name` (required): Full name of the batter
- `season` (optional): Season year (e.g., '2024')

**Returns**: O-Swing%, Z-Swing%, Contact%, O-Contact%, Z-Contact%, SwStr%, CSW%, K%, and zone control metrics.

**Use Case**: Evaluating a batter's approach at the plate and swing decision quality.

---

### 22. get_batter_expected_outcomes
**Purpose**: Analyzes expected outcome metrics and run value data.

**Input Parameters**:
- `batter_name` (required): Full name of the batter
- `season` (optional): Season year (e.g., '2024')

**Returns**: xBA, xSLG, xwOBA, xISO, run value, run value per 100 PA, and performance vs. expected.

**Use Case**: Understanding a batter's true offensive value beyond actual outcomes.

---

### 23. get_batter_batted_ball_profile
**Purpose**: Examines detailed batted ball profile and spray chart tendencies.

**Input Parameters**:
- `batter_name` (required): Full name of the batter
- `season` (optional): Season year (e.g., '2024')

**Returns**: GB%/FB%/LD%, Pull%/Center%/Opposite%, contact quality distribution, and launch characteristics.

**Use Case**: Understanding a batter's hitting tendencies and approach.

---

### 24. get_batter_speed_metrics
**Purpose**: Analyzes baserunning and speed metrics for athletic evaluation.

**Input Parameters**:
- `batter_name` (required): Full name of the batter
- `season` (optional): Season year (e.g., '2024')

**Returns**: Sprint speed, stolen base success rate, baserunning value, first-to-third rate, and defensive range.

**Use Case**: Evaluating a batter's speed and baserunning impact.

---

### 25. get_batter_clutch_performance
**Purpose**: Examines clutch performance and situational effectiveness.

**Input Parameters**:
- `batter_name` (required): Full name of the batter
- `season` (optional): Season year (e.g., '2024')

**Returns**: WPA, WPA/LI, Clutch, RE24, leverage performance, and RISP statistics.

**Use Case**: Understanding how a batter performs in high-pressure situations.

---

## Defensive Metrics Tools

### 26. get_pitcher_defensive_metrics
**Purpose**: Analyzes defensive metrics for pitchers including fielding and pickoff ability.

**Input Parameters**:
- `pitcher_name` (required): Full name of the pitcher
- `season` (optional): Season year (e.g., '2024')

**Returns**: Fielding percentage, range factor, DRS, UZR, defensive WAR, pickoff attempts, and success rate.

**Use Case**: Evaluating a pitcher's defensive contributions beyond pitching.

---

### 27. get_batter_defensive_metrics
**Purpose**: Analyzes comprehensive defensive metrics for position players.

**Input Parameters**:
- `batter_name` (required): Full name of the batter
- `season` (optional): Season year (e.g., '2024')
- `position` (optional): Specific defensive position to analyze

**Returns**: Fielding percentage, range factor, DRS, UZR, defensive WAR, and position-specific metrics.

**Use Case**: Evaluating a player's defensive value and range at specific positions.

---

### 28. get_defensive_comparison
**Purpose**: Compares defensive metrics between multiple players or positions.

**Input Parameters**:
- `player_names` (required): List of player names to compare
- `season` (optional): Season year (e.g., '2024')
- `position` (optional): Specific defensive position to compare

**Returns**: Side-by-side comparison of defensive metrics including fielding%, DRS, UZR, and range factor.

**Use Case**: Comparing defensive abilities between players or evaluating position changes.

---

## Visualization Tools

### 29. generate_pitch_plot
**Purpose**: Creates interactive pitch visualization charts for analysis.

**Input Parameters**:
- `pitcher_name` (required): Full name of the pitcher
- `chart_type` (required): Type of chart (movement, velocity, location, heatmap)
- `season` (optional): Season year (e.g., '2024')
- `pitch_type` (optional): Specific pitch type to visualize

**Returns**: Interactive Plotly charts showing pitch movement, velocity distribution, location patterns, or heatmaps.

**Use Case**: Visual analysis of pitch characteristics and patterns.

---

## Comparison Tools

### 30. get_pitcher_comparison
**Purpose**: Compares multiple pitchers across various advanced metrics.

**Input Parameters**:
- `pitcher_names` (required): List of pitcher names to compare
- `season` (optional): Season year (e.g., '2024')
- `metrics` (optional): Specific metrics to compare

**Returns**: Side-by-side comparison of selected metrics with rankings and analysis.

**Use Case**: Evaluating pitcher performance relative to peers or identifying trade targets.

---

### 31. get_pitch_sequence_analysis
**Purpose**: Analyzes pitch sequencing patterns and effectiveness.

**Input Parameters**:
- `pitcher_name` (required): Full name of the pitcher
- `season` (optional): Season year (e.g., '2024')
- `count_situation` (optional): Specific count situation to analyze

**Returns**: First pitch patterns, count tendencies, two-strike approach, and sequencing effectiveness.

**Use Case**: Understanding a pitcher's strategic approach and sequencing tendencies.

---

## News and Information Tools

### 32. scrape_pitcher_news
**Purpose**: Scrapes latest news and analysis about specific pitchers using Firecrawl.

**Input Parameters**:
- `pitcher_name` (required): Full name of the pitcher
- `news_sources` (optional): News sources to search (e.g., ['mlb.com', 'fangraphs.com'])

**Returns**: Latest news articles, analysis, and insights about the specified pitcher.

**Use Case**: Staying updated on pitcher news, injuries, analysis, and recent performance.

---

## Tool Categories Summary

### **Pitching Analysis (18 tools)**
- Basic stats and traditional metrics
- Advanced pitch characteristics (spin, movement, tunneling)
- Efficiency and effectiveness metrics
- Biomechanics and delivery analysis
- Strategic sequencing and deception

### **Batting Analysis (7 tools)**
- Traditional and advanced offensive metrics
- Contact quality and Statcast data
- Plate discipline and approach
- Expected outcomes and run value
- Speed and baserunning metrics
- Clutch performance analysis

### **Defensive Analysis (3 tools)**
- Pitcher defensive metrics
- Position player defensive evaluation
- Multi-player defensive comparisons

### **Visualization (1 tool)**
- Interactive pitch charts and analysis

### **Comparison & Analysis (2 tools)**
- Multi-pitcher comparisons
- Pitch sequencing analysis

### **Information (1 tool)**
- Latest news and analysis

---

## Usage Examples

### Basic Pitcher Analysis
```python
# Get comprehensive pitcher overview
pitcher_stats = await get_pitcher_basic_stats({"pitcher_name": "Jacob deGrom", "season": "2024"})
pitch_breakdown = await get_pitch_breakdown({"pitcher_name": "Jacob deGrom", "season": "2024"})
efficiency = await get_pitch_efficiency_metrics({"pitcher_name": "Jacob deGrom", "season": "2024"})
```

### Advanced Pitch Analysis
```python
# Analyze specific pitch characteristics
fastball_analysis = await get_specialized_pitch_analysis({
    "pitcher_name": "Jacob deGrom", 
    "season": "2024", 
    "pitch_type": "Fastball"
})
tunneling = await get_advanced_tunneling_metrics({
    "pitcher_name": "Jacob deGrom", 
    "season": "2024"
})
```

### Batter Analysis
```python
# Comprehensive batter evaluation
batter_stats = await get_batter_basic_stats({"batter_name": "Mike Trout", "season": "2024"})
contact_quality = await get_batter_contact_quality({"batter_name": "Mike Trout", "season": "2024"})
plate_discipline = await get_batter_plate_discipline({"batter_name": "Mike Trout", "season": "2024"})
```

### Defensive Evaluation
```python
# Compare defensive abilities
defensive_comparison = await get_defensive_comparison({
    "player_names": ["Mookie Betts", "Ronald Acuña Jr."], 
    "season": "2024", 
    "position": "rf"
})
```

### Visualization
```python
# Create pitch movement chart
movement_chart = await generate_pitch_plot({
    "pitcher_name": "Jacob deGrom", 
    "chart_type": "movement", 
    "season": "2024"
})
```

---

## Data Sources

The Baseball Stats MCP Server integrates with multiple data sources:

1. **MLB API**: Official statistics and basic metrics
2. **Statcast**: Advanced metrics including exit velocity, launch angle, spin rate, and movement data
3. **Firecrawl**: News scraping and analysis from various sources
4. **Mock Data**: Comprehensive sample data for testing and demonstration

---

## Performance Notes

- **API Calls**: Tools make intelligent API calls to minimize data requests
- **Caching**: Results are cached when possible to improve response times
- **Fallback**: Mock data is provided when external APIs are unavailable
- **Error Handling**: Comprehensive error handling with fallback to mock data

---

## Getting Started

1. **Installation**: Ensure the MCP server is properly configured
2. **API Keys**: Set up MLB API and Firecrawl tokens for full functionality
3. **Basic Usage**: Start with basic stats tools to understand the data structure
4. **Advanced Analysis**: Progress to specialized tools for deeper insights
5. **Visualization**: Use chart tools to visualize patterns and trends

---

This comprehensive toolset provides the most complete baseball analytics platform available, covering every aspect of player performance from basic statistics to the most sophisticated modern analytics.
