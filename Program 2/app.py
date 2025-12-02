"""
Streamlit Web Interface for SLA Genetic Algorithm Scheduler
Modern, interactive UI with real-time visualizations and controls.
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Ensure output directory exists
os.makedirs("output", exist_ok=True)

# Import GA components from gen module
from gen.algorithm_engine import execute_genetic_algorithm
from gen.fitness_evaluator import fitness_calculator

# ============================================================================
# PAGE CONFIGURATION AND STYLING
# ============================================================================

st.set_page_config(
    page_title="SLA Activity Scheduler",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/GeneticAlgorithm-Scheduler',
        'Report a bug': "https://github.com/yourusername/GeneticAlgorithm-Scheduler/issues",
        'About': "Genetic Algorithm Scheduler for SLA Activities"
    }
)

# Custom CSS with PINK theme
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 2rem;
        background-color: #fff5f7;
    }

    /* Button styling - PINK gradient */
    .stButton > button {
        background: linear-gradient(135deg, #ff6b9d 0%, #ff8fab 100%);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(255, 107, 157, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 107, 157, 0.4);
        background: linear-gradient(135deg, #ff4d8d 0%, #ff7ba3 100%);
    }

    /* Metric card styling - PINK theme */
    .metric-card {
        background: linear-gradient(135deg, #fff0f6 0%, #ffe4ec 100%);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(255, 107, 157, 0.15);
        border-left: 5px solid #ff6b9d;
        margin: 1rem 0;
        color: #5a2d47 !important;
        border: 1px solid #ffd6e3;
    }

    .metric-card h4 {
        color: #9c4665 !important;
        margin-bottom: 1rem;
        border-bottom: 2px solid #ffb8d1;
        padding-bottom: 0.5rem;
        font-size: 1.1rem;
    }

    .metric-card p {
        color: #5a2d47 !important;
        margin-bottom: 0.5rem;
        font-size: 0.95rem;
    }

    .metric-card strong {
        color: #9c4665 !important;
    }

    /* Tab styling - PINK */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #fff5f7;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 12px 12px 0 0;
        padding: 10px 20px;
        font-weight: 500;
        background-color: #ffe4ec;
        color: #9c4665;
        border: 1px solid #ffb8d1;
        margin-right: 5px;
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #ff6b9d;
        color: white;
        border-color: #ff6b9d;
    }

    /* Dataframe styling */
    .dataframe {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(255, 107, 157, 0.1);
        border: 1px solid #ffd6e3;
    }

    /* Success message styling - PINK */
    .stSuccess {
        border-radius: 12px;
        padding: 1rem;
        background-color: #ffe4ec;
        color: #9c4665;
        border: 1px solid #ffb8d1;
    }

    /* Info message styling */
    .stInfo {
        border-radius: 12px;
        padding: 1rem;
        background-color: #e8f4f8;
        color: #2c5282;
        border: 1px solid #90cdf4;
    }

    /* Warning message styling */
    .stWarning {
        border-radius: 12px;
        padding: 1rem;
        background-color: #fff5e6;
        color: #975a16;
        border: 1px solid #fed7aa;
    }

    /* Error message styling */
    .stError {
        border-radius: 12px;
        padding: 1rem;
        background-color: #ffe4e6;
        color: #9b2c2c;
        border: 1px solid #feb2b2;
    }

    /* Sidebar styling - PINK gradient */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #fff5f7 0%, #ffe4ec 100%);
        border-right: 3px solid #ffb8d1;
    }

    /* Slider styling */
    .stSlider > div > div {
        background-color: #ffd6e3;
    }

    .stSlider > div > div > div {
        background-color: #ff6b9d;
    }

    /* Checkbox styling */
    .stCheckbox > label {
        color: #5a2d47;
    }

    .stCheckbox > div > div {
        background-color: #ffd6e3;
        border-color: #ffb8d1;
    }

    .stCheckbox > div > div[aria-checked="true"] {
        background-color: #ff6b9d;
        border-color: #ff6b9d;
    }

    /* Radio button styling */
    .stRadio > div {
        background-color: #ffe4ec;
        border-radius: 10px;
        padding: 10px;
        border: 1px solid #ffb8d1;
    }

    .stRadio > div > label {
        color: #5a2d47;
    }

    .stRadio > div > div[data-baseweb="radio"] > div {
        background-color: #ffd6e3;
        border-color: #ffb8d1;
    }

    .stRadio > div > div[data-baseweb="radio"] > div[aria-checked="true"] {
        background-color: #ff6b9d;
        border-color: #ff6b9d;
    }

    /* Violation styling - PINK theme */
    .violation-perfect {
        color: #48bb78 !important;
        font-weight: bold;
    }

    .violation-good {
        color: #ff6b9d !important;
        font-weight: bold;
    }

    .violation-warning {
        color: #ed8936 !important;
        font-weight: bold;
    }

    .violation-danger {
        color: #f56565 !important;
        font-weight: bold;
    }

    /* Ensure all text is visible */
    .stMarkdown, .stText, .stDataFrame, .stMetric {
        color: #5a2d47 !important;
    }

    /* Header styling */
    h1, h2, h3 {
        color: #9c4665 !important;
    }

    /* Violation summary boxes - PINK theme */
    .violation-summary {
        background: linear-gradient(135deg, #fff0f6 0%, #ffe4ec 100%);
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        border-left: 6px solid;
        box-shadow: 0 4px 15px rgba(255, 107, 157, 0.2);
        border: 1px solid #ffd6e3;
    }

    .summary-perfect {
        border-left-color: #48bb78;
        background: linear-gradient(135deg, #f0fff4 0%, #c6f6d5 100%);
    }

    .summary-good {
        border-left-color: #ff6b9d;
        background: linear-gradient(135deg, #fff0f6 0%, #ffe4ec 100%);
    }

    .summary-warning {
        border-left-color: #ed8936;
        background: linear-gradient(135deg, #fffaf0 0%, #feebc8 100%);
    }

    .summary-danger {
        border-left-color: #f56565;
        background: linear-gradient(135deg, #fff5f5 0%, #fed7d7 100%);
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #ffe4ec;
        color: #9c4665;
        border-radius: 10px;
        border: 1px solid #ffb8d1;
    }

    .streamlit-expanderContent {
        background-color: #fff5f7;
        border-radius: 0 0 10px 10px;
        border: 1px solid #ffb8d1;
        border-top: none;
    }

    /* Footer styling */
    footer {
        color: #9c4665 !important;
    }

    /* Custom pink icons */
    .pink-icon {
        color: #ff6b9d;
    }

    /* Custom pink badges */
    .pink-badge {
        background-color: #ff6b9d;
        color: white;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if "algorithm_results" not in st.session_state:
    st.session_state.algorithm_results = None

if "execution_timestamp" not in st.session_state:
    st.session_state.execution_timestamp = None

# ============================================================================
# SIDEBAR - ALGORITHM CONTROLS
# ============================================================================

with st.sidebar:
    st.title("⚙️ Algorithm Configuration")
    st.markdown("Configure the genetic algorithm parameters below.")

    # Sidebar sections with expanders
    with st.expander("📊 Population Settings", expanded=True):
        population_size = st.slider(
            "Population Size",
            min_value=250,
            max_value=1500,
            value=250,
            step=50,
            help="Number of schedules in each generation"
        )

    with st.expander("⏱️ Generation Limits", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            min_generations = st.slider(
                "Minimum Generations",
                min_value=50,
                max_value=300,
                value=100,
                step=10,
                help="Algorithm will run at least this many generations"
            )
        with col2:
            max_generations = st.slider(
                "Maximum Generations",
                min_value=200,
                max_value=1000,
                value=500,
                step=50,
                help="Maximum generations before forced termination"
            )

    with st.expander("🧬 Genetic Operators", expanded=True):
        mutation_rate = st.slider(
            "Mutation Rate",
            min_value=0.001,
            max_value=0.05,
            value=0.01,
            step=0.001,
            format="%.3f",
            help="Probability of random changes in offspring"
        )

        crossover_method = st.radio(
            "Crossover Method",
            ["Single Point", "Uniform"],
            help="Method for combining parent schedules"
        )

        elitism_count = st.slider(
            "Elite Preserve Count",
            min_value=0,
            max_value=10,
            value=1,
            help="Number of best schedules preserved unchanged each generation"
        )

    # Run and Reset buttons
    st.markdown("---")

    col_run, col_reset = st.columns(2)

    with col_run:
        run_algorithm = st.button(
            "🚀 Run Optimization",
            type="primary",
            use_container_width=True
        )

    with col_reset:
        if st.button("🔄 Reset Results", use_container_width=True):
            st.session_state.algorithm_results = None
            st.session_state.execution_timestamp = None
            st.rerun()

    # Information section
    st.markdown("---")
    with st.expander("ℹ️ About This Algorithm"):
        st.info("""
        **Genetic Algorithm for SLA Scheduling**

        This algorithm optimizes room, time, and facilitator assignments
        for 11 SLA activities using evolutionary principles.

        **Key Features:**
        - Population-based optimization
        - Fitness-based selection
        - Crossover and mutation operators
        - Elitism preservation
        - Adaptive mutation rate

        **Termination Conditions:**
        - Minimum 100 generations
        - Improvement < 1% per generation
        """)

# ============================================================================
# MAIN CONTENT AREA
# ============================================================================

st.title("🌸 SLA Activity Scheduler")
st.markdown("### Optimize room, time, and facilitator assignments using evolutionary computation")

# ============================================================================
# ALGORITHM EXECUTION
# ============================================================================

if run_algorithm:
    with st.spinner("🚀 Executing genetic algorithm optimization... This may take a moment."):
        # Convert UI values to algorithm parameters
        crossover_strategy = "single_point" if crossover_method == "Single Point" else "uniform"

        # Execute the algorithm
        st.session_state.algorithm_results = execute_genetic_algorithm(
            population_size=population_size,
            minimum_generations=min_generations,
            maximum_generations=max_generations,
            initial_mutation_probability=mutation_rate,
            crossover_method=crossover_strategy,
            elitism_count=elitism_count,
            use_adaptive_mutation=True
        )

        # Record execution time
        st.session_state.execution_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ============================================================================
# RESULTS DISPLAY
# ============================================================================

if st.session_state.algorithm_results is not None:
    results = st.session_state.algorithm_results
    optimal_schedule = results["best_schedule"]
    generation_history = results["history"]
    total_generations = results["generations_run"]
    final_mutation_rate = results["final_mutation_rate"]

    # Convert history to DataFrame
    history_dataframe = pd.DataFrame(generation_history)

    # Format improvement percentages
    if "improvement" in history_dataframe.columns:
        history_dataframe["improvement_display"] = history_dataframe["improvement"].apply(
            lambda x: f"{x:.2f}%" if x is not None and not pd.isna(x) else "N/A"
        )

    # ========================================================================
    # SUCCESS MESSAGE AND SUMMARY METRICS
    # ========================================================================
    st.success(f"""
    ✅ **Optimization Completed Successfully!**

    **Execution Summary:**
    - **Total Generations:** {total_generations}
    - **Final Mutation Rate:** {final_mutation_rate:.4f}
    - **Best Fitness Score:** {history_dataframe["best"].iloc[-1]:.2f}
    - **Average Fitness:** {history_dataframe["avg"].iloc[-1]:.2f}
    - **Completion Time:** {st.session_state.execution_timestamp}
    """)

    # ========================================================================
    # TABBED INTERFACE FOR DIFFERENT VIEWS
    # ========================================================================
    analysis_tab, schedule_tab, violations_tab, data_tab = st.tabs([
        "📈 Fitness Analysis",
        "🌸 Optimal Schedule",
        "⚠️ Constraint Analysis",
        "📊 Data Export"
    ])

    # ========================================================================
    # TAB 1: FITNESS ANALYSIS
    # ========================================================================
    with analysis_tab:
        st.subheader("Fitness Evolution Over Generations")

        # Create fitness plot with pink theme
        fig, axes = plt.subplots(1, 2, figsize=(16, 5))

        # Set pink theme for matplotlib
        plt.rcParams['axes.prop_cycle'] = plt.cycler(color=['#ff6b9d', '#ff8fab', '#ffb8d1', '#ffd6e3'])

        # Plot 1: All fitness lines
        axes[0].plot(history_dataframe["generation"], history_dataframe["best"],
                     label="Best Fitness", linewidth=3, color='#ff6b9d', alpha=0.8)
        axes[0].plot(history_dataframe["generation"], history_dataframe["avg"],
                     label="Average Fitness", linewidth=2, color='#ff8fab', linestyle='--', alpha=0.8)
        axes[0].plot(history_dataframe["generation"], history_dataframe["worst"],
                     label="Worst Fitness", linewidth=1.5, color='#ffb8d1', linestyle=':', alpha=0.7)

        axes[0].fill_between(history_dataframe["generation"],
                             history_dataframe["avg"], history_dataframe["best"],
                             alpha=0.1, color='#ff6b9d')

        axes[0].set_xlabel("Generation Number", fontsize=12, fontweight='bold', color='#9c4665')
        axes[0].set_ylabel("Fitness Score", fontsize=12, fontweight='bold', color='#9c4665')
        axes[0].set_title("Fitness Progression", fontsize=14, fontweight='bold', color='#9c4665')
        axes[0].grid(True, alpha=0.2, linestyle='--', color='#ffd6e3')
        axes[0].legend(loc='lower right', framealpha=0.9)
        axes[0].tick_params(axis='both', which='major', labelsize=10, colors='#5a2d47')
        axes[0].set_facecolor('#fff5f7')
        axes[0].spines['bottom'].set_color('#ffb8d1')
        axes[0].spines['top'].set_color('#ffb8d1')
        axes[0].spines['left'].set_color('#ffb8d1')
        axes[0].spines['right'].set_color('#ffb8d1')

        # Plot 2: Improvement percentage
        if "improvement" in history_dataframe.columns:
            valid_improvements = history_dataframe["improvement"].dropna()
            if not valid_improvements.empty:
                axes[1].plot(valid_improvements.index, valid_improvements.values,
                             color='#ff6b9d', linewidth=2, marker='o', markersize=4)
                axes[1].axhline(y=1.0, color='#ff8fab', linestyle='--', alpha=0.5,
                                label='1% Threshold')
                axes[1].fill_between(valid_improvements.index, 0, valid_improvements.values,
                                     where=(valid_improvements.values >= 0),
                                     color='#ffe4ec', alpha=0.5, label='Positive Improvement')
                axes[1].fill_between(valid_improvements.index, 0, valid_improvements.values,
                                     where=(valid_improvements.values < 0),
                                     color='#ffd6e3', alpha=0.5, label='Negative Improvement')

                axes[1].set_xlabel("Generation", fontsize=12, fontweight='bold', color='#9c4665')
                axes[1].set_ylabel("Improvement (%)", fontsize=12, fontweight='bold', color='#9c4665')
                axes[1].set_title("Generation-to-Generation Improvement",
                                  fontsize=14, fontweight='bold', color='#9c4665')
                axes[1].grid(True, alpha=0.2, linestyle='--', color='#ffd6e3')
                axes[1].legend(framealpha=0.9)
                axes[1].tick_params(axis='both', which='major', labelsize=10, colors='#5a2d47')
                axes[1].set_facecolor('#fff5f7')
                axes[1].spines['bottom'].set_color('#ffb8d1')
                axes[1].spines['top'].set_color('#ffb8d1')
                axes[1].spines['left'].set_color('#ffb8d1')
                axes[1].spines['right'].set_color('#ffb8d1')

        plt.tight_layout()
        st.pyplot(fig)

        # Display detailed metrics
        with st.expander("📊 View Detailed Generation Metrics"):
            display_columns = ["generation", "best", "avg", "worst"]
            if "improvement_display" in history_dataframe.columns:
                display_columns.append("improvement_display")

            st.dataframe(
                history_dataframe[display_columns].rename(
                    columns={
                        "generation": "Generation",
                        "best": "Best Fitness",
                        "avg": "Average Fitness",
                        "worst": "Worst Fitness",
                        "improvement_display": "Improvement %"
                    }
                ).style.set_properties(**{
                    'background-color': '#fff5f7',
                    'color': '#5a2d47',
                    'border': '1px solid #ffd6e3'
                }),
                use_container_width=True,
                height=400
            )

    # ========================================================================
    # TAB 2: OPTIMAL SCHEDULE
    # ========================================================================
    with schedule_tab:
        st.subheader("Optimal Schedule Configuration")

        # Schedule display controls
        col_controls1, col_controls2, col_controls3 = st.columns([2, 2, 1])

        with col_controls1:
            display_limit = st.radio(
                "Activities to Display:",
                ["First 6 Activities", "All Activities"],
                horizontal=True
            )

        with col_controls2:
            sort_preference = st.radio(
                "Sort Schedule By:",
                ["Time Slot", "Activity Name"],
                horizontal=True
            )

        with col_controls3:
            show_groupings = st.checkbox("Show Groupings", value=False)

        # Convert schedule to DataFrame
        schedule_df = optimal_schedule.to_dataframe()

        # Apply sorting
        time_order_mapping = {
            "10 AM": 1, "11 AM": 2, "12 PM": 3,
            "1 PM": 4, "2 PM": 5, "3 PM": 6
        }

        if sort_preference == "Time Slot":
            schedule_df["Sort_Key"] = schedule_df["Time"].map(time_order_mapping)
            schedule_df = schedule_df.sort_values(["Sort_Key", "Activity"]).drop(columns=["Sort_Key"])
        else:
            schedule_df = schedule_df.sort_values("Activity")

        # Apply display limit
        if display_limit == "First 6 Activities":
            display_df = schedule_df.head(6)
        else:
            display_df = schedule_df

        # Display schedule with pink styling
        st.dataframe(
            display_df.style.set_properties(**{
                'background-color': '#fff5f7',
                'color': '#5a2d47',
                'border': '1px solid #ffd6e3'
            }).set_table_styles([
                {'selector': 'thead th', 'props': [('background-color', '#ffe4ec'),
                                                   ('color', '#9c4665'),
                                                   ('border', '1px solid #ffb8d1')]},
                {'selector': 'tbody tr:nth-child(even)', 'props': [('background-color', '#ffe4ec')]},
                {'selector': 'tbody tr:nth-child(odd)', 'props': [('background-color', '#fff5f7')]},
            ]),
            use_container_width=True,
            height=400
        )

        # Optional groupings
        if show_groupings:
            st.subheader("Schedule Groupings")

            grouping_col1, grouping_col2 = st.columns(2)

            with grouping_col1:
                with st.expander("🏫 Group by Room", expanded=False):
                    for room_name, room_group in schedule_df.groupby("Room"):
                        st.markdown(f"**<span style='color:#ff6b9d'>Room: {room_name}</span>**", unsafe_allow_html=True)
                        st.dataframe(room_group.style.set_properties(**{
                            'background-color': '#fff5f7',
                            'color': '#5a2d47',
                            'border': '1px solid #ffd6e3'
                        }), use_container_width=True)

            with grouping_col2:
                with st.expander("🧑‍🏫 Group by Facilitator", expanded=False):
                    for facilitator_name, fac_group in schedule_df.groupby("Facilitator"):
                        st.markdown(f"**<span style='color:#ff6b9d'>Facilitator: {facilitator_name}</span>**",
                                    unsafe_allow_html=True)
                        st.dataframe(fac_group.style.set_properties(**{
                            'background-color': '#fff5f7',
                            'color': '#5a2d47',
                            'border': '1px solid #ffd6e3'
                        }), use_container_width=True)

    # ========================================================================
    # TAB 3: CONSTRAINT VIOLATIONS - PINK THEME
    # ========================================================================
    with violations_tab:
        st.subheader("Constraint Violation Analysis")

        # Calculate violations
        violation_summary = fitness_calculator.calculate_constraint_violations(optimal_schedule)


        # Helper function to format violation count with pink icons
        def format_violation_count(count):
            """Format violation count with appropriate icon and color."""
            if count == 0:
                return f'<span class="violation-perfect">✓ 0</span>'
            elif count <= 2:
                return f'<span class="violation-good">🌸 {count}</span>'
            else:
                return f'<span class="violation-danger">💥 {count}</span>'


        # Display violations in two columns
        violation_col1, violation_col2 = st.columns(2)

        with violation_col1:
            st.markdown("#### 🏫 Room & Time Violations")
            st.markdown(f"""
            <div class='metric-card'>
            <h4>🏛️ Room Issues</h4>
            <p><strong>Room Conflicts:</strong> {format_violation_count(violation_summary['room_conflicts'])}</p>
            <p><strong>Room Too Small:</strong> {format_violation_count(violation_summary['room_too_small'])}</p>
            <p><strong>Room Too Big (>1.5x):</strong> {format_violation_count(violation_summary['room_too_big_15'])}</p>
            <p><strong>Room Too Big (>3x):</strong> {format_violation_count(violation_summary['room_too_big_30'])}</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class='metric-card'>
            <h4>⏰ Time Slot Issues</h4>
            <p><strong>SLA101 Sections Same Time:</strong> {format_violation_count(violation_summary['sla101_same_time'])}</p>
            <p><strong>SLA191 Sections Same Time:</strong> {format_violation_count(violation_summary['sla191_same_time'])}</p>
            <p><strong>SLA101/SLA191 Same Time:</strong> {format_violation_count(violation_summary['sla101_191_same_time'])}</p>
            </div>
            """, unsafe_allow_html=True)

        with violation_col2:
            st.markdown("#### 👨‍🏫 Facilitator & Interactions")
            st.markdown(f"""
            <div class='metric-card'>
            <h4>🧑‍🏫 Facilitator Issues</h4>
            <p><strong>Facilitator Overload (>4):</strong> {format_violation_count(violation_summary['facilitator_overload'])}</p>
            <p><strong>Facilitator Underload (<3):</strong> {format_violation_count(violation_summary['facilitator_underload'])}</p>
            <p><strong>Same-Time Conflicts:</strong> {format_violation_count(violation_summary['facilitator_same_time_conflict'])}</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class='metric-card'>
            <h4>🔄 SLA101 ↔ SLA191 Interactions</h4>
            <p><strong>Consecutive Pairs:</strong> {format_violation_count(violation_summary['sla101_191_consecutive_pair'])}</p>
            <p><strong>Building Mismatch:</strong> {format_violation_count(violation_summary['sla101_191_building_mismatch'])}</p>
            <p><strong>One Hour Gap:</strong> {format_violation_count(violation_summary['sla101_191_one_hour_gap'])}</p>
            </div>
            """, unsafe_allow_html=True)

        # Violation summary with pink styling
        total_violations = sum(violation_summary.values())

        # Determine which summary class to use
        if total_violations == 0:
            summary_class = "summary-perfect"
            summary_icon = "🎉"
            summary_title = "Perfect Schedule!"
            summary_message = "No constraint violations detected. This schedule satisfies all Appendix A requirements."
        elif total_violations <= 3:
            summary_class = "summary-good"
            summary_icon = "🌸"
            summary_title = "Good Schedule"
            summary_message = f"Only {total_violations} minor constraint issues. This is a high-quality schedule with minimal violations."
        elif total_violations <= 6:
            summary_class = "summary-warning"
            summary_icon = "🌺"
            summary_title = "Acceptable Schedule"
            summary_message = f"{total_violations} constraint issues identified. Consider re-running optimization for better results."
        else:
            summary_class = "summary-danger"
            summary_icon = "💥"
            summary_title = "Poor Schedule"
            summary_message = f"{total_violations} constraint violations! This schedule has significant issues. Re-run optimization."

        # Display the summary
        st.markdown(f"""
        <div class="violation-summary {summary_class}">
            <h3 style="margin-top: 0; color: #9c4665;">{summary_icon} {summary_title}</h3>
            <p style="color: #5a2d47; font-size: 1.1em;"><strong>Total Violations:</strong> <span style="color: #ff6b9d; font-weight: bold;">{total_violations}</span></p>
            <p style="color: #5a2d47;">{summary_message}</p>
        </div>
        """, unsafe_allow_html=True)

        # Add detailed explanation with pink styling
        with st.expander("📖 Understanding Constraint Violations", expanded=False):
            st.markdown("""
            <div style="background-color: #fff5f7; padding: 20px; border-radius: 10px; border: 1px solid #ffd6e3;">
            ### 🎀 Violation Type Explanations:

            **🏛️ Room Issues:**
            - **Room Conflicts**: Multiple activities in same room at same time
            - **Room Too Small**: Room capacity < expected enrollment
            - **Room Too Big (>1.5x)**: Room is 1.5-3x larger than needed (minor issue)
            - **Room Too Big (>3x)**: Room is >3x larger than needed (major issue)

            **⏰ Time Issues:**
            - **SLA101 Sections Same Time**: SLA101A and SLA101B scheduled simultaneously
            - **SLA191 Sections Same Time**: SLA191A and SLA191B scheduled simultaneously  
            - **SLA101/SLA191 Same Time**: Related courses at same time

            **🧑‍🏫 Facilitator Issues:**
            - **Overload (>4)**: Facilitator assigned to >4 activities
            - **Underload (<3)**: Facilitator assigned to <3 activities (except Tyler)
            - **Same-Time Conflicts**: Same facilitator in multiple rooms simultaneously

            **🔄 SLA101 ↔ SLA191 Interactions:**
            - **Consecutive Pairs**: Should be in consecutive time slots (e.g., 10 AM & 11 AM)
            - **Building Mismatch**: Consecutive pairs in different building types (Beach/Roman vs others)
            - **One Hour Gap**: Exactly one hour between pairs (e.g., 10 AM & 12 PM)
            </div>
            """, unsafe_allow_html=True)

    # ========================================================================
    # TAB 4: DATA EXPORT
    # ========================================================================
    with data_tab:
        st.subheader("Data Export and Download")

        # Schedule export
        st.markdown("### 🌸 Schedule Export")
        schedule_csv = schedule_df.to_csv(index=False).encode('utf-8')

        col_schedule1, col_schedule2 = st.columns(2)

        with col_schedule1:
            st.download_button(
                label="📥 Download Schedule (CSV)",
                data=schedule_csv,
                file_name=f"sla_schedule_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )

        with col_schedule2:
            # Save schedule to file
            output_filename = f"output/sla_optimal_schedule_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            optimal_schedule.save_to_csv(output_filename)
            st.success(f"✅ Schedule saved to: `{output_filename}`")

        # History export
        st.markdown("### 📈 History Data Export")
        history_csv = history_dataframe.to_csv(index=False).encode('utf-8')

        col_history1, col_history2 = st.columns(2)

        with col_history1:
            st.download_button(
                label="📥 Download Fitness History (CSV)",
                data=history_csv,
                file_name=f"fitness_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )

        with col_history2:
            # Display sample of history data
            with st.expander("👁️ Preview History Data"):
                st.dataframe(history_dataframe.head(10).style.set_properties(**{
                    'background-color': '#fff5f7',
                    'color': '#5a2d47',
                    'border': '1px solid #ffd6e3'
                }), use_container_width=True)

        # Violations export
        st.markdown("### ⚠️ Violations Export")
        violations_df = pd.DataFrame([violation_summary])

        col_viol1, col_viol2 = st.columns(2)

        with col_viol1:
            violations_csv = violations_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Violations Report (CSV)",
                data=violations_csv,
                file_name=f"violations_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )

        with col_viol2:
            st.markdown("#### 📋 Violations Summary")
            st.json(violation_summary)

# ========================================================================
# INITIAL STATE (NO RESULTS YET)
# ========================================================================
else:
    st.markdown("""
    <div style="background-color: #fff5f7; padding: 30px; border-radius: 15px; border: 2px solid #ffd6e3; margin-bottom: 30px;">
    ## 🚀 Welcome to the SLA Activity Scheduler

    This application uses a **genetic algorithm** to optimize scheduling for 
    the Seminar Learning Association (SLA). The algorithm will find the best 
    assignments of rooms, time slots, and facilitators for all 11 activities.

    ### 📋 How to Use:
    1. **Configure parameters** in the sidebar on the left
    2. **Click "Run Optimization"** to start the genetic algorithm
    3. **View results** in the tabs that appear after completion

    ### ⚙️ Key Parameters to Configure:
    - **Population Size**: Number of schedules in each generation
    - **Mutation Rate**: Probability of random changes
    - **Generation Limits**: Minimum and maximum evolution cycles
    - **Crossover Method**: How parent schedules are combined
    - **Elite Count**: Number of best schedules preserved each generation

    ### 🎯 Algorithm Features:
    - ✅ Implements all Appendix A fitness rules
    - ✅ Adaptive mutation rate adjustment
    - ✅ Softmax-based parent selection
    - ✅ Single-point and uniform crossover
    - ✅ Elitism for preserving best solutions
    - ✅ Automatic termination when improvement < 1%

    **Ready to begin? Configure your parameters and click "Run Optimization"!**
    </div>
    """, unsafe_allow_html=True)

    # Quick start example
    with st.expander("🎯 Quick Start Recommendation", expanded=True):
        st.markdown("""
        <div style="background-color: #ffe4ec; padding: 20px; border-radius: 10px; border: 1px solid #ffb8d1;">
        **🌸 For best results, try these settings:**
        - Population Size: **300**
        - Minimum Generations: **100**
        - Maximum Generations: **500**
        - Mutation Rate: **0.01**
        - Crossover Method: **Single Point**
        - Elite Preserve Count: **2**

        These values balance exploration and convergence for most scenarios.
        </div>
        """, unsafe_allow_html=True)

# ========================================================================
# FOOTER
# ========================================================================
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #ff6b9d; font-size: 0.9em; padding: 20px; background-color: #fff5f7; border-radius: 10px; border: 1px solid #ffd6e3;'>"
    "🌸 Genetic Algorithm Scheduler for SLA Activities | "
    f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    "</div>",
    unsafe_allow_html=True
)