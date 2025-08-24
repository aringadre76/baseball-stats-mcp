# Advanced Baseball Metrics Guide

This guide explains all the advanced baseball metrics now available through the Baseball Stats MCP Server. These metrics go far beyond traditional statistics and provide the same level of analysis used by MLB teams and professional analysts.

## 🚀 **Pitch Quality & Movement Metrics**

### Core Movement Metrics
- **Velocity (Velo)**: Average speed of the pitch in mph
- **Spin Rate (rpm)**: Higher spin can make fastballs "ride" or breaking balls break more
- **Spin Axis**: The orientation of the spin (like clock face direction)
- **Spin Efficiency (Active Spin)**: % of spin contributing to movement (vs. "gyro spin" that doesn't move the ball)
- **IVB (Induced Vertical Break)**: Vertical movement from spin, compared to gravity — fastballs with high IVB "rise"
- **HB (Horizontal Break)**: How much the ball moves left/right vs. average
- **Movement vs. Avg**: Statcast compares a pitch's movement to league average for that velocity/handedness

### Why These Matter
- **High IVB Fastballs**: Create the "rising" effect that makes them harder to square up
- **Spin Efficiency**: Determines how much of the spin actually contributes to movement
- **Movement vs. Average**: Shows how a pitcher's stuff compares to league standards

## 🎯 **Pitch Effectiveness Metrics**

### Contact Quality
- **Whiff Rate**: Percentage of swings that miss the ball
- **Chase Rate**: Percentage of swings at pitches outside the strike zone
- **Barrel Percentage**: Percentage of batted balls with optimal launch angle and exit velocity
- **Hard Hit Rate**: Percentage of batted balls with exit velocity ≥ 95 mph

### Zone Control
- **Zone Rate**: Percentage of pitches thrown in the strike zone
- **First Pitch Strike Rate**: Percentage of first pitches that result in a strike
- **Swinging Strike Rate**: Percentage of total pitches that result in swinging strikes
- **Called Strike Rate**: Percentage of total pitches that result in called strikes

### Advanced Analytics
- **CSW%**: Called Strike + Whiff percentage
- **O-Swing%**: Out-of-zone swing percentage
- **Z-Swing%**: In-zone swing percentage
- **O-Contact%**: Out-of-zone contact percentage
- **Z-Contact%**: In-zone contact percentage

## 📊 **Statcast Outcomes (The Gold Standard)**

### Per-Pitch Metrics
- **Whiff% per pitch**: Percentage of swings against that pitch that miss
- **CSW% per pitch**: Called strikes + whiffs, divided by total pitches
- **Putaway%**: How often a pitch finishes an at-bat with a strikeout

### Expected Outcomes
- **xBA vs pitch**: Expected batting average against that specific pitch
- **xSLG vs pitch**: Expected slugging percentage against that specific pitch
- **xwOBA vs pitch**: Expected weighted on-base average against that specific pitch

### Run Value
- **Run Value (RV)**: Statcast's all-in metric; how many runs above/below average that pitch has saved
- **RV/100 pitches**: Run value normalized per 100 pitches for fair comparison

## 🔄 **Pitch Usage & Tunneling**

### Usage Patterns
- **Pitch Usage %**: How often each pitch type is thrown
- **Release Point Consistency**: Repeatability of delivery across pitches

### Tunneling (The Art of Deception)
- **Tunneling Metrics**: How long different pitch types look the same before diverging
- **Tunneling Distance**: Distance from release point where pitches start to diverge
- **Tunneling Time**: Time from release until pitches become distinguishable

### Why Tunneling Matters
- **Example**: Fastball and slider with identical release but late divergence = great tunneling
- **Result**: Batters can't distinguish pitch types until it's too late to adjust

## 🎯 **Pitch Location & Command**

### Zone Analysis
- **Edge%**: Percentage of pitches thrown on the edges of the strike zone (where damage is lowest)
- **Zone%**: Percentage of pitches in the strike zone
- **Meatball%**: Percentage of pitches thrown down the middle
- **Called Strike%**: Percentage of takes that get a called strike (command-related)

### Command Quality
- **High Edge%**: Good command, keeps pitches away from the middle
- **Low Meatball%**: Avoids the most hittable locations
- **High Called Strike%**: Excellent command and umpire respect

## 🎭 **Specialized Pitch Analysis**

### Fastball Analysis
- **IVB (Induced Vertical Break)**: Vertical movement from spin
- **"Ride" Factor**: High IVB → harder to square up up in the zone
- **Hop Ratio**: Vertical break relative to velocity
- **Spin Efficiency**: How much spin contributes to movement

### Breaking Balls (Slider/Curve)
- **Sweep (Horizontal Break)**: Wider break = harder to hit
- **Gyro Sliders**: Low spin efficiency, dive more late
- **Spin Efficiency**: Determines movement characteristics

### Changeup Analysis
- **Velocity Differential**: Difference between fastball & changeup (ideally 8–12 mph)
- **Arm-Side Fade**: HB + drop, makes it miss barrels
- **Drop vs Fastball**: How much more the changeup drops

### Sinker Characteristics
- **Arm-Side Run**: Horizontal movement toward the pitcher's arm side
- **IVB vs Fastball**: Lower IVB = more groundballs
- **Ground Ball Rate**: Percentage of batted balls that stay on the ground

## 🛠️ **How to Use These Metrics**

### For Pitcher Analysis
```
Get the comprehensive pitch quality metrics for Max Scherzer including spin rate, IVB, and movement vs. average
```

### For Pitch-Specific Analysis
```
Analyze the specialized characteristics of Gerrit Cole's fastball including ride factor and hop ratio
```

### For Deception Analysis
```
Examine the pitch usage patterns and tunneling metrics for Clayton Kershaw to understand his deception
```

### For Command Analysis
```
Analyze Jacob deGrom's pitch location and command metrics including edge% and meatball%
```

### For Comparative Analysis
```
Compare the whiff rates, chase rates, and CSW% of Jacob deGrom, Gerrit Cole, and Max Scherzer in 2024
```

## 📈 **What These Metrics Reveal**

### Pitch Quality
- **High Spin Rate + High Efficiency**: Premium stuff
- **High IVB Fastball**: "Rising" effect, harder to square up
- **Movement vs. Average**: How stuff compares to league standards

### Effectiveness
- **High CSW%**: Pitch is working well
- **Low xBA/xSLG**: Pitch is effective at preventing damage
- **High Putaway%**: Pitch is a strikeout weapon

### Command
- **High Edge%**: Excellent command
- **Low Meatball%**: Avoids hittable locations
- **Consistent Release**: Repeatable delivery

### Deception
- **Good Tunneling**: Pitches look the same until late
- **Release Point Consistency**: Same delivery for all pitches
- **Velocity Differential**: Proper changeup separation

## 🎯 **Professional Applications**

### Scouting
- **Stuff Evaluation**: Spin rate, movement, efficiency
- **Command Assessment**: Zone%, edge%, meatball%
- **Deception Analysis**: Tunneling, release consistency

### Game Planning
- **Pitch Selection**: Usage patterns and effectiveness
- **Location Strategy**: Where to throw each pitch
- **Sequencing**: How to set up hitters

### Development
- **Mechanical Adjustments**: Improving spin efficiency
- **Pitch Design**: Optimizing movement profiles
- **Command Training**: Reducing meatball%

## 🚀 **Getting Started**

### Basic Analysis
1. Start with basic stats and efficiency metrics
2. Add pitch quality metrics for stuff evaluation
3. Include location and command analysis
4. Add specialized pitch analysis for specific pitches

### Advanced Analysis
1. Combine multiple metric types for comprehensive evaluation
2. Use tunneling metrics to understand deception
3. Analyze Statcast outcomes for effectiveness
4. Compare across multiple pitchers and seasons

### Example Workflow
```
1. Get basic stats for pitcher A
2. Analyze pitch quality metrics
3. Examine usage and tunneling patterns
4. Review location and command data
5. Get specialized analysis for key pitches
6. Compare with other pitchers
7. Generate visualizations for key insights
```

This comprehensive set of metrics provides the same analytical depth used by MLB teams, giving you professional-grade insights into pitching performance and effectiveness.
