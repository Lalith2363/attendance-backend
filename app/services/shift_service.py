from datetime import datetime

def evaluate_attendance(check_in, check_out, shift):

    status = "on_time"

    if check_in.time() > shift.start_time:
        status = "late"

    work_hours = 0

    if check_out:
        duration = check_out - check_in
        work_hours = duration.total_seconds() / 3600

    overtime = 0

    if check_out and check_out.time() > shift.end_time:
        overtime = (
            datetime.combine(datetime.today(), check_out.time()) -
            datetime.combine(datetime.today(), shift.end_time)
        ).total_seconds() / 3600

    return {
        "status": status,
        "work_hours": work_hours,
        "overtime": overtime
    }