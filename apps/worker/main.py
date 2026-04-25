from packages.common.request_context import RequestIDs, set_request_ids, reset_request_ids, current_ids


def main() -> None:
    tokens = set_request_ids(RequestIDs(trace_id="trc_worker", run_id="run_worker", device_id="dev_worker"))
    try:
        ids = current_ids()
        print(f"worker scaffold trace_id={ids.trace_id} run_id={ids.run_id} device_id={ids.device_id}")
    finally:
        reset_request_ids(tokens)


if __name__ == "__main__":
    main()
