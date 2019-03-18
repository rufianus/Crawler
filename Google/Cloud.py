
import os
import threading
import subprocess
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


class MySQL:

    def __init__(self, operating_system="windows", project_name="toraja", database_region="asia-southeast1", database_instance_name="sql-toraja", database_name=None, user_name="root", user_password="RagnarTargaryen"):

        operating_system = operating_system.lower()
        instance_name = ''.join([project_name, ":", database_region, ":", database_instance_name])
        print(instance_name)


        if operating_system == "windows":
            script_directory = os.path.dirname(os.path.realpath(__file__))
            proxy_path = os.path.join(script_directory, "cloud_sql_proxy_x64.exe")
            credential_path = os.path.join(script_directory, "cloud-sql-client.json")
            process = ''.join([proxy_path, " -instances=", instance_name, '=tcp:3306 -credential_file="', credential_path, '" &'])
            def run_proxy():
                subprocess.run(process)
                while True:
                    time.sleep(10)
            run_proxy = threading.Thread(target=run_proxy, args=[])
            run_proxy.daemon = True
            run_proxy.start()
            self.AlchemyEngine = create_engine(''.join(['mysql+pymysql://', user_name, ':', user_password, '@127.0.0.1/', database_name]))

        elif operating_system == "linux":
            script_directory = os.path.dirname(os.path.realpath(__file__))
            credential_path = os.path.join(script_directory, "cloud-sql-client.json")
            print(instance_name)
            process = ''.join(["/cloud_sql_proxy -dir=/cloudsql -instances=", instance_name, ' -credential_file="', credential_path, '" &'])
            os.system(process)
            time.sleep(5)
            self.AlchemyEngine = create_engine(''.join(['mysql+pymysql://', user_name, ':', user_password, '@/', database_name, '?unix_socket=/cloudsql/', instance_name]))

            # os.system("./cloud_sql_proxy -dir=/cloudsql &")
            # time.sleep(5)
            # self.AlchemyEngine = create_engine(''.join(['mysql+pymysql://', user_name, ':', user_password, '@/', database_name, '?unix_socket=/cloudsql/', instance_name]))

        self.Base = declarative_base()
        self.Session = sessionmaker(bind=self.AlchemyEngine)()

    def Insert(self, objects):

        try:
            objects.record_lastupdate_datetime = datetime.now()
        except:
            pass
        if isinstance(objects, list):
            self.Session.add_all(objects)
            for objecta in objects:
                print("Inserting:", objecta.__table__.name)
        else:
            self.Session.add(objects)
            print("Inserting:", objects.__table__.name)
        self.Session.commit()
