# SLA Activity Scheduler - Genetic Algorithm Solution

## 📋 Overview

A genetic algorithm implementation for optimizing room, time, and facilitator assignments for the Seminar Learning Association (SLA). This solution automatically generates optimal schedules that respect complex constraints while maximizing fitness scores according to Appendix A requirements.

## ✨ Features

### **Core Algorithm**
- ✅ Population-based genetic algorithm with customizable parameters
- ✅ Complete implementation of all Appendix A fitness rules
- ✅ Softmax-based parent selection
- ✅ Single-point and uniform crossover methods
- ✅ Adaptive mutation rate (automatically adjusts during optimization)
- ✅ Elitism preservation of best schedules
- ✅ Termination when improvement <1% per generation

### **Constraint Handling**
- 🏫 **Room Constraints**: Size violations, capacity mismatches, conflicts
- 👨‍🏫 **Facilitator Constraints**: Preferences, overload/underload, time conflicts
- ⏰ **Time Constraints**: Section spacing, consecutive class optimization
- 🏛️ **Special Rules**: SLA101/SLA191 interactions, building preferences

### **Web Interface**
- 🎀 **Modern Pink-Themed UI** with custom styling
- 📊 **Real-time Visualizations**: Fitness progression charts
- ⚙️ **Interactive Controls**: Adjust algorithm parameters live
- 📋 **Multiple Views**: Schedule display, violation analysis, data export
- 📈 **Performance Metrics**: Generation-by-generation statistics
- 📥 **Export Options**: CSV downloads for schedules and history

## 🚀 Quick Start

### **Prerequisites**
```bash
Python 3.8+
pip install streamlit pandas matplotlib
```

### **Installation**
1. Clone the repository:
```bash
git clone <repository-url>
cd sla-genetic-scheduler
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

### **Alternative: Direct Run**
```bash
# One-liner installation and run
pip install streamlit pandas matplotlib && streamlit run app.py
```

## 🏗️ Project Structure

```
sla-scheduler/
├── app.py                      # Main Streamlit web interface
├── gen/                        # Core genetic algorithm package
│   ├── __init__.py            # Package exports
│   ├── constants.py           # Rooms, activities, facilitators
│   ├── models.py              # Schedule and Assignment classes
│   ├── population_manager.py  # Initial population creation
│   ├── fitness_evaluator.py   # Fitness calculation (Appendix A)
│   ├── selection_methods.py   # Softmax selection, parent pairing
│   ├── genetic_operators.py   # Crossover and mutation
│   └── algorithm_engine.py    # Main GA loop controller
├── output/                    # Generated schedules (created at runtime)
└── README.md                  # This file
```

## ⚙️ Configuration Options

### **Algorithm Parameters**
| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| Population Size | Schedules per generation | 250 | 250-1500 |
| Minimum Generations | Minimum evolution cycles | 100 | 50-300 |
| Maximum Generations | Maximum evolution cycles | 500 | 200-1000 |
| Mutation Rate | Probability of random changes | 0.01 | 0.001-0.05 |
| Crossover Method | Parent combination method | Single Point | Single/Uniform |
| Elite Count | Best schedules preserved | 1 | 0-10 |

### **Quick Start Settings**
For best results, use these recommended settings:
- **Population Size**: 300
- **Generations**: 100 min, 500 max
- **Mutation Rate**: 0.01
- **Crossover**: Single Point
- **Elitism**: 2

## 📊 Understanding the Output

### **Fitness Score Interpretation**
- **Positive Score**: Good schedule (higher is better)
- **Typical Range**: -10 to +10 based on constraint satisfaction
- **Perfect Score**: Maximizes all positive bonuses, minimizes violations

### **Violation Categories**
1. **Room Issues** (Red/Yellow indicators)
   - Conflicts, size mismatches, under/over utilization
2. **Time Issues** 
   - Section conflicts, improper spacing
3. **Facilitator Issues**
   - Overload (>4 activities), underload (<3), time conflicts
4. **Special Interactions**
   - SLA101/SLA191 consecutive pairs, building mismatches

### **Visualization Tabs**
1. **📈 Fitness Analysis** - Evolution charts
2. **🌸 Optimal Schedule** - Best found schedule
3. **⚠️ Constraint Analysis** - Violation breakdown
4. **📊 Data Export** - Download results

## 🧠 Algorithm Details

### **Fitness Function Components**
```
Total Fitness = 
  Base Activity Scores (room, facilitator, preferences) +
  Section Spacing Rules +
  Cross-Section Interactions +
  Load Balancing Bonuses/Penalties
```

### **Genetic Operations**
1. **Selection**: Softmax probability distribution based on fitness
2. **Crossover**: Mix parent schedules to create offspring
3. **Mutation**: Random changes to explore solution space
4. **Elitism**: Preserve top performers unchanged

### **Termination Conditions**
1. Minimum 100 generations completed
2. Average fitness improvement <1% between generations
3. Maximum generation limit reached (safety net)

## 🎯 Example Use Cases

### **Scenario 1: Quick Optimization**
1. Use default parameters
2. Run algorithm (~1-2 minutes)
3. Export schedule for review

### **Scenario 2: Fine-Tuning**
1. Increase population to 500
2. Set mutation rate to 0.005
3. Enable adaptive mutation
4. Run for detailed analysis

### **Scenario 3: Constraint Analysis**
1. Run optimization
2. Check "Constraint Analysis" tab
3. Identify recurring violation patterns
4. Adjust algorithm to target specific issues

## 📁 Data Files

### **Input Data (Hardcoded in constants.py)**
- **11 Activities** with enrollment expectations
- **10 Facilitators** with preference levels
- **7 Rooms** with capacities and equipment
- **6 Time Slots** from 10 AM to 3 PM

### **Output Files**
Generated in `output/` directory:
- `sla_optimal_schedule_YYYYMMDD_HHMMSS.csv` - Best schedule
- Fitness history and violation reports via download buttons

## 🛠️ Development

### **Extending the Algorithm**
1. **Add New Constraints**:
   - Modify `fitness_evaluator.py`
   - Update `calculate_constraint_violations()`
   
2. **Customize Visualization**:
   - Edit CSS in `app.py`
   - Add new charts to analysis tabs

3. **Enhance Algorithm**:
   - Implement new crossover methods
   - Add additional selection strategies
   - Include optional constraints from assignment

### **Testing**
```bash
# Run with test parameters
python -c "from gen.algorithm_engine import execute_genetic_algorithm; print(execute_genetic_algorithm(population_size=100, minimum_generations=5))"
```

## 📝 Assignment Requirements Met

| Requirement | Status | Notes |
|-------------|---------|-------|
| Population ≥ 250 | ✅ | Configurable up to 1500 |
| Minimum 100 generations | ✅ | Configurable minimum |
| <1% improvement termination | ✅ | Automatic detection |
| Softmax selection | ✅ | Implemented in selection_methods.py |
| Mutation rate 0.01 | ✅ | Adaptive adjustment available |
| All Appendix A rules | ✅ | Complete implementation |
| CSV export | ✅ | Schedule and history exports |
| Fitness visualization | ✅ | Real-time charts |
| Constraint violation analysis | ✅ | Detailed breakdown |
| GUI interface | ✅ | Streamlit web app |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/improvement`)
5. Create Pull Request

## 📄 License

This project is for educational purposes as part of CS 461 AI coursework.

## 🙏 Acknowledgments

- CS 461 AI Program 2 assignment guidelines
- Genetic algorithm theory and implementations
- Streamlit for the web framework
- All contributors and testers

## 📞 Support

For issues or questions:
1. Check the algorithm parameters
2. Review the constraint explanations in the app
3. Examine generated violation reports

---

**Ready to schedule?** Run `streamlit run app.py` and start optimizing! 🌸

---

*Last Updated: 2024-03-15 | Version: 1.0.0*
