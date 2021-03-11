import psutil as ps


FORMS = {
    "sensors":{
        "keys": "{keys: >11}   |",
        "temperatures": "{current: >7}   | {high: >6} | {critical: >8}",
        "fans": "\nFans_Current: {current: >1}phase/sec\n",
        "battery": "Battery: {percent: >5} | Time left: {secsleft: >1}secs | Power plugged: {power_plugged: >1}\n\n"
    }
}


def get_info():
   res = {"keys": [],"temperatures": [], "fans": [], "battery": []}
   
   root_temperatures = ps.sensors_temperatures()
   keys_temperatures = list(root_temperatures.keys())
   for i in keys_temperatures:
       res["keys"].append({"keys": i})
   vl_temperatures = list(root_temperatures.values())
   data_temperatures = list()
   for i in vl_temperatures:
       data_temperatures.append(i[0])
   for sens in data_temperatures:
       res["temperatures"].append(
            {
               "current": sens.current,
               "high": sens.high or 0.0,
               "critical": sens.critical or 0.0
            }
       )

   root_fans = ps.sensors_fans()
   rt_fans = list(root_fans.values())
   data_fans = rt_fans[0][0]
   res["fans"].append(
        {
           "current": data_fans.current
        }
   )

   data_battery = ps.sensors_battery()
   res["battery"].append(
        {
            "percent": data_battery.percent,
            "secsleft": data_battery.secsleft,
            "power_plugged": data_battery.power_plugged
        }
   )
   
   return res


def show(**kwargs):
    keys = kwargs["sens"]["keys"]
    temperatures = kwargs["sens"]["temperatures"]
    print("\n\n'Name_Sensors'| 'Current' | 'High' | 'Critical'")
    for k,t in zip(keys,temperatures):
        print(FORMS["sensors"]["keys"].format(**k), end="\t")
        print(FORMS["sensors"]["temperatures"].format(**t))
    
    fans = kwargs["sens"]["fans"]
    for f in fans:
        print(FORMS["sensors"]["fans"].format(**f))
    
    battery = kwargs["sens"]["battery"]
    for b in battery:
        print(FORMS["sensors"]["battery"].format(**b))


def main():
    sens_info = get_info()

    show(sens=sens_info)


if __name__ == '__main__':
    main()