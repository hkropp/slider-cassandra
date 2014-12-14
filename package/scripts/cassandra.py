#!/usr/bin/env python
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import sys
from resource_management import *

class Cassandra(Script):
    def install(self, env):
        self.install_packages(env)

    def configure(self, env):
        import params
        env.set_params(params)

        TemplateConfig(
            format("{conf_dir}/cassandra.yaml"),
            owner = params.cassandra_user
        )

        TemplateConfig(
            format("{conf_dir}/cassandra-env.sh"),
            owner = params.cassandra_user
        )

        TemplateConfig(
            format("{conf_dir}/log4j-server.properties"),
            owner = params.cassandra_user
        )

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env) # for security

        process_cmd = format("{app_root}/bin/cassandra")

        Execute(
            process_cmd,
            user=params.app_user,
            logoutput=False,
            wait_for_finish=False
        )

    def stop(self, env):
        import params
        env.set_params(params)

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(params.pid_file)


if __name__ == "__main__":
    Cassandra().execute()
