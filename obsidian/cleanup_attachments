#!/bin/bash

# ------------------------------------------------------------------------------
# Filename: cleanup_attachments.sh
# Author: Justin Kindrix
# Description: Script to clean up unused files in the attachments directory of 
#              a markdown-based project. It deletes files not referenced in any
#              markdown files, with a dry run mode and help option.
# Version: 1.2
# Date: 2024-07-12
#
# Features:
#   1. URL encode file names to check their references in markdown files.
#   2. Verify if a file is referenced in any markdown file, excluding the attachments directory.
#   3. Delete unreferenced files and count the deletions.
#   4. Provide a dry run mode to list files that would be deleted without deleting them.
#   5. Display a help message explaining the script's options.
#
# Usage: ./cleanup_attachments.sh [OPTIONS]
#
# Options:
#   -n, --dry-run    Dry run mode. Show which files would be deleted without actually deleting them.
#   -h, --help       Show this help message and exit.
#   -v level         Set verbosity level. Options are:
#                       INFO    (default) Show informational messages.
#                       WARN    Show warning messages.
#                       ERROR   Show error messages.
#                       DEBUG   Show debug messages.
#
# Note: Ensure the script has the necessary permissions to run and access required directories.
# ------------------------------------------------------------------------------

set -euo pipefail

# Constants for color codes
readonly COLOR_RESET="\033[0m"
readonly COLOR_INFO="\033[1;32m"
readonly COLOR_WARN="\033[1;33m"
readonly COLOR_ERROR="\033[1;31m"
readonly COLOR_DEBUG="\033[1;34m"

# Default verbosity level
verbosity="INFO"

# Function to display the help message
show_help() {
    echo "Usage: $(basename "$0") [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -n, --dry-run     Dry run mode. Show which files would be deleted without actually deleting them."
    echo "  -h, --help        Show this help message and exit."
    echo "  -v level          Set verbosity level. Options are:"
    echo "                      INFO    (default) Show informational messages."
    echo "                      WARN    Show warning messages."
    echo "                      ERROR   Show error messages."
    echo "                      DEBUG   Show debug messages."
    echo ""
    echo "Description:"
    echo "  This script processes files in the specified directory and deletes those that are not referenced in any markdown files."
    echo ""
    echo "Examples:"
    echo "  $(basename "$0") -n"
    echo "      Run the script in dry run mode, showing which files would be deleted."
    echo ""
    echo "  $(basename "$0") -v DEBUG"
    echo "      Run the script with debug verbosity, showing detailed information about the script's operation."
}

# Function to URL encode a string
urlencode() {
    local input="$1"
    local length="${#input}"
    local encoded=""

    for (( i = 0; i < length; i++ )); do
        local c="${input:i:1}"
        case "$c" in
            [a-zA-Z0-9.~_-])
                encoded+="$c"
                ;;
            *)
                encoded+="$(printf '%%%02X' "'$c")"
                ;;
        esac
    done

    echo "$encoded"
}

# Logging function with colorized output and verbosity control
log() {
    local level="$1"
    local message="$2"
    local color=""
    local default_verbosity="INFO"
    local verbosity="${VERBOSITY:-$default_verbosity}"

    declare -A levels=( ["ERROR"]=1 ["WARN"]=2 ["INFO"]=3 ["DEBUG"]=4 )
    
    # Check if the provided level is valid
    if [[ ! ${levels[$level]} ]]; then
        echo "Invalid log level: $level"
        return 1
    fi

    # Check if the verbosity level is valid, default to INFO if not
    if [[ ! ${levels[$verbosity]} ]]; then
        verbosity=$default_verbosity
    fi

    # Proceed if the log level is within the verbosity threshold
    if [[ ${levels[$level]} -le ${levels[$verbosity]} ]]; then
        case "$level" in
            INFO) color="$COLOR_INFO" ;;
            WARN) color="$COLOR_WARN" ;;
            ERROR) color="$COLOR_ERROR" ;;
            DEBUG) color="$COLOR_DEBUG" ;;
            *) color="$COLOR_RESET" ;;
        esac
        echo -e "${color}[$level] $message${COLOR_RESET}"
    fi
}

# Function to check if a file is referenced in any markdown file
is_file_referenced() {
    local filename="$1"
    local encoded_filename

    if [[ -z "$filename" ]]; then
        log "ERROR" "No filename provided to is_file_referenced function."
        return 2
    fi

    encoded_filename=$(urlencode "$filename")

    if grep -qr "(${encoded_filename})" --exclude-dir="./attachments" --include="*.md" .; then
        log "DEBUG" "File '$filename' is referenced in markdown files."
        return 0
    else
        log "DEBUG" "File '$filename' is NOT referenced in markdown files."
        return 1
    fi
}

# Function to delete a file and count the deletion
delete_file() {
    local file="$1"
    local -n count_ref="$2"
    local dry_run="$3"

    if [[ -z "$file" ]]; then
        log "ERROR" "No file specified for deletion."
        return 1
    fi

    if [[ "$dry_run" == "true" ]]; then
        log "INFO" "Would delete $file"
    else
        if rm -f "$file"; then
            log "INFO" "Deleted $file"
            ((count_ref++))
        else
            log "ERROR" "Failed to delete $file"
            return 1
        fi
    fi

    return 0
}

# Function to process files in a directory
process_files_in_directory() {
    local directory="$1"
    local -n deleted_count_ref="$2"
    local dry_run="$3"

    if [[ ! -d "$directory" ]]; then
        log "ERROR" "Directory '$directory' does not exist."
        return 1
    fi

    log "INFO" "Processing files in directory: $directory"
    while IFS= read -r -d '' file; do
        local filename
        filename=$(basename "$file")

        if ! is_file_referenced "$filename"; then
            delete_file "$file" deleted_count_ref "$dry_run" || true
        fi
    done < <(find "$directory" -type f -print0)

    log "INFO" "Finished processing files in directory: $directory"
    return 0
}

# Main function to orchestrate the file cleanup process
main() {
    local deleted_count=0
    local attachments_dir="./attachments"
    local dry_run=false
    local verbosity="INFO"

    # Check for the dry-run, help, and verbosity flags
    while [[ "$#" -gt 0 ]]; do
        case "$1" in
            -n|--dry-run) dry_run=true ;;
            -h|--help) show_help; exit 0 ;;
            -v) shift; verbosity="$1" ;;
            *) show_help; exit 1 ;;
        esac
        shift
    done

    # Export verbosity for use in log function
    export VERBOSITY="$verbosity"

    # Log the script start
    log "INFO" "Starting the cleanup script with verbosity level: $verbosity."

    # Process files in the attachments directory
    process_files_in_directory "$attachments_dir" deleted_count "$dry_run"

    # Print the number of unused files removed
    if [[ "$dry_run" == "false" ]]; then
        log "INFO" "Number of unused files removed: $deleted_count"
    else
        log "INFO" "Dry run mode: no files were actually deleted."
    fi

    # Log the script end
    log "INFO" "Cleanup script completed."
}

# Execute the main function
main "$@"
