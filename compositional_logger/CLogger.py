import json
import time


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Log:
    def __init__(self, text):
        self.type = "Log"
        self.timestamp = time.time()
        self.text = text

    def is_ready(self):
        return False


class Step:
    def __init__(self, step_name):
        self.type = "Step"
        self.name = step_name
        self.logs = []
        self.in_process = True
        self.result = None

    def add_log(self, text):
        if self.logs:
            unit = self.logs[-1]
            if unit.is_ready():
                unit.add_log(text)
            else:
                self.logs.append(Log(text))
        else:
            self.logs.append(Log(text))

    def is_ready(self):
        return self.in_process

    def start_step(self, step_name):
        if self.logs:
            unit = self.logs[-1]
            if unit.is_ready():
                unit.start_step(step_name)
            else:
                self.logs.append(Step(step_name))
        else:
            self.logs.append(Step(step_name))

    def end_step(self, result):
        if self.logs:
            unit = self.logs[-1]
            if unit.is_ready():
                unit.end_step(result)
            else:
                self.in_process = False
                self.result = result
        else:
            self.in_process = False
            self.result = result

    def start_test(self, test_name):
        if self.logs:
            unit = self.logs[-1]
            if unit.is_ready():
                unit.start_test(test_name)
            else:
                self.logs.append(Test(test_name))
        else:
            self.logs.append(Test(test_name))

    def end_test(self, test_result):
        if self.logs:
            unit = self.logs[-1]
            if unit.is_ready():
                unit.end_test(test_result)
            else:
                raise f"Last unit is closed (no opened tests)"
        else:
            raise f"Clear session, no tests"


class Test:
    def __init__(self, test_name):
        self.type = "Test"
        self.logs = []
        self.name = test_name
        self.in_process = True
        self.result = None

    def add_log(self, text):
        if self.logs:
            unit = self.logs[-1]
            if unit.is_ready():
                unit.add_log(text)
            else:
                self.logs.append(Log(text))
        else:
            self.logs.append(Log(text))

    def is_ready(self):
        return self.in_process

    def start_step(self, step_name):
        if self.logs:
            unit = self.logs[-1]
            if unit.is_ready():
                unit.start_step(step_name)
            else:
                self.logs.append(Step(step_name))
        else:
            self.logs.append(Step(step_name))

    def end_step(self, result):
        if self.logs:
            unit = self.logs[-1]
            if unit.is_ready():
                unit.end_step(result)
            else:
                raise f"Last unit is closed (no opened steps)"
        else:
            raise f"Clear session, no steps"

    def start_test(self, test_name):
        if self.logs:
            unit = self.logs[-1]
            if unit.is_ready():
                unit.start_test(test_name)
            else:
                self.logs.append(Test(test_name))
        else:
            self.logs.append(Test(test_name))

    def end_test(self, test_result):
        if self.logs:
            unit = self.logs[-1]
            if unit.is_ready():
                unit.end_test(test_result)
            else:
                self.in_process = False
                self.result = test_result
        else:
            self.in_process = False
            self.result = test_result


class Session:
    def __init__(self):
        self.type = "Session"
        self.logs = []
        self.queue = []
        self.iter = 0

    def add_log(self, text):
        self.queue.append(text)
        if self.logs:
            unit = self.logs[-1]
            if unit.is_ready():
                unit.add_log(text)
            else:
                self.logs.append(Log(text))
        else:
            self.logs.append(Log(text))

    def start_test(self, test_name):
        if self.logs:
            unit = self.logs[-1]
            if unit.is_ready():
                unit.start_test(test_name)
            else:
                self.logs.append(Test(test_name))
        else:
            self.logs.append(Test(test_name))

    def end_test(self, test_result):
        if self.logs:
            unit = self.logs[-1]
            if unit.is_ready():
                unit.end_test(test_result)
            else:
                raise f"Last unit is closed (no opened tests)"
        else:
            raise f"Clear session, no tests"

    def start_step(self, step_name):
        if self.logs:
            unit = self.logs[-1]
            if unit.is_ready():
                unit.start_step(step_name)
            else:
                self.logs.append(Step(step_name))
        else:
            self.logs.append(Step(step_name))

    def end_step(self, result):
        if self.logs:
            unit = self.logs[-1]
            if unit.is_ready():
                unit.end_step(result)
            else:
                raise f"Last unit is closed (no opened steps)"
        else:
            raise f"Clear session, no steps"

    def get_queue(self):
        last_index = len(self.queue)
        while last_index > self.iter:
            yield self.queue[self.iter]
            self.iter += 1

    # def get_queue(self):
    #     last_index = len(self.queue)
    #     if last_index > self.iter:
    #         temp = self.queue[self.iter:last_index]
    #         self.iter = last_index
    #         return temp
    #     else:
    #         return []


class CLogger(object):
    def __init__(self):
        self.sessions = {}

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(CLogger, cls).__new__(cls)
        return cls.instance
    def send_session(self, sso):
        session = self.sessions.get(sso)
        if session:
            session.queue.append(self.dump_json(sso))
        return None

    def create_session(self, sso):
        session = Session()
        self.sessions[sso] = session

    def start_test(self, sso, test_name):
        self.add_log(sso, "Test Started", test_name)
        session: Session = self.sessions.get(sso)
        if session:
            session.start_test(test_name)
        else:
            raise f"No session for: {sso}"

    def end_test(self, sso, test_result=None):
        self.add_log(sso, "Test Ended")
        session: Session = self.sessions.get(sso)
        if session:
            session.end_test(test_result)
        else:
            raise f"No session for: {sso}"

    def start_step(self, sso, step_name):
        self.add_log(sso, "Step Started", step_name)
        session: Session = self.sessions.get(sso)
        if session:
            session.start_step(step_name)
        else:
            raise f"No session for: {sso}"

    def end_step(self, sso, result=None):
        self.add_log(sso, "Step Ended")
        session: Session = self.sessions.get(sso)
        if session:
            session.end_step(result)
        else:
            raise f"No session for: {sso}"

    def add_log(self, sso, *messages):
        message = " ".join(messages)
        session: Session = self.sessions.get(sso)
        if session:
            session.add_log(message)
        else:
            raise Exception(f"No session for: {sso}")

    def check_logs(self, sso):
        session: Session = self.sessions.get(sso)
        if session:
            return session.get_queue()
        else:
            raise f"No session for: {sso}"

    def dump_json(self, sso):
        session = self.sessions.get(sso)
        if session:
            temp = vars(session).copy()
            del temp["queue"]
            return json.dumps(temp, default=lambda obj: obj.__dict__, indent=4, ensure_ascii=False)
        return None

    def end_session(self, sso):
        session = self.sessions.get(sso)
        if session:
            temp = self.dump_json(sso)
            del self.sessions[sso]
            return temp