<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>My Devices</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/water.css">
</head>
<body>
<h1>Glisan Devices</h1>
<table style="table-layout: auto;">
    <thead>
        <tr>
            <th>Name</th>
            <th>Address</th>
            <th>MAC</th>
            <th>Static</th>
            <th>Connected</th>
            <th>Last Seen</th>
            <th>Go</th>
        </tr>
    </thead>
    <tbody>
        % for device in devices:
        <tr>
            % if "comment" in device:
            <th>{{device["comment"]}}</th>
            % else:
            <th>{{device.get("host-name",  "❌")}}</th>
            % end
            <th>{{device.get("address", "❌")}}</th>
            <th>{{device.get("mac-address", "❌")}}</th>
            % if device["dynamic"] == "true":
            <th>❌</th>
            % else:
            <th>✔️</th>
            % end
            % if device["status"] == "bound":
            <th>✔️</th>
            % else:
            <th>❌</th>
            % end
            <th>{{device.get("last-seen", "❌")}}</th>
            <th><a href="http://{{device['address']}}">Go</a></th>
        </tr>
        % end
    </tbody>
</table>

<p>Server Closet Temp: {{ iot['server_room_temp'] }}°F</p>
<p>Server Closet Humidity: {{ iot['server_room_hum'] }}%</p>
<p>Studio Temp: {{ iot['studio_temp'] }}°F</p>
<p>Studio Humidity: {{ iot['studio_hum'] }}%</p>

</body>
</html>
