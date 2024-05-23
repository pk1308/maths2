#!/bin/bash

# Bash script to convert modified and untracked Jupyter notebook files to markdown.

# Function to check if a directory exists
check_directory() {
    local folder_path="$1"
    if [ ! -d "$folder_path" ]; then
        echo "Error: Directory '$folder_path' does not exist."
        exit 1
    fi
}

# Function to convert modified and untracked notebook files to markdown
convert_to_markdown() {
    local folder_path="$1"
    local notebook_files=()

    # Find modified .ipynb files using git status
    while IFS= read -r -d '' file; do
        # Get the relative path excluding the base directory
        relative_path=$(realpath --relative-to="$folder_path" "$file" 2>/dev/null)
        if [ -n "$relative_path" ]; then
            notebook_files+=("$relative_path")
        else
            echo "Error: realpath failed for '$file'."
        fi
    done < <(git status --porcelain | grep -E "^\s*M.*\.ipynb$" | sed -E 's/^\s*M\s*//' | \
             find "$folder_path" -type f -name "*.ipynb" -print0)

    # Find untracked .ipynb files using git ls-files
    while IFS= read -r -d '' file; do
        # Get the relative path excluding the base directory
        relative_path=$(realpath --relative-to="$folder_path" "$file" 2>/dev/null)
        if [ -n "$relative_path" ]; then
            notebook_files+=("$relative_path")
        else
            echo "Error: realpath failed for '$file'."
        fi
    done < <(git ls-files --others --exclude-standard -- "*.ipynb")

    # Remove duplicates
    readarray -t notebook_files < <(printf "%s\n" "${notebook_files[@]}" | sort -u)

    # Check if any notebook files were found
    if [ ${#notebook_files[@]} -gt 0 ]; then
        echo "Found modified and untracked notebook files:"
        for file in "${notebook_files[@]}"; do
            echo "Converting '$file' to markdown..."
            if jupyter nbconvert --to markdown "$folder_path/$file"; then
                echo "Converted '$file' to markdown successfully."
            else
                echo "Failed to convert '$file' to markdown."
            fi
        done
    else
        echo "No modified or untracked notebook files found in '$folder_path'."
    fi
}

# Main function
main() {
    local folder_path="${1:-./docs}"
    check_directory "$folder_path"
    convert_to_markdown "$folder_path"
}

# Entry point
main "$@"
