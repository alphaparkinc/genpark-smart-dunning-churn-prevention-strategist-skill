import sys, json
from client import SmartDunningChurnStrategist

def main():
    dunning = SmartDunningChurnStrategist()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(dunning.run_benchmark_smart_dunning(), indent=2))
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            params = req.get("params", {})
            rid = req.get("id")

            if method == "tools/list":
                res = {
                    "tools": [
                        {"name": "analyze_payment_failure", "description": "Classify card decline codes and recommended dunning action."},
                        {"name": "generate_optimized_retry_schedule", "description": "Generate intelligent multi-attempt retry cadence."},
                        {"name": "run_benchmark_smart_dunning", "description": "Run smart dunning benchmark suite."}
                    ]
                }
            elif method == "tools/call":
                tname = params.get("name")
                args = params.get("arguments", {})
                if tname == "analyze_payment_failure":
                    out = dunning.analyze_payment_failure(args.get("decline_code", ""), args.get("attempt_number", 1), args.get("invoice_amount", 99.0))
                elif tname == "generate_optimized_retry_schedule":
                    out = dunning.generate_optimized_retry_schedule(args.get("decline_code", ""), args.get("total_attempts", 4))
                elif tname == "run_benchmark_smart_dunning":
                    out = dunning.run_benchmark_smart_dunning()
                else:
                    out = {"error": f"Unknown tool {tname}"}
                res = {"content": [{"type": "text", "text": json.dumps(out)}]}
            else:
                res = {"error": "Unsupported method"}
            print(json.dumps({"jsonrpc": "2.0", "id": rid, "result": res}), flush=True)
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}), flush=True)

if __name__ == "__main__":
    main()
