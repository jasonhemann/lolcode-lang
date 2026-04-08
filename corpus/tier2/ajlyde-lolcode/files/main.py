import sys
from interpreter import Interpreter

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <filename.lol>")
        return

    filename = sys.argv[1]
    try:
        with open(filename, "r", encoding="utf-8") as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return

    print("SOURCE CODE:")
    print(source_code)  # Print file content so you confirm it's read

    interpreter = Interpreter(source_code)
    interpreter.run()

if __name__ == "__main__":
    main()
