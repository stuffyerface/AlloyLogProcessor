import os
import re
import time

alloysDropped = []
uuids = []

def read_log_line(line):
  uuidpattern = re.compile(r"uuid:\s*([0-9a-f]{32})")
  alloypattern = re.compile(r"\[(\d+:\d+:\d+)\]\s+Player\s+([^\s]+)\s+dropped a new alloy at timestamp\s+(\d+)")
  match = uuidpattern.search(line)
  if match:
    uuid = match.group(1)
    if uuid in uuids:
      return 0
    uuids.append(uuid)
    return 0
  match = alloypattern.search(line)
  if match:
    alloysDropped.append((match.group(2),match.group(3)))
  return 0

def read_log_file(filepath):
  with open(filepath, 'r', errors="ignore") as file:
    for line in file:
      read_log_line(line)

def write_to_file(filename, data):
  with open(filename, "w") as file:
    for x in data:
      file.write(f"{x}\n")

def main():
  directory = input("Select directory: ")
  if not os.path.exists(directory):
    print("Invalid directory: " + directory)
    return

  for filename in os.listdir(directory):
    filepath = os.path.join(directory, filename)
    if filepath.endswith('.txt'):
      # print(f"Processing {filename}")
      read_log_file(filepath)
      # print(f"Total uuids: {len(uuids)}")
      # print(f"Total alloys: {len(alloysDropped)}")
  
  uuids.sort()

  script_dir = os.path.dirname(os.path.abspath(__file__))
  uuid_file = os.path.join(script_dir, "uuids.txt")
  alloy_file = os.path.join(script_dir, "alloysDropped.txt")

  write_to_file(uuid_file, uuids)
  write_to_file(alloy_file, alloysDropped)

  print(f"Wrote to file {len(uuids)} uuids and {len(alloysDropped)} alloys.")
  

if __name__ == "__main__":
  start = time.time()
  main()
  end = time.time()
  print(f"Process finished in {(end - start)}")
  
