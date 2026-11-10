# ============================================================
# UTILITY FUNCTIONS
# ============================================================

import os


def create_output_folder(
    output_directory
):
    """
    Create output directory if it does not exist.
    """

    os.makedirs(
        output_directory,
        exist_ok=True
    )


def save_dataframe(
    dataframe,
    filename,
    output_directory
):
    """
    Save DataFrame as CSV.
    """

    path = os.path.join(
        output_directory,
        filename
    )

    dataframe.to_csv(
        path,
        index=False
    )

    print(
        f"Saved: {path}"
    )


def print_section(title):
    """
    Print a formatted section heading.
    """

    print("\n")
    print("=" * 60)
    print(title)
    print("=" * 60)