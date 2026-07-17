import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Computer Hardware Price Crisis Dashboard",
    page_icon="💾",
    layout="wide",
)

# Main title
st.title("💾 Computer Hardware Price Crisis Data Analysis")
st.markdown("---")

# ============================================================
# Executive Summary
# ============================================================
st.header("📋 Executive Summary")
st.markdown("""
This data science project analyzes a simulated global RAM (memory module) market during a
**memory shortage crisis**, covering 10,000 memory kits sold across brands, regions, and
generations of DRAM technology (DDR4, DDR5, and the upcoming DDR6). The analysis aims to
uncover pricing trends, supply dynamics, and performance characteristics that define the
memory shortage crisis.

**Key Objectives:**
- Understand pricing patterns across brands, generations, and regions
- Analyze the relationship between memory capacity, speed, and price
- Track how prices have evolved over time during the shortage
- Examine performance/latency characteristics and recommended usage segments
- Identify which brands and models are most exposed to shortage-driven inflation

**Expected Deliverables:**
- Interactive Plotly visualizations covering pricing, capacity, and performance
- Statistical summaries of key market indicators
- Actionable insights for buyers, retailers, and market analysts
""")

st.markdown("---")

# ============================================================
# Project Description
# ============================================================
st.header("📖 Project Description")

st.subheader("❗ Problem Statement")
st.markdown("""
Global memory (RAM) markets have experienced severe supply shortages, causing price spikes,
inventory shocks, and shifting demand toward AI/enterprise-grade memory. This project uses a
synthetic but realistic RAM market dataset to help:

- **Buyers & Builders**: Understand which brands/generations offer the best value during the shortage
- **Retailers**: Identify pricing trends and inventory risk by region and brand
- **Market Analysts**: Track how shortage-driven pricing behaves across capacities and speeds
- **Manufacturers**: Understand demand concentration across recommended-usage segments
""")

st.subheader("🗂️ Dataset Overview")
st.markdown("""
The dataset contains detailed information about individual RAM kits, including:

**Core Identification:**
- `kit_id`, `brand`, `model_name`, `timestamp`, `region`

**Technical Specifications:**
- `generation` (DDR4 / DDR5 / DDR6 Preview), `form_factor`, `capacity_gb`, `module_count`,
  `is_ecc`, `speed_mts`, `cas_latency`, `voltage`, `timing_string`, `die_manufacturer`, `die_type`

**Performance Metrics:**
- `true_latency_ns`, `bandwidth_per_dollar`, `latency_value_index`, `speed_premium_ratio`

**Pricing & Market Data:**
- `price_per_gb`, `price_usd`, `market_segment`, `recommended_usage`, `price_status`

**Supply-Side Indicators:**
- `global_inventory_weeks`, `fab_utilization_rate`, `gpu_hbm_trend_gb`
""")

st.markdown("---")

# ============================================================
# Data Overview Section
# ============================================================
st.header("📊 Data Overview")


@st.cache_data
def load_data():
    """Load the RAM Memory Shortage Crisis dataset with caching"""
    try:
        df = pd.read_csv('Ultimate_Memory_Shortage_Crisis_Dataset_10k.csv')
        return df
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return None

@st.cache_data
def prepare_dataframe_for_display(df, max_string_length=100):
    """Prepare dataframe for display, avoiding Arrow serialization issues"""
    if df is None or df.empty:
        return df
    try:
        df_display = df.copy()
        for col in df_display.columns:
            if df_display[col].dtype == 'object' or pd.api.types.is_object_dtype(df_display[col]):
                df_display[col] = df_display[col].astype(str)
                df_display[col] = df_display[col].replace(['nan', 'None', 'NaN', '<NA>', 'null'], '')
                mask = df_display[col].str.len() > max_string_length
                if mask.any():
                    df_display.loc[mask, col] = df_display.loc[mask, col].str[:max_string_length] + '...'
        return df_display
    except Exception as e:
        st.warning(f"DataFrame conversion warning: {str(e)}. Using fallback conversion.")
        df_fallback = df.copy()
        for col in df_fallback.columns:
            df_fallback[col] = df_fallback[col].astype(str)
        return df_fallback


df = load_data()

if df is not None:
    # Parse timestamp as datetime for time-series charting
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

    st.subheader("ℹ️ Dataset Basic Information")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Records", f"{df.shape[0]:,}")
    with col2:
        st.metric("Total Columns", df.shape[1])
    with col3:
        st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
    with col4:
        st.metric("Unique Brands", df['brand'].nunique())

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📝 Column Info",
        "🚨 Missing Values",
        "📄 Sample Data",
        "📈 Statistics",
        "🏷️ Categorical Data",
    ])

    with tab1:
        st.subheader("📝 Column Information")
        col_info = pd.DataFrame({
            'Column Name': df.columns,
            'Data Type': df.dtypes.astype(str),
            'Non-Null Count': df.count(),
            'Null Count': df.isnull().sum(),
            'Null Percentage': (df.isnull().sum() / len(df) * 100).round(2)
        })
        st.dataframe(prepare_dataframe_for_display(col_info), use_container_width=True)

    with tab2:
        st.subheader("🚨 Missing Values Analysis")
        missing_data = df.isnull().sum().sort_values(ascending=False)
        missing_data = missing_data[missing_data > 0]
        if not missing_data.empty:
            missing_df = pd.DataFrame({
                'Column': missing_data.index,
                'Missing Count': missing_data.values,
                'Missing Percentage': (missing_data.values / len(df) * 100).round(2)
            })
            st.dataframe(prepare_dataframe_for_display(missing_df), use_container_width=True)
        else:
            st.success("No missing values found in the dataset!")

    with tab3:
        st.subheader("📄 Sample Data")
        st.write("First 10 rows of the dataset:")
        st.dataframe(prepare_dataframe_for_display(df.head(10)), use_container_width=True)
        st.write("Random Sample (10 rows):")
        st.dataframe(prepare_dataframe_for_display(df.sample(10)), use_container_width=True)

    with tab4:
        st.subheader("📈 Statistical Summary")
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        if len(numerical_cols) > 0:
            st.write("**Numerical Columns Statistics:**")
            st.dataframe(prepare_dataframe_for_display(df[numerical_cols].describe()), use_container_width=True)

    with tab5:
        st.subheader("🏷️ Categorical Data Analysis")
        categorical_cols = ['brand', 'generation', 'region', 'market_segment', 'recommended_usage', 'price_status']
        for col in categorical_cols:
            if col in df.columns:
                unique_count = df[col].nunique()
                st.write(f"**{col}**: {unique_count} unique values")
                value_counts = df[col].value_counts()
                st.dataframe(prepare_dataframe_for_display(value_counts.reset_index()), use_container_width=True)
                st.write("---")
else:
    st.error("Could not load the dataset. Please ensure the CSV file is in the correct directory.")

st.markdown("---")

# ============================================================
# Data Visualization Section
# ============================================================
st.header("📉 Data Visualization & Insights")

if df is not None:
    df_viz = df.copy()

    # ---------------- Sidebar Filters ----------------
    st.sidebar.header("Data Filters")
    st.sidebar.markdown("Use these filters to explore specific segments of the data.")
    st.sidebar.markdown("---")

    with st.sidebar.form("filters_form"):
        st.subheader("Product Filters")

        brands = sorted(df_viz['brand'].dropna().unique().tolist())
        selected_brands = st.multiselect("Select Brand(s)", brands, help="Filter by RAM brand")

        generations = sorted(df_viz['generation'].dropna().unique().tolist())
        selected_generations = st.multiselect("Select Generation(s)", generations, help="Filter by DDR generation")

        regions = sorted(df_viz['region'].dropna().unique().tolist())
        selected_regions = st.multiselect("Select Region(s)", regions, help="Filter by sales region")

        st.markdown("---")
        st.subheader("Price & Capacity Filters")

        min_price, max_price = float(df_viz['price_usd'].min()), float(df_viz['price_usd'].max())
        price_range = st.slider("Price Range (USD)", min_value=min_price, max_value=max_price,
                                 value=(min_price, max_price))

        min_cap, max_cap = int(df_viz['capacity_gb'].min()), int(df_viz['capacity_gb'].max())
        capacity_range = st.slider("Capacity Range (GB)", min_value=min_cap, max_value=max_cap,
                                    value=(min_cap, max_cap))

        st.markdown("---")
        col_a, col_b = st.columns(2)
        with col_a:
            apply_filters = st.form_submit_button("✅ Apply Filters", type="primary", use_container_width=True)
        with col_b:
            reset_filters = st.form_submit_button("🔄 Reset Filters", use_container_width=True)

    if 'filters_applied' not in st.session_state:
        st.session_state.filters_applied = False

    if reset_filters:
        st.session_state.filters_applied = False
        st.rerun()

    if apply_filters:
        st.session_state.filters_applied = True
        st.session_state.sel_brands = selected_brands
        st.session_state.sel_generations = selected_generations
        st.session_state.sel_regions = selected_regions
        st.session_state.sel_price_range = price_range
        st.session_state.sel_capacity_range = capacity_range

    if st.session_state.filters_applied:
        if st.session_state.sel_brands:
            df_viz = df_viz[df_viz['brand'].isin(st.session_state.sel_brands)]
        if st.session_state.sel_generations:
            df_viz = df_viz[df_viz['generation'].isin(st.session_state.sel_generations)]
        if st.session_state.sel_regions:
            df_viz = df_viz[df_viz['region'].isin(st.session_state.sel_regions)]
        df_viz = df_viz[
            (df_viz['price_usd'] >= st.session_state.sel_price_range[0]) &
            (df_viz['price_usd'] <= st.session_state.sel_price_range[1])
        ]
        df_viz = df_viz[
            (df_viz['capacity_gb'] >= st.session_state.sel_capacity_range[0]) &
            (df_viz['capacity_gb'] <= st.session_state.sel_capacity_range[1])
        ]
        st.sidebar.success(f"Showing {len(df_viz):,} of {len(df):,} kits")
    else:
        st.sidebar.info("Filters not applied yet — showing full dataset.")

    if len(df_viz) == 0:
        st.error("No records match your current filter criteria. Please adjust your filters.")
        st.stop()

    # ---------------- Dynamic Metrics ----------------
    st.subheader("Filtered Data Overview")
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.metric("RAM Kits", f"{len(df_viz):,}")
    with m2:
        st.metric("Avg Price", f"${df_viz['price_usd'].mean():,.2f}")
    with m3:
        st.metric("Avg Capacity", f"{df_viz['capacity_gb'].mean():.0f} GB")
    with m4:
        st.metric("Avg Speed", f"{df_viz['speed_mts'].mean():,.0f} MT/s")
    with m5:
        shortage_pct = (df_viz['price_status'] == 'Shortage-Inflated').mean() * 100
        st.metric("Shortage-Inflated", f"{shortage_pct:.0f}%")

    st.markdown("---")

    # ============================================================
    # Chart 1: Average RAM Price by Brand (px.bar)
    # ============================================================
    st.subheader("1. 💲 Average RAM Price by Brand")
    brand_price = df_viz.groupby('brand', as_index=False)['price_usd'].mean().sort_values('price_usd', ascending=False)
    fig1 = px.bar(
        brand_price, x='brand', y='price_usd',
        title="Average RAM Price by Brand",
        labels={'brand': 'Brand', 'price_usd': 'Average Price (USD)'},
        color='price_usd', color_continuous_scale='viridis', text_auto='.2s'
    )
    fig1.update_layout(height=500, xaxis_tickangle=-45, showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)
    st.write(f"**Key Insight:** **{brand_price.iloc[0]['brand']}** has the highest average price "
             f"(${brand_price.iloc[0]['price_usd']:,.2f}), while **{brand_price.iloc[-1]['brand']}** "
             f"has the lowest (${brand_price.iloc[-1]['price_usd']:,.2f}).")

    st.markdown("---")

    # ============================================================
    # Chart 2: Memory Capacity Distribution (px.histogram)
    # ============================================================
    st.subheader("2. 📦 Memory Capacity Distribution")
    fig2 = px.histogram(
        df_viz, x='capacity_gb', nbins=30,
        title="Distribution of Memory Kit Capacities",
        labels={'capacity_gb': 'Capacity (GB)', 'count': 'Number of Kits'},
        color_discrete_sequence=['#4ecdc4']
    )
    median_cap = df_viz['capacity_gb'].median()
    fig2.add_vline(x=median_cap, line_dash="dash", line_color="red",
                    annotation_text=f"Median: {median_cap:.0f} GB")
    fig2.update_layout(height=500)
    st.plotly_chart(fig2, use_container_width=True)
    st.write(f"**Key Insight:** The median memory capacity is **{median_cap:.0f} GB**, with the most "
              f"common capacity being **{int(df_viz['capacity_gb'].mode()[0])} GB**.")

    st.markdown("---")

    # ============================================================
    # Chart 3: Price vs Capacity (px.scatter)
    # ============================================================
    st.subheader("3. 📈 Price vs Capacity")
    sample_size = min(3000, len(df_viz))
    df_sample = df_viz.sample(sample_size, random_state=42)
    fig3 = px.scatter(
        df_sample, x='capacity_gb', y='price_usd',
        title="Price vs Capacity",
        labels={'capacity_gb': 'Capacity (GB)', 'price_usd': 'Price (USD)'},
        color='generation', opacity=0.6,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig3.update_layout(height=550)
    st.plotly_chart(fig3, use_container_width=True)
    corr = df_viz[['capacity_gb', 'price_usd']].corr().iloc[0, 1]
    st.write(f"**Key Insight:** Correlation between capacity and price is **{corr:.3f}** — "
              f"larger-capacity kits generally command higher prices, especially in enterprise/AI segments.")

    st.markdown("---")

    # ============================================================
    # Chart 4: Price Trend Over Time (px.line)
    # ============================================================
    st.subheader("4. 📅 Price Trend Over Time")
    price_trend = df_viz.dropna(subset=['timestamp']).copy()
    price_trend['month'] = price_trend['timestamp'].dt.to_period('M').dt.to_timestamp()
    monthly_price = price_trend.groupby('month', as_index=False)['price_usd'].mean()
    fig4 = px.line(
        monthly_price, x='month', y='price_usd',
        title="Average RAM Price Trend Over Time",
        labels={'month': 'Month', 'price_usd': 'Average Price (USD)'},
        markers=True
    )
    fig4.update_layout(height=500)
    st.plotly_chart(fig4, use_container_width=True)
    if len(monthly_price) > 1:
        change_pct = ((monthly_price['price_usd'].iloc[-1] - monthly_price['price_usd'].iloc[0])
                      / monthly_price['price_usd'].iloc[0] * 100)
        trend_word = "increased" if change_pct > 0 else "decreased"
        st.write(f"**Key Insight:** Average price has **{trend_word} by {abs(change_pct):.1f}%** "
                  f"from {monthly_price['month'].iloc[0].strftime('%b %Y')} to "
                  f"{monthly_price['month'].iloc[-1].strftime('%b %Y')}.")

    st.markdown("---")

    # ============================================================
    # Chart 5: Price Distribution by Brand (px.box)
    # ============================================================
    st.subheader("5. 📊 Price Distribution by Brand")
    fig5 = px.box(
        df_viz, x='brand', y='price_usd',
        title="Price Distribution by Brand",
        labels={'brand': 'Brand', 'price_usd': 'Price (USD)'},
        color='brand', color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig5.update_layout(height=550, xaxis_tickangle=-45, showlegend=False)
    st.plotly_chart(fig5, use_container_width=True)
    widest_brand = df_viz.groupby('brand')['price_usd'].std().idxmax()
    st.write(f"**Key Insight:** **{widest_brand}** shows the widest price variability, indicating a "
              f"broad range of product tiers within that brand.")

    st.markdown("---")

    # ============================================================
    # Chart 6: RAM Generation Distribution (px.pie / donut)
    # ============================================================
    st.subheader("6. 💾 RAM Generation Distribution")
    gen_counts = df_viz['generation'].value_counts()
    fig6 = px.pie(
        values=gen_counts.values, names=gen_counts.index,
        title="Distribution of RAM Generations",
        hole=0.4, color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig6.update_traces(textposition='inside', textinfo='percent+label')
    fig6.update_layout(height=500)
    st.plotly_chart(fig6, use_container_width=True)
    st.write(f"**Key Insight:** **{gen_counts.index[0]}** is the most common generation, representing "
              f"**{gen_counts.iloc[0] / gen_counts.sum() * 100:.1f}%** of all kits.")

    st.markdown("---")

    # ============================================================
    # Chart 7: Brand → Model Hierarchy (px.treemap)
    # ============================================================
    st.subheader("7. 🌳 Brand → Model Hierarchy")
    treemap_data = df_viz.groupby(['brand', 'model_name'], as_index=False)['price_usd'].mean()
    top_models = treemap_data.sort_values('price_usd', ascending=False).groupby('brand').head(5)
    fig7 = px.treemap(
        top_models, path=['brand', 'model_name'], values='price_usd',
        title="Brand → Model Hierarchy (Top 5 Models per Brand by Avg Price)",
        color='price_usd', color_continuous_scale='blues'
    )
    fig7.update_layout(height=600)
    st.plotly_chart(fig7, use_container_width=True)
    st.write("**Key Insight:** The treemap shows how average pricing is distributed across brands and "
              "their top models — larger tiles represent higher average prices.")

    st.markdown("---")

    # ============================================================
    # Chart 8: Recommended Usage Breakdown (px.sunburst)
    # ============================================================
    st.subheader("8. 🎯 Recommended Usage Breakdown")
    sunburst_data = df_viz.groupby(['recommended_usage', 'brand', 'generation'], as_index=False).size()
    fig8 = px.sunburst(
        sunburst_data, path=['recommended_usage', 'brand', 'generation'], values='size',
        title="Recommended Usage → Brand → Generation Breakdown",
        color='size', color_continuous_scale='sunset'
    )
    fig8.update_layout(height=650)
    st.plotly_chart(fig8, use_container_width=True)
    top_usage = df_viz['recommended_usage'].value_counts().idxmax()
    st.write(f"**Key Insight:** **{top_usage}** is the most common recommended usage segment across "
              f"brands and generations in the current data.")

    st.markdown("---")

    # ============================================================
    # Chart 9: Speed vs Price (px.scatter)
    # ============================================================
    st.subheader("9. ⚡ Speed vs Price")
    fig9 = px.scatter(
        df_sample, x='speed_mts', y='price_usd',
        title="Memory Speed vs Price",
        labels={'speed_mts': 'Speed (MT/s)', 'price_usd': 'Price (USD)'},
        color='market_segment', opacity=0.6,
        color_discrete_sequence=['#e74c3c', '#2ecc71']
    )
    fig9.update_layout(height=550)
    st.plotly_chart(fig9, use_container_width=True)
    speed_corr = df_viz[['speed_mts', 'price_usd']].corr().iloc[0, 1]
    st.write(f"**Key Insight:** Correlation between speed and price is **{speed_corr:.3f}** — "
              f"higher-speed kits tend to be priced higher, particularly in enterprise/AI segments.")

    st.markdown("---")

    # ============================================================
    # Chart 10: Capacity Distribution by Brand (px.violin)
    # ============================================================
    st.subheader("10. 📦 Capacity Distribution by Brand")
    fig10 = px.violin(
        df_viz, x='brand', y='capacity_gb',
        title="Capacity Distribution by Brand",
        labels={'brand': 'Brand', 'capacity_gb': 'Capacity (GB)'},
        color='brand', color_discrete_sequence=px.colors.qualitative.Set1,
        box=True, points="outliers"
    )
    fig10.update_layout(height=600, xaxis_tickangle=-45, showlegend=False)
    st.plotly_chart(fig10, use_container_width=True)
    widest_cap_brand = df_viz.groupby('brand')['capacity_gb'].std().idxmax()
    st.write(f"**Key Insight:** **{widest_cap_brand}** offers the widest range of memory capacities, "
              f"spanning both consumer and enterprise/AI configurations.")

    st.markdown("---")

    # ============================================================
    # Conclusion
    # ============================================================
    st.header("🎓   Project Conclusion & Key Insights")
    st.markdown("---")

    st.subheader("Data Analysis Summary")
    st.markdown("""
    This analysis of the Ultimate Memory Shortage Crisis dataset reveals significant insights into
    pricing behavior, capacity trends, and performance dynamics of the global RAM market during a
    period of supply shortage. Through 10 targeted Plotly Express visualizations, we uncovered
    patterns across brands, generations, and market segments.
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### **Pricing Insights**
        - Price varies significantly by brand and generation
        - Larger-capacity and higher-speed kits command a price premium
        - Shortage-inflated pricing is prevalent across the dataset

        ### **Capacity & Performance**
        - Capacity distribution skews toward common consumer tiers (8–64 GB)
        - Enterprise/AI kits push into much higher capacities
        - Speed and price show a clear positive relationship
        """)
    with col2:
        st.markdown("""
        ### **Market Segmentation**
        - Consumer and Enterprise/AI segments show distinct pricing and capacity profiles
        - Recommended usage (Gaming, AI/Data Science, Content Creation, Productivity) drives
          demand concentration by brand and generation
        - DDR5 and the emerging DDR6 (Preview) dominate current market activity

        ### **Business Implications**
        - Buyers should compare price-per-GB across brands to avoid shortage premiums
        - Retailers should monitor inventory weeks and fab utilization for pricing risk
        - Enterprise/AI demand is a key driver of premium pricing during the shortage
        """)

    st.markdown("---")
    st.subheader("Final Summary Metrics")
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        st.metric("Total Kits Analyzed", f"{len(df_viz):,}")
    with f2:
        st.metric("Avg Price/GB", f"${df_viz['price_per_gb'].mean():.2f}")
    with f3:
        st.metric("Avg Latency", f"{df_viz['true_latency_ns'].mean():.2f} ns")
    with f4:
        st.metric("Shortage-Inflated %", f"{(df_viz['price_status'] == 'Shortage-Inflated').mean() * 100:.0f}%")

else:
    st.error("Dataset not available for visualization.")