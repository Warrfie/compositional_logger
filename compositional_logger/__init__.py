from compositional_logger.CLogger import CLogger

logger = CLogger()

check_logs = logger.check_logs
add_log = logger.add_log

create_session = logger.create_session
dump_json = logger.dump_json
send_session = logger.send_session
start_test = logger.start_test
end_test = logger.end_test
end_session = logger.end_session
start_step = logger.start_step
end_step = logger.end_step
