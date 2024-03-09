class Settings:
    def __init__(self):
        self._status_sleep_interval = 15
        self._status_timeout = 300
        self._autopop_sleep_interval = 180
        self._autopop_main_map = "2154"
        self._role_to_tag = "<@&492494724528340992>"
        self._admin_role_id = 493097119897616414
        self._autopop_channel_id = 1208112690657239110
        self._autopop_to_preserve_msg_id = 1210244715715371049

    # --- Getters ---
    @property
    def status_sleep_interval(self):
        return self._status_sleep_interval

    @property
    def status_timeout(self):
        return self._status_timeout

    @property
    def autopop_sleep_interval(self):
        return self._autopop_sleep_interval

    @property
    def autopop_main_map(self):
        return self._autopop_main_map

    @property
    def role_to_tag(self):
        return self._role_to_tag

    @property
    def admin_role_id(self):
        return self._admin_role_id

    @property
    def autopop_channel_id(self):
        return self._autopop_channel_id

    @property
    def autopop_to_preserve_msg_id(self):
        return self._autopop_to_preserve_msg_id

    # --- Setters ---
    @status_sleep_interval.setter
    def status_sleep_interval(self, value):
        if not isinstance(value, int):
            raise ValueError("status_sleep_interval must be an integer")
        self._status_sleep_interval = value

    @status_timeout.setter
    def status_timeout(self, value):
        if not isinstance(value, int):
            raise ValueError("status_timeout must be an integer")
        self._status_timeout = value

    @autopop_sleep_interval.setter
    def autopop_sleep_interval(self, value):
        if not isinstance(value, int):
            raise ValueError("autopop_sleep_interval must be an integer")
        self._autopop_sleep_interval = value

    @autopop_main_map.setter
    def autopop_main_map(self, value):
        if not isinstance(value, str):
            raise ValueError("autopop_main_map must be a string")
        self._autopop_main_map = value

    @role_to_tag.setter
    def role_to_tag(self, value):
        if not isinstance(value, str):
            raise ValueError("role_to_tag must be a string")
        self._role_to_tag = value

    @admin_role_id.setter
    def admin_role_id(self, value):
        if not isinstance(value, int):
            raise ValueError("admin_role_id must be an integer")
        self._admin_role_id = value

    @autopop_channel_id.setter
    def autopop_channel_id(self, value):
        if not isinstance(value, int):
            raise ValueError("autopop_channel_id must be an integer")
        self._autopop_channel_id = value

    @autopop_to_preserve_msg_id.setter
    def autopop_to_preserve_msg_id(self, value):
        if not isinstance(value, int):
            raise ValueError("autopop_to_preserve_msg_id must be an integer")
        self._autopop_to_preserve_msg_id = value
