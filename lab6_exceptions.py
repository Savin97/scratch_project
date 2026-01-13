def parse_int(value):
    return int(value)

def pipeline_step(value):
    return parse_int(value)

def run_pipeline(values):
    results = []
    for value in values:
        try:
            results.append(pipeline_step(value))
        except ValueError as e:
            print(f"Skipped value {value} due to error:", e)
        
    return results

print(run_pipeline(["10", "20", "x", "30"]))
