import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def univariate_plots(df: pd.DataFrame, target: str) -> None:
    """
    Plots univariate plots for all the columns in the dataframe.

    Expects numeric columns only.
    """
    for col in df.columns:
        # Check if the col is the target column (EC1 or EC2)
        if col == target:
            continue  # Skip target columns in univariate analysis

        plt.figure(figsize=(8, 4))

        # Histogram
        plt.subplot(1, 2, 1)
        sns.histplot(data=df, x=col, kde=True)
        plt.xlabel(col)
        plt.ylabel("Frequency")
        plt.title("Histogram")

        # Box plot
        plt.subplot(1, 2, 2)
        sns.boxplot(data=df, y=col)
        plt.ylabel(col)
        plt.title("Box Plot")

        # Adjust spacing between subplots
        plt.tight_layout()

        # Show the plots
        plt.show()


def bi_variate_plots(df: pd.DataFrame, target: str) -> None:
    """
    Plots bivariate plots for all column combinations in the dataframe.

    Expects numeric columns only.
    """
    # Get the list of column names except for the target column
    variables = [col for col in df.columns if col != target]

    # Define the grid layout based on the number of variables
    num_variables = len(variables)
    num_cols = 4  # Number of columns in the grid
    num_rows = (
        num_variables + num_cols - 1
    ) // num_cols  # Calculate the number of rows needed

    # Set the size of the figure
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 4 * num_rows))

    # Generate violin plots for each variable with respect to EC1
    for i, variable in enumerate(variables):
        row = i // num_cols
        col = i % num_cols
        ax = axes[row][col]

        sns.violinplot(data=df, x=target, y=variable, ax=ax)
        ax.set_xlabel(target)
        ax.set_ylabel(variable)
        ax.set_title(f"Violin Plot: {variable} vs {target}")

    # Remove any empty subplots
    if num_variables < num_rows * num_cols:
        for i in range(num_variables, num_rows * num_cols):
            fig.delaxes(axes.flatten()[i])

    # Adjust the spacing between subplots
    plt.tight_layout()

    # Show the plot
    plt.show()


def correlation_heatmap(df: pd.DataFrame) -> None:
    """
    Plots half of the heatmap showing correlations of all features.

    Expects numeric columns only.
    """
    # Calculate the correlation matrix
    corr = df.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(230, 20, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(
        corr,
        mask=mask,
        cmap=cmap,
        vmax=0.3,
        center=0,
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.5},
    )

    plt.show()


def correlation_to_target(df: pd.DataFrame, target: str) -> None:
    """
    Plots correlations for all the columns in the dataframe in relation to the target column.

    Expects numeric columns only.
    """
    # Calculate the correlation matrix
    corr = df.corr()

    # Get correlations without 'EC1' and 'EC2'
    corrs = corr[target].drop([target])

    # Sort correlation values in descending order
    corrs_sorted = corrs.sort_values(ascending=False)

    # Create a heatmap of the correlations with EC1
    sns.set(font_scale=0.8)
    sns.set_style("white")
    sns.set_palette("PuBuGn_d")
    sns.heatmap(corrs_sorted.to_frame(), cmap="coolwarm", annot=True, fmt=".2f")
    plt.title("Correlation with EC1")
    plt.show()
