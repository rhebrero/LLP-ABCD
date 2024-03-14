import ROOT
import argparse

# Create the parser
parser = argparse.ArgumentParser(description="A script that writes a sentence to a file.")

# Add optional arguments
parser.add_argument('-s', '--sentence', type=str, default="This is a default sentence.", help="The sentence to write.")
parser.add_argument('-f', '--file', type=str, default="output.txt", help="The file to write to.")

# Parse the arguments
args = parser.parse_args()

# Write the sentence to the file
with open(args.file, 'w') as f:
    f.write(args.sentence)