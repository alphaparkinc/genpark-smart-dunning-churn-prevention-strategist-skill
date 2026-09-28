import sys, json
from client import SmartDunningChurnStrategist

def main():
    print("Testing SmartDunningChurnStrategist...")
    dunning = SmartDunningChurnStrategist()
    res = dunning.run_benchmark_smart_dunning()
    print(json.dumps(res, indent=2))
    assert res["benchmark_status"] == "PASSED"
    assert res["soft_decline_retried"] is True
    assert res["hard_decline_blocked"] is True
    assert res["schedule_steps_count"] == 3
    print("All Smart Dunning Churn Strategist tests passed successfully!")

if __name__ == "__main__":
    main()
