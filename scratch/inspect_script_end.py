with open('build_store_verification_milestone.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("First 30 lines:")
print("".join(lines[:30]))

print("\nLast 60 lines:")
print("".join(lines[-60:]))
