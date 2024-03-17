class Settings:
    def __init__(self):
        self._status_sleep_interval = 15
        self._status_timeout = 300
        self._autopop_sleep_interval = 180
        self._autopop_main_map = "2154"
        self._admin_role_id = 493097119897616414
        self._autopop_channel_id = 1208112690657239110
        self._autopop_to_preserve_msg_id = 1210244715715371049
        self._role_id_to_tag = 492494724528340992
        self._role_to_tag = f"<@&{self._role_id_to_tag}>"
        self._breeder_role_id: int  = 1209578090666393630

        self._data = {
            "status_sleep_interval": {
                "id": 0,
                "name": "Status command refresh interval",
                "value": self.status_sleep_interval,
                "type": int,
            },
            "status_timeout": {
                "id": 1,
                "name": "Status command timeout",
                "value": self.status_timeout,
                "type": int,
            },
            "autopop_sleep_interval": {
                "id": 2,
                "name": "Autopop refresh interval",
                "value": self.autopop_sleep_interval,
                "type": int,
            },
            "autopop_main_map": {
                "id": 3,
                "name": "Autopop main map",
                "value": self.autopop_main_map,
                "type": str,
            },
            "role_id_to_tag": {
                "id": 4,
                "name": "Role id to tag",
                "value": self.role_id_to_tag,
                "type": int,
            },
            "admin_role_id": {
                "id": 5,
                "name": "Admin role id",
                "value": self.admin_role_id,
                "type": int,
            },
            "autopop_channel_id": {
                "id": 6,
                "name": "Autopop channel id",
                "value": self.autopop_channel_id,
                "type": int,
            },
            "autopop_to_preserve_msg_id": {
                "id": 7,
                "name": "Message id to preserve",
                "value": self.autopop_to_preserve_msg_id,
                "type": int,
            },
            "breeder_role_id" : {
              "id": 8,
              "name": "Breeder role ID",
              "value": self.breeder_role_id,
              "type": int,
            },
        }

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
    def role_id_to_tag(self):
        return self._role_id_to_tag

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

    @property
    def breeder_role_id(self):
        return self._breeder_role_id

    @property
    def data(self):
        return self._data

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

    @role_id_to_tag.setter
    def role_id_to_tag(self, value):
        if not isinstance(value, int):
            raise ValueError("role_id_to_tag must be an integer")
        self._role_id_to_tag = value

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