import sys

def read_file(filename):
    try:
        with open(filename, 'r') as file:
            return file.readlines()
    except IOError:
        print(f"Error opening or reading input file: {filename}")
        sys.exit()

def compare_files(file1_lines, file2_lines):
    max_len = max(len(file1_lines), len(file2_lines))
    differences = []

    for i in range(max_len):
        line1 = file1_lines[i] if i < len(file1_lines) else ""
        line2 = file2_lines[i] if i < len(file2_lines) else ""

        if line1 != line2:
            differences.append((i + 1, line1, line2))
    
    return differences

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 diff.py <file1> <file2>")
        sys.exit()

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    file1_lines = read_file(file1)
    file2_lines = read_file(file2)

    differences = compare_files(file1_lines, file2_lines)

    if differences:
        for line_num, line1, line2 in differences:
            print(f"Line {line_num}:")
            print(f"- {line1.strip()}")
            print(f"+ {line2.strip()}")
            print()
    else:
        print("The files are identical.")

if __name__ == "__main__":
    main()