with open('index.php', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if '$documents = array(' in line or '$documents =' in line:
        print(f"Start on line {idx+1}")
        for j in range(idx, min(idx + 70, len(lines))):
            print(f"{j+1}: {lines[j]}", end='')
        break
