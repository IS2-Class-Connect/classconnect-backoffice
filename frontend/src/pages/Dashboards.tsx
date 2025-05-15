function Dashboards() {
  return (
    <div>
      <h2>Metrics Dashboards</h2>
      <iframe
        src="http://localhost:3006/d-solo/9db7ad8d-8f0d-4034-92c0-37a3c8b87c9b/95th-percentile-response-time?orgId=1&from=1747296922265&to=1747297042265&timezone=browser&refresh=5m&panelId=1&__feature.dashboardSceneSolo"  
        width="450" 
        height="400"
        frameBorder="0"
        title="Metrics Dashboard"
      ></iframe>
      <iframe src="http://localhost:3006/d-solo/0be38d3d-5deb-42b1-89b6-5937ffe3db49/cpu-usage?orgId=1&from=1747312568673&to=1747334168673&timezone=browser&refresh=5m&panelId=1&__feature.dashboardSceneSolo" width="450" height="400" frameBorder="0"></iframe>
      <iframe src="http://localhost:3006/d-solo/678e42f2-b74b-46ef-8b3f-7c0806633938/new-dashboard?orgId=1&from=1747334233181&to=1747334533181&timezone=browser&refresh=5m&panelId=1&__feature.dashboardSceneSolo" width="450" height="400" frameBorder="0"></iframe>
    </div>
  );
}

export default Dashboards;