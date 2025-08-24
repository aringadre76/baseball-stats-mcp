# Baseball Stats MCP Server - Project Structure

This document provides a comprehensive overview of the project structure, explaining the purpose and organization of each component in the Baseball Stats MCP Server.

## Project Overview

The Baseball Stats MCP Server is a comprehensive baseball analytics platform that provides access to every advanced baseball metric available, from traditional statistics to cutting-edge Statcast data and biomechanical analysis.

## Directory Structure

```
baseball-stats-mcp/
├── src/                           # Source code directory
│   ├── server.py                 # Main MCP server implementation
│   ├── run_server.py             # Server startup script
│   └── demo_visualizations.py    # Visualization examples
├── docs/                         # Documentation directory
│   ├── TOOLS_REFERENCE.md        # Complete tools reference
│   ├── PROJECT_STRUCTURE.md      # This file
│   ├── COMPLETE_METRICS_SUMMARY.md # Metrics overview
│   ├── ADVANCED_METRICS_GUIDE.md   # Advanced metrics explanation
│   └── IMPLEMENTATION_SUMMARY.md   # Implementation details
├── tests/                        # Test files
│   └── test_server.py            # Server functionality tests
├── examples/                     # Example files and outputs
│   └── example_chart.html        # Sample visualization output
├── .gitignore                    # Git ignore rules
├── README.md                     # Main project documentation
├── QUICKSTART.md                 # Quick start guide
├── requirements.txt              # Python dependencies
└── mcp_config.json              # MCP configuration file
```

## Core Components

### 1. Source Code (`src/`)

#### `server.py` - Main Server Implementation
**Purpose**: Core MCP server that implements all baseball analytics tools
**Key Features**:
- 32 comprehensive baseball analysis tools
- Integration with MLB API and Statcast data
- Firecrawl news scraping capabilities
- Comprehensive error handling and fallback systems
- Mock data for testing and demonstration

**Architecture**:
- `BaseballStatsMCPServer` class with modular tool implementation
- Async/await pattern for non-blocking operations
- Comprehensive data parsing and validation
- Intelligent API call management

#### `run_server.py` - Server Startup Script
**Purpose**: Entry point for starting the MCP server
**Features**:
- Environment variable loading
- Server initialization
- Error handling and logging setup

#### `demo_visualizations.py` - Visualization Examples
**Purpose**: Demonstrates chart generation capabilities
**Features**:
- Sample pitch movement charts
- Velocity distribution plots
- Location heatmaps

### 2. Documentation (`docs/`)

#### `TOOLS_REFERENCE.md` - Complete Tools Reference
**Purpose**: Comprehensive documentation of all 32 available tools
**Content**:
- Detailed tool descriptions and parameters
- Use cases and examples
- Input/output specifications
- Categorization by functionality

#### `PROJECT_STRUCTURE.md` - This File
**Purpose**: Project organization and component explanation
**Content**:
- Directory structure overview
- Component purposes and relationships
- Development workflow

#### `COMPLETE_METRICS_SUMMARY.md` - Metrics Overview
**Purpose**: High-level summary of available metrics
**Content**:
- Metric categories and coverage
- Tool availability matrix
- Example queries and use cases

#### `ADVANCED_METRICS_GUIDE.md` - Advanced Metrics Explanation
**Purpose**: Educational content for advanced baseball analytics
**Content**:
- Metric definitions and calculations
- Interpretation guidelines
- Statistical significance explanations

#### `IMPLEMENTATION_SUMMARY.md` - Implementation Details
**Purpose**: Technical implementation information
**Content**:
- Architecture decisions
- Data flow diagrams
- Performance considerations

### 3. Testing (`tests/`)

#### `test_server.py` - Server Functionality Tests
**Purpose**: Validate server functionality and tool implementations
**Features**:
- Unit tests for individual tools
- Integration tests for data flow
- Mock data validation
- Error handling verification

### 4. Examples (`examples/`)

#### `example_chart.html` - Sample Visualization Output
**Purpose**: Demonstrates chart generation capabilities
**Features**:
- Interactive Plotly charts
- Sample pitch data visualization
- Chart customization examples

### 5. Configuration Files

#### `.gitignore` - Git Ignore Rules
**Purpose**: Exclude unnecessary files from version control
**Exclusions**:
- Cursor rules files (`.cursorrules`, `.cursor-rules`)
- Python cache and build files
- Virtual environments
- IDE configuration files
- OS-specific files
- Logs and temporary files

#### `mcp_config.json` - MCP Configuration
**Purpose**: Model Context Protocol server configuration
**Content**:
- Server identification
- Capability definitions
- Connection parameters

#### `requirements.txt` - Python Dependencies
**Purpose**: Define required Python packages
**Key Dependencies**:
- `mcp`: Model Context Protocol implementation
- `requests`: HTTP client for API calls
- `pandas`: Data manipulation and analysis
- `plotly`: Interactive chart generation
- `numpy`: Numerical computing
- `python-dotenv`: Environment variable management

## Data Flow Architecture

### 1. Client Request Flow
```
Client Request → MCP Server → Tool Handler → Data Fetcher → API/Data Source → Parser → Response
```

### 2. Data Sources
- **MLB API**: Official statistics and basic metrics
- **Statcast**: Advanced metrics (exit velocity, spin rate, movement)
- **Firecrawl**: News and analysis scraping
- **Mock Data**: Comprehensive sample data for testing

### 3. Data Processing Pipeline
1. **Request Validation**: Parameter checking and validation
2. **Data Fetching**: API calls with error handling
3. **Data Parsing**: Raw data to structured format conversion
4. **Response Formatting**: Markdown-formatted output
5. **Fallback Handling**: Mock data when APIs unavailable

## Tool Categories

### Pitching Analysis (18 tools)
- Basic statistics and traditional metrics
- Advanced pitch characteristics
- Efficiency and effectiveness metrics
- Biomechanics and delivery analysis
- Strategic sequencing and deception

### Batting Analysis (7 tools)
- Traditional and advanced offensive metrics
- Contact quality and Statcast data
- Plate discipline and approach
- Expected outcomes and run value
- Speed and baserunning metrics
- Clutch performance analysis

### Defensive Analysis (3 tools)
- Pitcher defensive metrics
- Position player defensive evaluation
- Multi-player defensive comparisons

### Visualization (1 tool)
- Interactive pitch charts and analysis

### Comparison & Analysis (2 tools)
- Multi-pitcher comparisons
- Pitch sequencing analysis

### Information (1 tool)
- Latest news and analysis

## Development Workflow

### 1. Adding New Tools
1. Define tool in `setup_server()` method
2. Add tool handler in `handle_call_tool()`
3. Implement tool method with async signature
4. Add data fetching method if needed
5. Add parsing method for API responses
6. Add mock data method for fallback
7. Update documentation

### 2. Testing New Features
1. Unit test individual components
2. Integration test data flow
3. Validate error handling
4. Test fallback mechanisms
5. Update test documentation

### 3. Documentation Updates
1. Update `TOOLS_REFERENCE.md`
2. Update relevant category documentation
3. Add usage examples
4. Update project structure if needed

## Performance Considerations

### 1. API Call Optimization
- Intelligent caching of frequently requested data
- Batch requests when possible
- Rate limiting compliance
- Connection pooling

### 2. Data Processing
- Efficient data parsing algorithms
- Memory management for large datasets
- Async processing for non-blocking operations

### 3. Fallback Systems
- Comprehensive mock data coverage
- Graceful degradation when APIs unavailable
- User-friendly error messages

## Security and Privacy

### 1. API Key Management
- Environment variable storage
- Secure token handling
- Access control validation

### 2. Data Privacy
- No user data storage
- Secure API communication
- Rate limiting compliance

## Deployment Considerations

### 1. Environment Setup
- Python 3.8+ requirement
- Virtual environment isolation
- Dependency management
- Environment variable configuration

### 2. Server Configuration
- MCP protocol compliance
- Logging and monitoring
- Error handling and recovery
- Performance monitoring

### 3. Scaling Considerations
- Async operation support
- Memory usage optimization
- Connection pooling
- Load balancing readiness

## Future Enhancements

### 1. Additional Data Sources
- More comprehensive Statcast integration
- Additional news sources
- Historical data archives
- Real-time data feeds

### 2. Advanced Analytics
- Machine learning predictions
- Trend analysis algorithms
- Comparative analytics
- Custom metric calculations

### 3. User Experience
- Enhanced visualization options
- Custom dashboard creation
- Export functionality
- Batch processing capabilities

## Conclusion

The Baseball Stats MCP Server provides the most comprehensive baseball analytics platform available, with a well-organized, maintainable codebase that supports easy extension and enhancement. The modular architecture ensures that new tools can be added efficiently while maintaining code quality and performance.

The project structure emphasizes:
- **Maintainability**: Clear separation of concerns and modular design
- **Extensibility**: Easy addition of new tools and data sources
- **Reliability**: Comprehensive error handling and fallback systems
- **Documentation**: Thorough documentation for all components
- **Testing**: Comprehensive test coverage for quality assurance

This structure enables developers to easily understand, modify, and extend the system while maintaining high code quality and performance standards.
