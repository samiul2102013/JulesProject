import React, { useState, useEffect } from 'react';

const API_URL = 'http://localhost:8000/api/v1';

const Dashboard = () => {
  const [devices, setDevices] = useState([]);
  const [selectedDevice, setSelectedDevice] = useState(null);
  const [telemetry, setTelemetry] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch all devices on component mount
  useEffect(() => {
    const fetchDevices = async () => {
      try {
        const response = await fetch(`${API_URL}/devices/`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setDevices(data);
      } catch (error) {
        setError('Failed to fetch devices. Is the backend server running?');
        console.error('Fetch error:', error);
      }
    };
    fetchDevices();
  }, []);

  // Fetch telemetry data when a device is selected
  useEffect(() => {
    if (!selectedDevice) {
      setTelemetry([]);
      return;
    }

    const fetchTelemetry = async () => {
      setLoading(true);
      try {
        const response = await fetch(`${API_URL}/telemetry/?device_id=${selectedDevice.id}`);
        if (!response.ok) {
          throw new Error('Failed to fetch telemetry data.');
        }
        const data = await response.json();
        setTelemetry(data);
      } catch (error) {
        setError(error.message);
        console.error('Fetch telemetry error:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchTelemetry();
  }, [selectedDevice]);

  return (
    <div>
      <h2>Devices</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <div className="device-list">
        {devices.map(device => (
          <button
            key={device.id}
            onClick={() => setSelectedDevice(device)}
            className={selectedDevice?.id === device.id ? 'active' : ''}
          >
            {device.name} ({device.status})
          </button>
        ))}
      </div>

      {selectedDevice && (
        <div className="telemetry-section">
          <h3>Telemetry for {selectedDevice.name}</h3>
          {loading ? (
            <p>Loading data...</p>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Timestamp</th>
                  <th>Data</th>
                </tr>
              </thead>
              <tbody>
                {telemetry.map(entry => (
                  <tr key={entry.id}>
                    <td>{new Date(entry.timestamp).toLocaleString()}</td>
                    <td>{JSON.stringify(entry.data)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  );
};

export default Dashboard;