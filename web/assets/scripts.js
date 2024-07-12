async function fetchConfig() {
  try {
    const response = await fetch('/get_config');
    const data = await response.json();
    document.getElementById('site-title').innerText = data.siteTitle;
    const sidebarLinks = document.getElementById('sidebar-links');

    if (data.maps.length > 0) {
      changeMap(data.maps[0].link);
    }

    data.maps.forEach(map => {
      const listItem = document.createElement('li');
      const link = document.createElement('a');
      link.href = '#';
      link.onclick = () => changeMap(map.link);
      link.innerHTML = `<i class="fa fa-map"></i><span class="link-text">${map.label}</span>`;
      listItem.appendChild(link);
      sidebarLinks.appendChild(listItem);
    });

    const divider = document.createElement('li');
    divider.className = 'divider';
    sidebarLinks.appendChild(divider);

  } catch (error) {
    console.error('Error fetching config:', error);
  }
}

function changeMap(url) {
  document.getElementById('mapFrame').src = url;
}

function toggleSidebar() {
  const sidebar = document.getElementById('sidebar');
  if (sidebar.style.width === '5%') {
    sidebar.style.width = '20%';
    sidebar.classList.remove('collapsed');
  } else {
    sidebar.style.width = '5%';
    sidebar.classList.add('collapsed');
  }
}

async function showMapInfo() {
  try {
    const mapId = document.getElementById('mapFrame').src.split('/').pop();
    const response = await fetch(`/get_map_info/${mapId}`);
    const mapInfo = await response.json();

    document.querySelector('#infoModal h2').innerText = mapInfo.label;
    document.querySelector('#infoModal p#map-description').innerText = mapInfo.description;
    openModal();
  } catch (error) {
    console.error('Error fetching map info:', error);
  }
}
