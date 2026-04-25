import argparse

from packages.common.request_context import RequestIDs, current_ids, reset_request_ids, set_request_ids


def main() -> None:
    parser = argparse.ArgumentParser(description="automated-automation CLI scaffold")
    parser.add_argument("--run-id", default="run_cli")
    parser.add_argument("--device-id", default="dev_cli")
    args = parser.parse_args()

    tokens = set_request_ids(RequestIDs(trace_id="trc_cli", run_id=args.run_id, device_id=args.device_id))
    try:
        ids = current_ids()
        print(f"cli trace_id={ids.trace_id} run_id={ids.run_id} device_id={ids.device_id}")
    finally:
        reset_request_ids(tokens)


if __name__ == "__main__":
    main()
