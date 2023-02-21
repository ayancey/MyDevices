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
<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Comment</th>
            <th>Address</th>
            <th>MAC</th>
            <th>Dynamic</th>
            <th>Last Seen</th>
            <th>Go</th>
        </tr>
    </thead>
    <tbody>
        % for device in devices:
        <tr>
            <th>{{device.get("host-name", "❌")}}</th>
            <th>{{device.get("comment", "❌")}}</th>
            <th>{{device.get("address", "❌")}}</th>
            <th>{{device.get("active-mac-address", "❌")}}</th>
            % if device["dynamic"] == "true":
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
</body>
</html>
