import subprocess
import sys

def run_compiler():
    filename = sys.argv[1] if len(sys.argv) > 1 else 'test.java'
    print(f"[*] Running compiler.exe on {filename}...")
    try:
        result = subprocess.run(['./compiler.exe', filename], capture_output=True, text=True, timeout=5)
        print("\n=== COMPILER STDOUT ===")
        print(result.stdout)
        if result.stderr:
            print("\n=== COMPILER STDERR ===")
            print(result.stderr)
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == '__main__':
    run_compiler()