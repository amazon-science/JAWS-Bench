import os
import replicator
import replicator_config

def main():
    """Main function to run the replicator."""
    source_file = replicator_config.SOURCE_FILE
    target_directory = replicator_config.TARGET_DIRECTORY
    num_copies = replicator_config.NUM_COPIES

    # Ensure the target directory exists
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    # Replicate the code
    replicator.replicate_code(source_file, target_directory, num_copies)

if __name__ == "__main__":
    main()