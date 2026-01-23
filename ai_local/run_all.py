import subprocess
import sys

steps = [
    "generate_script.py",
    "generate_images.py",
    "generate_voice.py"
]

for step in steps:
    print(f"\n▶ Running {step}")
    result = subprocess.run(
        ["python", step],
        cwd=".",
        capture_output=True,
        text=True
    )

    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        print(f"❌ FAILED at {step}")
        sys.exit(1)

print("\n✅ ALL AI STEPS COMPLETED")
