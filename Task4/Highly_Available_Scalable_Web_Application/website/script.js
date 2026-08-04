document.addEventListener("DOMContentLoaded", () => {
  const info = window.SERVER_INFO || {};
  const values = {
    instanceId: info.instanceId || "S3 Static Website",
    availabilityZone: info.availabilityZone || "Not applicable",
    privateIp: info.privateIp || "Not applicable",
    hostname: info.hostname || window.location.hostname
  };
  Object.entries(values).forEach(([id, value]) => {
    const element = document.getElementById(id);
    if (element) element.textContent = value;
  });
});
