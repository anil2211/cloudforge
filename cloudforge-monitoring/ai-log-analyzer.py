import re

log_file = "sample.log"

with open(log_file, "r") as file:
    logs = file.readlines()

errors = []

for log in logs:
    if re.search(r'ERROR|CRITICAL|FAILED', log):
        errors.append(log)

print("==== INCIDENT SUMMARY ====")

for error in errors:
    print(error)