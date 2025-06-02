from Bio import SeqIO
from Bio.Align.Applications import MuscleCommandline
import os
import subprocess

def perform_muscle_alignment(input_fasta_path, output_fasta_path, muscle_exe_path="muscle"):
    """
    Performs a multiple sequence alignment using the MUSCLE program.

    Args:
        input_fasta_path (str): Path to the input FASTA file containing unaligned sequences.
        output_fasta_path (str): Path where the aligned sequences will be saved (in FASTA format).
        muscle_exe_path (str, optional): Path to the MUSCLE executable.
                                         Defaults to "muscle", assuming it's in your system's PATH.
                                         If not, provide the full path (e.g., "/usr/local/bin/muscle").

    Returns:
        bool: True if alignment was successful, False otherwise.
    """
    if not os.path.exists(input_fasta_path):
        print(f"Error: Input file '{input_fasta_path}' not found.")
        return False

    try:
        # Construct the MUSCLE command line.
        # -in: specifies the input file
        # -out: specifies the output file
        # -fasta: ensures output is in FASTA format
        muscle_cmd = MuscleCommandline(
            cmd=muscle_exe_path,
            input=input_fasta_path,
            out=output_fasta_path,
            fasta=True
        )

        print(f"Running MUSCLE on '{input_fasta_path}'...")
        
        # Execute the MUSCLE command.
        # stdout and stderr capture the output and errors from MUSCLE.
        stdout, stderr = muscle_cmd()

        if stderr:
            print(f"MUSCLE reported errors/warnings for '{input_fasta_path}':\n{stderr}")
        # You can uncomment the following lines if you want to see MUSCLE's standard output
        # if stdout:
        #     print(f"MUSCLE output for '{input_fasta_path}':\n{stdout}")

        if os.path.exists(output_fasta_path) and os.path.getsize(output_fasta_path) > 0:
            print(f"Alignment successful for '{input_fasta_path}'. Output saved to '{output_fasta_path}'.")
            return True
        else:
            print(f"MUSCLE alignment failed or produced an empty output file for '{input_fasta_path}'.")
            return False

    except FileNotFoundError:
        print(f"Error: MUSCLE executable not found at '{muscle_exe_path}'.")
        print("Please ensure MUSCLE is installed and its path is correct or in your system's PATH.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Error running MUSCLE for '{input_fasta_path}': {e}")
        print(f"MUSCLE stderr:\n{e.stderr.decode()}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred during MUSCLE alignment for '{input_fasta_path}': {e}")
        return False

def align_multiple_fasta_files_in_folder(input_folder_path, output_folder_path, muscle_exe_path="muscle"):
    """
    Iterates through FASTA files in a specified input folder, performs MUSCLE alignment
    on each, and saves the aligned sequences to an output folder.

    Args:
        input_folder_path (str): Path to the folder containing unaligned FASTA files.
        output_folder_path (str): Path to the folder where aligned sequences will be saved.
        muscle_exe_path (str, optional): Path to the MUSCLE executable.
                                         Defaults to "muscle", assuming it's in your system's PATH.
    """
    if not os.path.isdir(input_folder_path):
        print(f"Error: Input folder '{input_folder_path}' not found or is not a directory.")
        return

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
        print(f"Created output folder: '{output_folder_path}'")

    fasta_files_found = False
    for filename in os.listdir(input_folder_path):
        # Check if the file has a common FASTA extension
        if filename.lower().endswith((".fasta", ".fa", ".fna")):
            fasta_files_found = True
            input_file_path = os.path.join(input_folder_path, filename)
            
            # Construct output filename: add '_aligned' before the file extension
            name, ext = os.path.splitext(filename)
            output_file_name = f"{name}_aligned{ext}"
            output_file_path = os.path.join(output_folder_path, output_file_name)

            print(f"\n--- Processing '{filename}' ---")
            perform_muscle_alignment(input_file_path, output_file_path, muscle_exe_path)
            print(f"--- Finished processing '{filename}' ---")

    if not fasta_files_found:
        print(f"No FASTA files found in '{input_folder_path}'. (Looking for .fasta, .fa, .fna extensions)")
    else:
        print("\nAll specified FASTA files processed.")


# --- Main execution block ---
if __name__ == "__main__":
    # IMPORTANT:
    # 1. Ensure MUSCLE is installed and its executable is in your system's PATH,
    #    or provide the full path to `muscle_exe_path`.
    #    You can download MUSCLE from: http://www.drive5.com/muscle/downloads.htm

    # 2. Replace these with your actual input and output folder paths.
    #    Example:
    #    input_folder = "/path/to/your/unaligned_fasta_files"
    #    output_folder = "/path/to/your/aligned_output"
    
    # --- Demonstration Setup (Creates dummy files and cleans up) ---
    # This section is for demonstration purposes only.
    # In a real scenario, you would have your input folder ready.
    demo_input_folder = "unaligned_fasta_files_demo"
    demo_output_folder = "aligned_output_demo"
    
    # Create dummy input folder and files for demonstration
    if not os.path.exists(demo_input_folder):
        os.makedirs(demo_input_folder)
        
    with open(os.path.join(demo_input_folder, "geneA.fasta"), "w") as f:
        f.write(""">seqA_species1
ATGCGTACGTACGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCT
>seqA_species2
ATGCGTACGTACGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCT
>seqA_species3
ATGCGTACGTACGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCT
""")
    with open(os.path.join(demo_input_folder, "geneB.fasta"), "w") as f:
        f.write(""">seqB_organismX
GCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC
>seqB_organismY
GCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC
>seqB_organismZ
GCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC
""")
    print(f"Created dummy input folder '{demo_input_folder}' with sample FASTA files for demonstration.")

    # Call the function to align multiple files
    align_multiple_fasta_files_in_folder(demo_input_folder, demo_output_folder, muscle_exe_path="muscle")

    # --- Clean up demonstration files and folders ---
    print("\n--- Cleaning up demonstration files ---")
    if os.path.exists(demo_input_folder):
        for f in os.listdir(demo_input_folder):
            os.remove(os.path.join(demo_input_folder, f))
        os.rmdir(demo_input_folder)
        print(f"Removed dummy input folder '{demo_input_folder}'.")
    
    if os.path.exists(demo_output_folder):
        for f in os.listdir(demo_output_folder):
            os.remove(os.path.join(demo_output_folder, f))
        os.rmdir(demo_output_folder)
        print(f"Removed dummy output folder '{demo_output_folder}'.")
    print("Cleanup complete.")
